#!/usr/bin/env bash
#
# 校验提交信息是否包含中文，规则与 .githooks/commit-msg 一致。
#
#   bash scripts/check-commits.sh                    # 只检查最近一条
#   bash scripts/check-commits.sh origin/main..HEAD  # 检查一个区间
#
# 合并提交（有多个父提交）会被跳过，因为 git 自动生成的信息无法改写。
# 全部合规时退出码 0，存在不合规提交时退出码 1。
#
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"

RANGE="${1:-}"

if [ -z "$RANGE" ]; then
    # 只有一条提交时 HEAD~1 不存在，退回检查 HEAD 本身
    if git rev-parse --verify --quiet HEAD~1 >/dev/null; then
        RANGE="HEAD~1..HEAD"
    else
        RANGE="HEAD"
    fi
fi

COMMITS=$(git rev-list --no-merges "$RANGE" 2>/dev/null || true)

if [ -z "$COMMITS" ]; then
    echo "✔ 没有需要检查的提交（$RANGE）"
    exit 0
fi

has_chinese() {
    perl -CSD -ne 'BEGIN { $f = 0 } $f = 1 if /[\x{4E00}-\x{9FFF}]/; END { exit($f ? 0 : 1) }'
}

FAILED=0
TOTAL=0

while IFS= read -r sha; do
    [ -n "$sha" ] || continue
    TOTAL=$((TOTAL + 1))

    subject=$(git log -1 --format=%s "$sha")
    if ! printf '%s' "$subject" | has_chinese; then
        FAILED=$((FAILED + 1))
        printf '✖ %s  %s\n' "${sha:0:7}" "$subject"
    fi
done <<< "$COMMITS"

if [ "$FAILED" -gt 0 ]; then
    printf '\n✖ %d 条提交信息不含中文（共检查 %d 条）。\n' "$FAILED" "$TOTAL" >&2
    cat >&2 <<'EOF'
  本项目要求提交信息使用中文，格式为「类型: 简要说明」，例如：
    feat: 新增动物图标
    fix: 修正图标导出尺寸
  技术术语可以保留原文，但整句描述的主体必须是中文。
EOF
    exit 1
fi

echo "✔ 提交信息检查通过（$TOTAL 条）"

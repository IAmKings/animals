#!/usr/bin/env bash
#
# 一键配置本地开发环境。新克隆仓库后跑一次即可，重复执行安全。
#
#   bash scripts/setup.sh
#
# 做四件事：
#   1. 启用 .githooks（中文提交校验）
#   2. 自检提交钩子确实生效
#   3. 校验 icons/index.json 与磁盘目录一致
#   4. 检查 PNG 导出所需的渲染器
#
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"

GREEN=''; YELLOW=''; RED=''; RESET=''
if [ -t 1 ]; then
    GREEN=$'\033[32m'; YELLOW=$'\033[33m'; RED=$'\033[31m'; RESET=$'\033[0m'
fi

ok()   { printf '%s✔%s %s\n' "$GREEN" "$RESET" "$1"; }
warn() { printf '%s⚠%s %s\n' "$YELLOW" "$RESET" "$1"; }
fail() { printf '%s✖%s %s\n' "$RED" "$RESET" "$1"; }

WARNINGS=0

printf '\n=== animals 仓库环境配置 ===\n\n'

# --- 1. 确认在仓库根目录 ------------------------------------------------
if [ ! -d .git ]; then
    fail "当前目录不是 git 仓库：$ROOT"
    exit 1
fi

# --- 2. 启用钩子 --------------------------------------------------------
chmod +x .githooks/* 2>/dev/null || true
git config core.hooksPath .githooks
if [ "$(git config core.hooksPath)" = ".githooks" ]; then
    ok "已启用 .githooks（core.hooksPath = .githooks）"
else
    fail "core.hooksPath 设置失败"
    exit 1
fi

# --- 3. 自检提交钩子 ----------------------------------------------------
HOOK_TEST=$(mktemp)
trap 'rm -f "$HOOK_TEST"' EXIT

printf 'add setup script\n' > "$HOOK_TEST"
if .githooks/commit-msg "$HOOK_TEST" >/dev/null 2>&1; then
    fail "钩子自检失败：英文提交信息没有被拦截"
    WARNINGS=$((WARNINGS + 1))
else
    printf 'chore: 新增一键配置脚本\n' > "$HOOK_TEST"
    if .githooks/commit-msg "$HOOK_TEST" >/dev/null 2>&1; then
        ok "钩子自检通过（英文拦截、中文放行）"
    else
        fail "钩子自检失败：中文提交信息被误拦"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# --- 4. 校验 index.json -------------------------------------------------
if ! command -v python3 >/dev/null 2>&1; then
    warn "未找到 python3，跳过 index.json 校验"
    WARNINGS=$((WARNINGS + 1))
elif [ ! -f icons/index.json ]; then
    warn "未找到 icons/index.json，跳过校验"
    WARNINGS=$((WARNINGS + 1))
else
    set +e
    python3 - icons/index.json icons <<'PY'
import json
import os
import sys

index_path, src = sys.argv[1], sys.argv[2]
try:
    with open(index_path, encoding="utf-8") as fh:
        order = json.load(fh)
except Exception as exc:  # noqa: BLE001
    print(f"icons/index.json 解析失败：{exc}")
    sys.exit(1)

if not isinstance(order, list) or not all(isinstance(x, str) for x in order):
    print("icons/index.json 必须是字符串数组")
    sys.exit(1)

disk = sorted(d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d)))
dupes = sorted({x for x in order if order.count(x) > 1})
missing = [x for x in disk if x not in order]
stale = [x for x in order if x not in disk]

if missing:
    print("磁盘有但 index 未收录：" + "、".join(missing))
if stale:
    print("index 有但磁盘不存在：" + "、".join(stale))
if dupes:
    print("index 中重复出现：" + "、".join(dupes))

sys.exit(1 if (missing or stale or dupes) else 0)
PY
    CHECK_RC=$?
    set -e
    if [ "$CHECK_RC" -eq 0 ]; then
        ok "index.json 与磁盘目录一致"
    else
        warn "index.json 与磁盘目录不一致（详见上方），修正后重试"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# --- 5. 渲染器 ----------------------------------------------------------
if command -v rsvg-convert >/dev/null 2>&1; then
    ok "PNG 渲染器：rsvg-convert（推荐）"
elif command -v magick >/dev/null 2>&1; then
    ok "PNG 渲染器：ImageMagick（可用，复杂 SVG 可能失真）"
else
    warn "未找到渲染器，导出 PNG 前需安装：brew install librsvg"
    WARNINGS=$((WARNINGS + 1))
fi

# --- 汇总 ---------------------------------------------------------------
printf '\n'
if [ "$WARNINGS" -eq 0 ]; then
    ok "全部就绪。"
    printf '  提交时请使用中文信息，详见 README 的提交规范。\n\n'
else
    warn "完成，但有 $WARNINGS 项提示需要注意。"
    printf '  不影响正常提交，按需处理即可。\n\n'
fi

#!/usr/bin/env bash
#
# 从 icons/ 下的 SVG 源文件生成 PNG 图标，并校验 icons/index.json 与目录是否一致。
#
# PNG 是派生产物，已在 .gitignore 中排除。需要时运行本脚本即可，
# 不要把它们提交进仓库。
#
# 用法：
#   scripts/export-png.sh                 导出全部，长边 1024px
#   scripts/export-png.sh 512             指定长边尺寸
#   scripts/export-png.sh 1024 cow        只导出指定目录
#
# 环境变量：
#   SKIP_INDEX_CHECK=1   跳过 index.json 一致性校验，只导出
#
# 渲染器：默认使用 ImageMagick 内置渲染器，足以应付单路径图标。
# 若 SVG 含渐变、滤镜、遮罩等复杂特性，请先 brew install librsvg，
# 脚本会自动优先使用 rsvg-convert。
#
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
SIZE="${1:-1024}"
ONLY="${2:-}"
SRC="$ROOT/icons"

if [ ! -d "$SRC" ]; then
    echo "找不到源目录：$SRC" >&2
    exit 1
fi

# 校验 icons/index.json 与磁盘目录是否一一对应。
# 不一致时返回 1，避免导出时用着一份过期的顺序清单。
check_index() {
    local index="$SRC/index.json"

    if [ ! -f "$index" ]; then
        echo "提示：未找到 icons/index.json，跳过一致性校验。" >&2
        return 0
    fi

    if ! command -v python3 >/dev/null 2>&1; then
        echo "提示：需要 python3 才能校验 index.json，已跳过。" >&2
        return 0
    fi

    python3 - "$index" "$SRC" <<'PY'
import json
import os
import sys

index_path, src = sys.argv[1], sys.argv[2]

try:
    with open(index_path, encoding="utf-8") as fh:
        order = json.load(fh)
except Exception as exc:  # noqa: BLE001
    print(f"✖ icons/index.json 解析失败：{exc}", file=sys.stderr)
    sys.exit(1)

if not isinstance(order, list) or not all(isinstance(x, str) for x in order):
    print("✖ icons/index.json 必须是一个字符串数组。", file=sys.stderr)
    sys.exit(1)

disk = sorted(
    d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d))
)
dupes = sorted({x for x in order if order.count(x) > 1})
missing = [x for x in disk if x not in order]
stale = [x for x in order if x not in disk]

problems = []
if missing:
    problems.append("磁盘有但 index 未收录：" + "、".join(missing))
if stale:
    problems.append("index 有但磁盘不存在：" + "、".join(stale))
if dupes:
    problems.append("index 中重复出现：" + "、".join(dupes))

if problems:
    print("✖ icons/index.json 与磁盘目录不一致：", file=sys.stderr)
    for item in problems:
        print(f"  - {item}", file=sys.stderr)
    print("  修正 icons/index.json 后重试，或设 SKIP_INDEX_CHECK=1 跳过校验。",
          file=sys.stderr)
    sys.exit(1)

print(f"index.json 校验通过（{len(order)} 项）")
PY
}

if [ "${SKIP_INDEX_CHECK:-0}" != "1" ]; then
    check_index || exit 1
fi

if command -v rsvg-convert >/dev/null 2>&1; then
    RENDERER="rsvg"
elif command -v magick >/dev/null 2>&1; then
    RENDERER="magick"
else
    echo "需要 rsvg-convert 或 ImageMagick，请先安装其中之一。" >&2
    exit 1
fi

total=0
for dir in "$SRC"/*/; do
    [ -d "$dir" ] || continue
    name=$(basename "$dir")
    if [ -n "$ONLY" ] && [ "$name" != "$ONLY" ]; then
        continue
    fi
    for svg in "$dir"*.svg; do
        [ -f "$svg" ] || continue
        out="${svg%.svg}.png"
        if [ "$RENDERER" = "rsvg" ]; then
            rsvg-convert -w "$SIZE" -h "$SIZE" -b white "$svg" -o "$out"
        else
            magick -background white "$svg" -resize "${SIZE}x${SIZE}" -flatten \
                -colorspace Gray -type Grayscale -depth 8 -strip \
                -define png:compression-level=9 "$out"
        fi
        total=$((total + 1))
    done
done

echo "已生成 $total 个 PNG（长边 ${SIZE}px，渲染器：${RENDERER}）"

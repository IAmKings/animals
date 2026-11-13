#!/usr/bin/env bash
#
# 从 icons/ 下的 SVG 源文件生成 PNG 图标，导出前先校验图标素材组织。
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

if [ "${SKIP_INDEX_CHECK:-0}" != "1" ]; then
    if ! bash "$ROOT/scripts/check-index.sh"; then
        echo "  修正 icons/index.json 后重试，或设 SKIP_INDEX_CHECK=1 跳过校验。" >&2
        exit 1
    fi
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

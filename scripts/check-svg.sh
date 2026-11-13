#!/usr/bin/env bash
#
# 校验 icons/ 下所有 SVG 的语法与结构。
#
#   bash scripts/check-svg.sh            # 检查 icons/ 下全部
#   bash scripts/check-svg.sh icons/cat  # 只检查指定目录
#
# 检查项（任一不通过即退出码 1）：
#   - XML 能否正常解析
#   - 根元素是否为 <svg>
#   - 是否带 viewBox（图标要能缩放，缺了尺寸就固定了）
#   - 是否含 <script> 或 on* 事件属性
#   - 是否引用外部 http(s) 资源（仓库要能离线使用）
#
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"

TARGET="${1:-icons}"

if [ ! -d "$TARGET" ]; then
    echo "✖ 找不到目录：$TARGET" >&2
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "⚠ 未找到 python3，跳过 SVG 校验。" >&2
    exit 0
fi

python3 - "$TARGET" <<'PY'
import glob
import os
import sys
import xml.etree.ElementTree as ET

target = sys.argv[1]
SVG_NS = "http://www.w3.org/2000/svg"

files = sorted(glob.glob(os.path.join(target, "**", "*.svg"), recursive=True))
if not files:
    print(f"✖ {target} 下没有找到 SVG 文件", file=sys.stderr)
    sys.exit(1)

problems = []

for path in files:
    rel = path if os.path.isabs(target) else os.path.relpath(path)

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        problems.append((rel, f"XML 解析失败：{exc}"))
        continue
    except Exception as exc:  # noqa: BLE001
        problems.append((rel, f"读取失败：{exc}"))
        continue

    tag = root.tag
    if tag not in (f"{{{SVG_NS}}}svg", "svg"):
        problems.append((rel, f"根元素不是 <svg>，而是 {tag}"))
        continue

    issues = []

    if "viewBox" not in root.attrib:
        issues.append("缺少 viewBox，图标无法自适应缩放")

    for el in root.iter():
        local = el.tag.split("}")[-1] if isinstance(el.tag, str) else ""
        if local == "script":
            issues.append("包含 <script> 元素")
            break

    for el in root.iter():
        hit = None
        for name, value in el.attrib.items():
            local = name.split("}")[-1]
            if local.startswith("on") and len(local) > 2:
                hit = f"包含事件属性 {local}"
                break
            if isinstance(value, str) and ("http://" in value or "https://" in value):
                hit = f"引用外部资源：{value[:60]}"
                break
        if hit:
            issues.append(hit)
            break

    for issue in issues:
        problems.append((rel, issue))

if problems:
    print(f"✖ {len(problems)} 处 SVG 问题：", file=sys.stderr)
    for rel, reason in problems:
        print(f"  {rel}  {reason}", file=sys.stderr)
    sys.exit(1)

print(f"✔ SVG 语法校验通过（{len(files)} 个文件）")
PY

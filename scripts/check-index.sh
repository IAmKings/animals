#!/usr/bin/env bash
#
# 校验 icons/ 的目录与文件组织。
#
#   bash scripts/check-index.sh
#
# 检查项（任一不通过即退出码 1）：
#   - index.json 无法解析，或不是字符串数组
#   - 磁盘有目录但 index 未收录 / index 有条目但磁盘无目录
#   - index 中同一名字重复出现
#   - 文件名不符合 <目录名>-两位序号.svg
#   - 文件名前缀与所在目录名不一致
#   - 同一目录内序号重复
#   - 目录内混入子目录，或未被 .gitignore 忽略的非 SVG 文件
#
# 隐藏文件（.DS_Store 等）和 .gitignore 忽略的文件（导出的 PNG 等）
# 不参与检查，它们不属于仓库内容。
#
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"

INDEX="icons/index.json"
SRC="icons"

if [ ! -f "$INDEX" ]; then
    echo "✖ 未找到 $INDEX" >&2
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "⚠ 未找到 python3，跳过图标素材校验。" >&2
    exit 0
fi

python3 - "$INDEX" "$SRC" <<'PY'
import json
import os
import re
import subprocess
import sys

index_path, src = sys.argv[1], sys.argv[2]

try:
    with open(index_path, encoding="utf-8") as fh:
        order = json.load(fh)
except Exception as exc:  # noqa: BLE001
    print(f"✖ {index_path} 解析失败：{exc}", file=sys.stderr)
    sys.exit(1)

if not isinstance(order, list) or not all(isinstance(x, str) for x in order):
    print(f"✖ {index_path} 必须是一个字符串数组。", file=sys.stderr)
    sys.exit(1)

disk = sorted(
    d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d))
)

problems = []

dupes = sorted({x for x in order if order.count(x) > 1})
missing = [x for x in disk if x not in order]
stale = [x for x in order if x not in disk]

if missing:
    problems.append("磁盘有但 index 未收录：" + "、".join(missing))
if stale:
    problems.append("index 有但磁盘不存在：" + "、".join(stale))
if dupes:
    problems.append("index 中重复出现：" + "、".join(dupes))


def git_ignored(paths):
    """返回被 .gitignore 忽略的路径集合。git 不可用时返回空集合。"""
    if not paths:
        return set()
    try:
        result = subprocess.run(
            ["git", "check-ignore", "--stdin"],
            input="\n".join(paths),
            capture_output=True,
            text=True,
            check=False,
        )
        return {line for line in result.stdout.splitlines() if line}
    except Exception:  # noqa: BLE001
        return set()


# 先收集文件，跳过隐藏文件；再统一剔除被 git 忽略的（导出的 PNG 等）
candidates = []
for name in disk:
    dir_path = os.path.join(src, name)
    for entry in sorted(os.listdir(dir_path)):
        if entry.startswith("."):
            continue
        full = os.path.join(dir_path, entry)
        if os.path.isdir(full):
            problems.append(f"{name}/{entry} 是子目录，icons 下应为扁平结构")
            continue
        candidates.append((name, entry, full))

ignored = git_ignored([full for _, _, full in candidates])

FILE_PATTERN = re.compile(r"(.+)-(\d{2})\.svg")
total_files = 0
seen_numbers = {}

for name, entry, full in candidates:
    if full in ignored:
        continue

    if not entry.endswith(".svg"):
        problems.append(f"{name}/{entry} 不是 SVG 文件")
        continue

    total_files += 1
    match = FILE_PATTERN.fullmatch(entry)
    if not match:
        problems.append(f"{name}/{entry} 命名不符合 <目录名>-两位序号.svg")
        continue

    prefix, number = match.group(1), match.group(2)
    if prefix != name:
        problems.append(
            f"{name}/{entry} 文件名前缀 {prefix} 与目录名 {name} 不一致"
        )

    key = (name, number)
    if key in seen_numbers:
        problems.append(
            f"{name} 目录内序号 {number} 重复："
            f"{seen_numbers[key]} 与 {entry}"
        )
    else:
        seen_numbers[key] = entry

if problems:
    print(f"✖ 图标素材校验未通过（{len(problems)} 处问题）：", file=sys.stderr)
    for item in problems:
        print(f"  - {item}", file=sys.stderr)
    sys.exit(1)

print(f"✔ 图标素材校验通过（{len(order)} 个目录，{total_files} 个 SVG）")
PY

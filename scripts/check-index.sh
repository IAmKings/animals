#!/usr/bin/env bash
#
# 校验 icons/index.json 与磁盘目录是否一一对应。
#
#   bash scripts/check-index.sh
#
# 一致时退出码 0；发现以下任一情况退出码 1：
#   - 磁盘有目录但 index 未收录
#   - index 有条目但磁盘无对应目录
#   - index 中同一名字重复出现
#   - index.json 无法解析或不是字符串数组
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
    echo "⚠ 未找到 python3，跳过 index 校验。" >&2
    exit 0
fi

python3 - "$INDEX" "$SRC" <<'PY'
import json
import os
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
    print(f"✖ {index_path} 与磁盘目录不一致：", file=sys.stderr)
    for item in problems:
        print(f"  - {item}", file=sys.stderr)
    sys.exit(1)

print(f"✔ index.json 与磁盘目录一致（{len(order)} 项）")
PY

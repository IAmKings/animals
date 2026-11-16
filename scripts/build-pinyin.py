#!/usr/bin/env python3
"""根据 ALIASES 生成 ALIAS_PINYIN（别名拼音表）。

别名拼音需要查字典，所以不在生成页面时实时计算，而是预先算好写进
scripts/build-gallery.py，让 CI 在没有 pypinyin 的环境里也能得到一致的页面。

只在新增或修改别名后需要跑一次：

    pip install pypinyin
    python3 scripts/build-pinyin.py

写入位置由 build-gallery.py 里的首尾标记界定：

    # BEGIN ALIAS_PINYIN
    ALIAS_PINYIN = { ... }
    # END ALIAS_PINYIN
"""

import ast
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "scripts", "build-gallery.py")
BEGIN = "# BEGIN ALIAS_PINYIN"
END = "# END ALIAS_PINYIN"

try:
    from pypinyin import lazy_pinyin
except ImportError:
    sys.exit("✖ 需要 pypinyin：pip install pypinyin")


def read_aliases(src):
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "ALIASES":
            return ast.literal_eval(node.value)
    sys.exit("✖ 没在 build-gallery.py 里找到 ALIASES")


def build_block(terms):
    lines = []
    for term in sorted(terms):
        syllables = [s for s in lazy_pinyin(term) if s]
        full = "".join(syllables)
        abbr = "".join(s[0] for s in syllables)
        lines.append(f'    "{term}": ["{full}", "{abbr}"],')
    return "ALIAS_PINYIN = {\n" + "\n".join(lines) + "\n}\n"


def replace_block(src, block):
    start = src.find(BEGIN)
    end = src.find(END)
    if start < 0 or end < 0 or end < start:
        sys.exit("✖ build-gallery.py 里缺少 ALIAS_PINYIN 首尾标记")
    head = src[:start] + BEGIN + "（由 scripts/build-pinyin.py 生成，请勿手改）\n"
    return head + block + src[end:]


def main():
    src = open(TARGET, encoding="utf-8").read()
    aliases = read_aliases(src)
    terms = {a for values in aliases.values() for a in values}
    out = replace_block(src, build_block(terms))

    try:
        ast.parse(out)
    except SyntaxError as exc:
        sys.exit(f"✖ 生成结果不是合法 Python，已放弃写入：{exc}")

    open(TARGET, "w", encoding="utf-8").write(out)
    print(f"✔ 已写入 {len(terms)} 条别名拼音")


if __name__ == "__main__":
    main()

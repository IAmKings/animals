#!/usr/bin/env python3
"""把 dist/icons 里的 currentColor 图标合并成一个 SVG sprite。

每个图标变成一个 <symbol id="cat-01" viewBox="0 0 100 100" fill="currentColor">，
fill 必须写在 symbol 上：有些源文件的填充色写在根 <svg> 上，抽出来就丢了。
使用方用 <use href="sprite.svg#cat-01"> 引用，同一份文件里
所有图标共享 currentColor，可以整组换色。

依赖 scripts/build-dist.py 先生成 dist/icons。

用法：
    python3 scripts/build-dist.py && python3 scripts/build-sprite.py
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "dist", "icons")
OUT = os.path.join(ROOT, "dist", "sprite.svg")
PER_DIR = os.path.join(ROOT, "dist", "sprites")
INDEX = os.path.join(ROOT, "icons", "index.json")

HEAD = (
    '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">'
    '<!-- 动物图标 sprite：用 <use href="sprite.svg#cat-01"> 引用，颜色跟随 currentColor -->'
)

INNER = re.compile(r"(?s)<svg[^>]*>(.*)</svg>\s*$")
VIEWBOX = re.compile(r'viewBox="([^"]+)"')


def squash(text: str) -> str:
    """压掉路径数据里的换行与多余空格，缩短 sprite 体积。"""
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def main() -> int:
    if not os.path.isdir(SRC):
        return sys.exit("✖ 找不到 dist/icons，请先运行 scripts/build-dist.py")

    with open(INDEX, encoding="utf-8") as f:
        animals = [n for n in json.load(f) if isinstance(n, str)]

    os.makedirs(PER_DIR, exist_ok=True)
    symbols = []
    total = 0
    for name in animals:
        folder = os.path.join(SRC, name)
        if not os.path.isdir(folder):
            continue
        own = []
        for entry in sorted(os.listdir(folder)):
            if not entry.endswith(".svg"):
                continue
            with open(os.path.join(folder, entry), encoding="utf-8") as f:
                text = f.read()
            m = INNER.search(text)
            vb = VIEWBOX.search(text)
            if not m or not vb:
                return sys.exit(f"✖ {name}/{entry}: 结构不符合预期")
            sid = entry[:-4]
            own.append(f'<symbol id="{sid}" viewBox="{vb.group(1)}" fill="currentColor">{squash(m.group(1))}</symbol>')
        symbols.extend(own)
        total += len(own)
        with open(os.path.join(PER_DIR, name + ".svg"), "w", encoding="utf-8") as f:
            f.write(HEAD + "\n" + "\n".join(own) + "\n</svg>\n")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(HEAD + "\n" + "\n".join(symbols) + "\n</svg>\n")

    size = os.path.getsize(OUT) / 1024 / 1024
    print(f"✔ 已生成 dist/sprites/：{len(animals)} 个文件")
    print(f"✔ 已生成 dist/sprite.svg：{total} 个 symbol，{size:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())

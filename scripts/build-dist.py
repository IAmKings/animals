#!/usr/bin/env python3
"""从 icons/ 生成 dist/ 下的 currentColor 版本。

源图标统一是 fill="#000"，只能当黑色用；dist/ 版本把填充色换成
currentColor，放进页面后颜色跟随外层文字颜色，也能被 CSS 覆盖。

用法：
    python3 scripts/build-dist.py
"""

import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "icons")
DST = os.path.join(ROOT, "dist", "icons")

# 根元素上这些属性会写死尺寸；dist 版本只保留 viewBox，交给使用方控制大小
SIZE_ATTR = re.compile(r'\s(?:width|height)="[^"]*"')


def convert(text: str) -> str:
    m = re.match(r"(?s)<svg([^>]*)>", text)
    if not m:
        raise ValueError("找不到 <svg> 根元素")
    attrs = SIZE_ATTR.sub("", m.group(1))
    if 'viewBox="' not in attrs:
        raise ValueError("缺少 viewBox")
    body = text[m.end():]
    # 有的文件把 fill 写在根元素上，有的写在每个 path 上，两种都要换
    out = ("<svg" + attrs + ">" + body).replace('fill="#000"', 'fill="currentColor"')
    if "#000" in out:
        raise ValueError("仍残留写死的黑色")
    return out


def main() -> int:
    if not os.path.isdir(SRC):
        return sys.exit(f"✖ 找不到源目录：{SRC}")

    if os.path.isdir(DST):
        shutil.rmtree(DST)
    os.makedirs(DST)

    count = 0
    for name in sorted(os.listdir(SRC)):
        src_dir = os.path.join(SRC, name)
        if not os.path.isdir(src_dir):
            continue
        dst_dir = os.path.join(DST, name)
        os.makedirs(dst_dir)
        for entry in sorted(os.listdir(src_dir)):
            if not entry.endswith(".svg"):
                continue
            with open(os.path.join(src_dir, entry), encoding="utf-8") as f:
                text = f.read()
            try:
                out = convert(text)
            except ValueError as e:
                return sys.exit(f"✖ {name}/{entry}: {e}")
            with open(os.path.join(dst_dir, entry), "w", encoding="utf-8") as f:
                f.write(out)
            count += 1

    print(f"✔ 已生成 dist/icons：{count} 个 currentColor 图标")
    return 0


if __name__ == "__main__":
    sys.exit(main())

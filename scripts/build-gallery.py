#!/usr/bin/env python3
"""生成 icons/ 的浏览页 index.html（GitHub Pages 入口）。

页面用 <img> 引用真实文件，不内联 SVG 内容，所以打开时看到的就是
icons/ 里的文件本身，不会和磁盘上的素材不同步。

用法：
    python3 scripts/build-gallery.py
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, "icons")
INDEX = os.path.join(ICONS, "index.json")
OUTPUT = os.path.join(ROOT, "index.html")

TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>动物图标库 · __COUNT__ 个图标</title>
<style>
  :root {
    --bg: #f7f7f5;
    --surface: #ffffff;
    --line: #e4e4df;
    --ink: #1a1a18;
    --muted: #8a8a84;
    --accent: #2f6f4e;
    --accent-soft: #eaf2ed;
    --radius: 10px;
    --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; }
  body {
    background: var(--bg);
    color: var(--ink);
    font: 14px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
          "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  header {
    position: sticky; top: 0; z-index: 20;
    display: flex; align-items: center; gap: 16px;
    padding: 14px 24px;
    background: rgba(247, 247, 245, .88);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--line);
  }
  header h1 { margin: 0; font-size: 15px; font-weight: 600; letter-spacing: .01em; }
  header .stat { color: var(--muted); font-size: 13px; font-variant-numeric: tabular-nums; }
  header .spacer { flex: 1; }

  .search { position: relative; }
  .search input {
    width: 240px; padding: 7px 12px 7px 30px;
    border: 1px solid var(--line); border-radius: 8px;
    background: var(--surface); color: var(--ink);
    font: inherit; font-size: 13px;
    outline: none; transition: border-color .15s, box-shadow .15s;
  }
  .search input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
  .search svg { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); width: 13px; height: 13px; stroke: var(--muted); fill: none; stroke-width: 2; }

  .layout { display: flex; align-items: flex-start; gap: 24px; padding: 24px; max-width: 1500px; margin: 0 auto; }
  main { flex: 1; min-width: 0; }

  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 16px; }

  .card {
    background: var(--surface); border: 1px solid var(--line);
    border-radius: var(--radius); padding: 12px 12px 10px;
  }
  .card-head { display: flex; align-items: baseline; gap: 8px; margin: 0 2px 10px; }
  .card-head .name { font-family: var(--mono); font-size: 12.5px; letter-spacing: .02em; }
  .card-head .count { margin-left: auto; color: var(--muted); font-size: 11.5px; font-variant-numeric: tabular-nums; }

  .variants { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; }

  .tile {
    position: relative; display: block; width: 100%; aspect-ratio: 1;
    padding: 6px; border: 1px solid transparent; border-radius: 8px;
    background: #fbfbfa; cursor: pointer; transition: background .12s, border-color .12s, transform .12s;
  }
  .tile:hover { background: var(--accent-soft); transform: translateY(-1px); }
  .tile img { width: 100%; height: 100%; object-fit: contain; display: block; }
  .tile .tag {
    position: absolute; left: 5px; bottom: 3px;
    font-family: var(--mono); font-size: 9.5px; color: var(--muted);
    opacity: 0; transition: opacity .12s;
  }
  .tile:hover .tag, .tile.selected .tag { opacity: 1; }
  .tile.selected { border-color: var(--accent); background: var(--accent-soft); }
  .tile.selected::after {
    content: ""; position: absolute; right: 4px; top: 4px;
    width: 7px; height: 7px; border-radius: 50%; background: var(--accent);
  }

  aside {
    position: sticky; top: 76px; width: 320px; flex: none;
    background: var(--surface); border: 1px solid var(--line);
    border-radius: var(--radius); padding: 16px;
  }
  aside.empty { color: var(--muted); font-size: 13px; text-align: center; padding: 48px 16px; }
  .preview {
    display: flex; align-items: center; justify-content: center;
    height: 180px; background: #fbfbfa; border-radius: 8px; margin-bottom: 14px;
  }
  .preview img { max-width: 150px; max-height: 150px; }
  .meta { font-family: var(--mono); font-size: 12px; line-height: 1.9; word-break: break-all; }
  .meta .k { color: var(--muted); }
  .actions { display: flex; gap: 8px; margin-top: 14px; }
  button {
    font: inherit; font-size: 12.5px; padding: 7px 12px; border-radius: 7px;
    border: 1px solid var(--line); background: var(--surface); color: var(--ink);
    cursor: pointer; transition: background .12s, border-color .12s;
  }
  button:hover { background: #f2f2ef; }
  button.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
  button.primary:hover { background: #275c41; }
  button.wide { flex: 1; }

  .selbar {
    position: fixed; left: 50%; bottom: 20px; transform: translateX(-50%);
    display: flex; align-items: center; gap: 12px;
    padding: 9px 12px 9px 16px;
    background: var(--ink); color: #fff; border-radius: 999px;
    box-shadow: 0 6px 24px rgba(0,0,0,.18); font-size: 13px;
    opacity: 0; pointer-events: none; transition: opacity .15s, transform .15s;
  }
  .selbar.show { opacity: 1; pointer-events: auto; transform: translateX(-50%) translateY(0); }
  .selbar .n { font-variant-numeric: tabular-nums; }
  .selbar button { background: transparent; border-color: rgba(255,255,255,.28); color: #fff; padding: 5px 11px; }
  .selbar button:hover { background: rgba(255,255,255,.12); }

  .toast {
    position: fixed; left: 50%; bottom: 84px; transform: translateX(-50%) translateY(6px);
    background: var(--accent); color: #fff; font-size: 12.5px;
    padding: 7px 14px; border-radius: 999px; opacity: 0;
    transition: opacity .18s, transform .18s; pointer-events: none; z-index: 40;
  }
  .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }

  .hidden { display: none !important; }

  @media (max-width: 900px) {
    .layout { flex-direction: column; padding: 16px; }
    aside { position: static; width: 100%; }
    header { flex-wrap: wrap; padding: 12px 16px; }
    .search input { width: 160px; }
  }
</style>
</head>
<body>

<header>
  <h1>动物图标库</h1>
  <span class="stat" id="stat"></span>
  <span class="spacer"></span>
  <div class="search">
    <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
    <input id="q" type="search" placeholder="搜索动物名" autocomplete="off">
  </div>
</header>

<div class="layout">
  <main><div class="grid" id="grid"></div></main>
  <aside class="empty" id="aside">点击任意图标查看详情</aside>
</div>

<div class="selbar" id="selbar">
  <span>已选 <span class="n" id="selcount">0</span> 个</span>
  <button id="copyall">复制全部路径</button>
  <button id="clearall">清空</button>
</div>

<div class="toast" id="toast"></div>

<script>
const DATA = __DATA__;

const grid = document.getElementById('grid');
const stat = document.getElementById('stat');
const aside = document.getElementById('aside');
const selbar = document.getElementById('selbar');
const selcount = document.getElementById('selcount');
const toastEl = document.getElementById('toast');

const selected = new Set();
let current = null;

const total = DATA.reduce((n, a) => n + a.variants.length, 0);
stat.textContent = DATA.length + ' 种动物 · ' + total + ' 个图标';

function el(tag, cls, html) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (html != null) node.innerHTML = html;
  return node;
}

for (const animal of DATA) {
  const card = el('div', 'card');
  const head = el('div', 'card-head');
  head.appendChild(el('span', 'name', animal.name));
  head.appendChild(el('span', 'count', animal.variants.length + ' 变体'));
  card.appendChild(head);

  const wrap = el('div', 'variants');
  for (const v of animal.variants) {
    const tile = el('button', 'tile');
    tile.type = 'button';
    tile.dataset.path = v.path;
    tile.title = v.path;

    const img = document.createElement('img');
    img.src = v.path;
    img.alt = v.name;
    img.loading = 'lazy';
    tile.appendChild(img);
    tile.appendChild(el('span', 'tag', v.index));

    tile.addEventListener('click', () => pick(v, tile));
    wrap.appendChild(tile);
  }
  card.appendChild(wrap);
  card.dataset.animal = animal.name;
  grid.appendChild(card);
}

function pick(v, tile) {
  current = v;
  if (selected.has(v.path)) {
    selected.delete(v.path);
    tile.classList.remove('selected');
  } else {
    selected.add(v.path);
    tile.classList.add('selected');
  }
  renderAside(v);
  renderSelbar();
}

function renderAside(v) {
  aside.className = '';
  aside.innerHTML = '';

  const preview = el('div', 'preview');
  const img = document.createElement('img');
  img.src = v.path;
  img.alt = v.name;
  preview.appendChild(img);
  aside.appendChild(preview);

  const meta = el('div', 'meta');
  meta.innerHTML =
    '<div><span class="k">名称 </span>' + v.name + '</div>' +
    '<div><span class="k">序号 </span>' + v.index + '</div>' +
    '<div><span class="k">路径 </span>' + v.path + '</div>';
  aside.appendChild(meta);

  const actions = el('div', 'actions');
  const copyBtn = el('button', 'primary wide', '复制路径');
  copyBtn.addEventListener('click', () => copy(v.path, '已复制路径'));
  const copyTag = el('button', 'wide', '复制 img 标签');
  copyTag.addEventListener('click', () => copy(
    '<img src="' + v.path + '" alt="' + v.name + '">',
    '已复制 img 标签'
  ));
  actions.appendChild(copyBtn);
  actions.appendChild(copyTag);
  aside.appendChild(actions);
}

function renderSelbar() {
  selcount.textContent = selected.size;
  selbar.classList.toggle('show', selected.size > 0);
}

document.getElementById('clearall').addEventListener('click', () => {
  selected.clear();
  document.querySelectorAll('.tile.selected').forEach(t => t.classList.remove('selected'));
  renderSelbar();
});

document.getElementById('copyall').addEventListener('click', () => {
  copy([...selected].join('\\n'), '已复制 ' + selected.size + ' 条路径');
});

async function copy(text, msg) {
  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
  }
  toast(msg);
}

let toastTimer;
function toast(msg) {
  toastEl.textContent = msg;
  toastEl.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toastEl.classList.remove('show'), 1600);
}

document.getElementById('q').addEventListener('input', (e) => {
  const q = e.target.value.trim().toLowerCase();
  for (const card of grid.children) {
    const hit = !q || card.dataset.animal.toLowerCase().includes(q);
    card.classList.toggle('hidden', !hit);
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    selected.clear();
    document.querySelectorAll('.tile.selected').forEach(t => t.classList.remove('selected'));
    renderSelbar();
  }
});
</script>
</body>
</html>
"""


def main():
    if not os.path.isfile(INDEX):
        sys.exit("✖ 未找到 icons/index.json")

    with open(INDEX, encoding="utf-8") as fh:
        order = json.load(fh)

    data = []
    total = 0
    for name in order:
        dir_path = os.path.join(ICONS, name)
        if not os.path.isdir(dir_path):
            sys.exit(f"✖ 目录不存在：icons/{name}")

        variants = []
        for entry in sorted(os.listdir(dir_path)):
            if not entry.endswith(".svg"):
                continue
            stem = entry[: -len(".svg")]
            index = stem.rsplit("-", 1)[-1]
            variants.append(
                {"name": stem, "index": index, "path": f"icons/{name}/{entry}"}
            )

        if not variants:
            sys.exit(f"✖ icons/{name} 下没有 SVG")
        total += len(variants)
        data.append({"name": name, "variants": variants})

    html = TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    html = html.replace("__COUNT__", str(total))

    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write(html)

    size = os.path.getsize(OUTPUT) / 1024
    print(f"✔ 已生成 index.html（{len(data)} 种动物，{total} 个图标，{size:.0f} KB）")


if __name__ == "__main__":
    main()

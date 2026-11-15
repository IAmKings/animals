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

# 目录名 → 中文名。新增动物时必须在这里补一条，否则生成脚本会报错，
# 避免出现「图标有了但搜不到中文名」的情况。
ZH_NAMES = {
    "ant": "蚂蚁",
    "ape": "猿",
    "bat": "蝙蝠",
    "bee": "蜜蜂",
    "butterfly": "蝴蝶",
    "cat": "猫",
    "chicken": "鸡",
    "cicada": "蝉",
    "cockroach": "蟑螂",
    "cow": "牛",
    "crocodile": "鳄鱼",
    "dinosaur": "恐龙",
    "dog": "狗",
    "dolphin": "海豚",
    "elephant": "大象",
    "fly": "苍蝇",
    "frog": "青蛙",
    "giraffe": "长颈鹿",
    "gorilla": "大猩猩",
    "horse": "马",
    "lion": "狮子",
    "monkey": "猴子",
    "mosquito": "蚊子",
    "mouse": "老鼠",
    "octopus": "章鱼",
    "panda": "熊猫",
    "parrot": "鹦鹉",
    "polar-bear": "北极熊",
    "rabbit": "兔子",
    "shark": "鲨鱼",
    "sheep": "绵羊",
    "snake": "蛇",
    "spider": "蜘蛛",
    "tiger": "老虎",
    "turtle": "乌龟",
    "whale": "鲸鱼",
    "wolfdog": "狼狗",    "bear": "熊",
    "centipede": "蜈蚣",
    "cobra": "眼镜蛇",
    "crab": "螃蟹",
    "crow": "乌鸦",
    "dragonfly": "蜻蜓",
    "earthworm": "蚯蚓",
    "firefly": "萤火虫",
    "fox": "狐狸",
    "fruit-fly": "果蝇",
    "goldfish": "金鱼",
    "hamster": "仓鼠",
    "jellyfish": "水母",
    "kingfisher": "翠鸟",
    "lizard": "蜥蜴",
    "lobster": "龙虾",
    "mammoth": "猛犸象",
    "orca": "虎鲸",
    "owl": "猫头鹰",
    "penguin": "企鹅",
    "pigeon": "鸽子",
    "piranha": "食人鱼",
    "rhinoceros": "犀牛",
    "silkworm": "蚕",
    "snail": "蜗牛",
    "sparrow": "麻雀",
    "squirrel": "松鼠",
    "totoro": "龙猫",    "camel": "骆驼",
    "electric-eel": "电鳗",
    "hedgehog": "刺猬",
    "hippo": "河马",
    "hummingbird": "蜂鸟",
    "kangaroo": "袋鼠",
    "pangolin": "穿山甲",
    "pig": "猪",
    "reindeer": "驯鹿",
    "sea-slug": "海蛞蝓",
    "sea-turtle": "海龟",
    "seahorse": "海马",
    "sloth": "树懒",
    "squid": "鱿鱼",
    "zebra-finch": "斑胸草雀",    "beetle": "甲虫",
    "beluga": "白鲸",
    "cheetah": "猎豹",
    "cricket": "蟋蟀",
    "dairy-cow": "奶牛",
    "duck": "鸭子",
    "falcon": "猎鹰",
    "leopard-cat": "豹猫",
    "mantis-shrimp": "螳螂虾",
    "naked-mole-rat": "裸鼹鼠",
    "pika": "鼠兔",
    "pufferfish": "河豚",
    "raccoon": "浣熊",
    "salmon": "鲑鱼",
    "scorpion": "蝎子",
    "sea-lion": "海狮",
    "seabird": "海鸟",
    "seagull": "海鸥",
    "shrimp": "虾",
    "snow-leopard": "雪豹",
    "swallow": "燕子",
    "tardigrade": "水熊虫",
    "vulture": "秃鹫",
    "wild-boar": "野猪",
    "woodpecker": "啄木鸟",
    "yangtze-giant-softshell": "斑鳖",
}

# 额外的中文别名，用来覆盖口语说法（搜「小强」也能找到蟑螂）。
ALIASES = {
    "ant": ["小蚂蚁"],
    "ape": ["猩猩", "类人猿"],
    "bat": ["小蝙蝠"],
    "bee": ["小蜜蜂"],
    "butterfly": ["蝶"],
    "cat": ["猫咪", "小猫"],
    "chicken": ["小鸡", "母鸡"],
    "cicada": ["知了"],
    "cockroach": ["小强"],
    "cow": ["黄牛"],
    "crocodile": ["鳄"],
    "dinosaur": ["霸王龙", "龙"],
    "dog": ["犬", "小狗"],
    "dolphin": ["小海豚"],
    "elephant": ["象"],
    "fly": ["蝇", "小苍蝇"],
    "frog": ["蛙", "田鸡"],
    "giraffe": ["鹿"],
    "gorilla": ["猩猩"],
    "horse": ["骏马"],
    "lion": ["狮"],
    "monkey": ["猴"],
    "mosquito": ["小蚊子"],
    "mouse": ["鼠", "小老鼠"],
    "octopus": ["八爪鱼"],
    "panda": ["大熊猫", "猫熊"],
    "parrot": ["鹦哥"],
    "polar-bear": ["白熊", "熊"],
    "rabbit": ["兔", "小兔"],
    "shark": ["鲨"],
    "sheep": ["羊", "小羊"],
    "snake": ["蟒蛇", "小蛇"],
    "spider": ["小蜘蛛"],
    "tiger": ["虎"],
    "turtle": ["龟", "海龟"],
    "whale": ["鲸"],
    "wolfdog": ["狼", "狼犬"],    "bear": ["小熊"],
    "centipede": ["百足虫"],
    "crab": ["蟹", "大闸蟹"],
    "crow": ["老鸹"],
    "earthworm": ["地龙"],
    "fox": ["小狐狸"],
    "hamster": ["小仓鼠"],
    "jellyfish": ["海蜇"],
    "kingfisher": ["鱼狗"],
    "lizard": ["四脚蛇"],
    "mammoth": ["长毛象"],
    "orca": ["杀人鲸"],
    "owl": ["夜猫子"],
    "penguin": ["小企鹅"],
    "pigeon": ["白鸽"],
    "piranha": ["水虎鱼"],
    "silkworm": ["蚕宝宝"],
    "snail": ["小蜗牛"],
    "sparrow": ["家雀"],
    "squirrel": ["小松鼠"],
    "totoro": ["豆豆龙", "托托罗"],    "kangaroo": ["小袋鼠"],
    "pangolin": ["鲮鲤"],
    "pig": ["小猪"],
    "sea-slug": ["海兔"],
    "sea-turtle": ["绿海龟"],
    "sloth": ["树獭"],
    "zebra-finch": ["斑马雀"],    "cricket": ["蛐蛐"],
    "duck": ["鸭"],
    "falcon": ["隼"],
    "mantis-shrimp": ["皮皮虾"],
    "pufferfish": ["河鲀"],
    "salmon": ["三文鱼"],
    "shrimp": ["小虾"],
    "tardigrade": ["缓步动物"],
    "yangtze-giant-softshell": ["扬子鳖"],
}

# 目录名 → 拼音。每项是「全拼 + 首字母缩写」，搜索时都能命中。
# 全拼按中文名逐字拼，缩写取每个字的声母（大猩猩 → daxingxing / dxx）。
PINYIN = {
    "ant": ["mayi", "my"],
    "ape": ["yuan", "y"],
    "bat": ["bianfu", "bf"],
    "bee": ["mifeng", "mf"],
    "butterfly": ["hudie", "hd"],
    "cat": ["mao", "m"],
    "chicken": ["ji", "j"],
    "cicada": ["chan", "c"],
    "cockroach": ["zhanglang", "zl"],
    "cow": ["niu", "n"],
    "crocodile": ["eyu", "ey"],
    "dinosaur": ["konglong", "kl"],
    "dog": ["gou", "g"],
    "dolphin": ["haitun", "ht"],
    "elephant": ["daxiang", "dx"],
    "fly": ["cangying", "cy"],
    "frog": ["qingwa", "qw"],
    "giraffe": ["changjinglu", "cjl"],
    "gorilla": ["daxingxing", "dxx"],
    "horse": ["ma", "m"],
    "lion": ["shizi", "sz"],
    "monkey": ["houzi", "hz"],
    "mosquito": ["wenzi", "wz"],
    "mouse": ["laoshu", "ls"],
    "octopus": ["zhangyu", "zy"],
    "panda": ["xiongmao", "xiong", "xm"],
    "parrot": ["yingwu", "yw"],
    "polar-bear": ["beijixiong", "bjx"],
    "rabbit": ["tuzi", "tz"],
    "shark": ["shayu", "sy"],
    "sheep": ["mianyang", "my"],
    "snake": ["she", "s"],
    "spider": ["zhizhu", "zz"],
    "tiger": ["laohu", "lh"],
    "turtle": ["wugui", "wg"],
    "whale": ["jingyu", "jy"],
    "wolfdog": ["langgou", "lg"],    "bear": ["xiong", "x"],
    "centipede": ["wugong", "wg"],
    "cobra": ["yanjingshe", "yjs"],
    "crab": ["pangxie", "px"],
    "crow": ["wuya", "wy"],
    "dragonfly": ["qingting", "qt"],
    "earthworm": ["qiuyin", "qy"],
    "firefly": ["yinghuochong", "yhc"],
    "fox": ["huli", "hl"],
    "fruit-fly": ["guoying", "gy"],
    "goldfish": ["jinyu", "jy"],
    "hamster": ["cangshu", "cs"],
    "jellyfish": ["shuimu", "sm"],
    "kingfisher": ["cuiniao", "cn"],
    "lizard": ["xiyi", "xy"],
    "lobster": ["longxia", "lx"],
    "mammoth": ["mengmaxiang", "mmx"],
    "orca": ["hujing", "hj"],
    "owl": ["maotouying", "mty"],
    "penguin": ["qie", "qe"],
    "pigeon": ["gezi", "gz"],
    "piranha": ["shirenyu", "sry"],
    "rhinoceros": ["xiniu", "xn"],
    "silkworm": ["can", "c"],
    "snail": ["woniu", "wn"],
    "sparrow": ["maque", "mq"],
    "squirrel": ["songshu", "ss"],
    "totoro": ["longmao", "lm"],    "camel": ["luotuo", "lt"],
    "electric-eel": ["dianman", "dm"],
    "hedgehog": ["ciwei", "cw"],
    "hippo": ["hema", "hm"],
    "hummingbird": ["fengniao", "fn"],
    "kangaroo": ["daishu", "ds"],
    "pangolin": ["chuanshanjia", "csj"],
    "pig": ["zhu", "z"],
    "reindeer": ["xunlu", "xl"],
    "sea-slug": ["haikuoyu", "hky"],
    "sea-turtle": ["haigui", "hg"],
    "seahorse": ["haima", "hm"],
    "sloth": ["shulan", "sl"],
    "squid": ["youyu", "yy"],
    "zebra-finch": ["banxiongcaoque", "bxcq"],    "beetle": ["jiachong", "jc"],
    "beluga": ["baijing", "bj"],
    "cheetah": ["liebao", "lb"],
    "cricket": ["xishuai", "xs"],
    "dairy-cow": ["nainiu", "nn"],
    "duck": ["yazi", "yz"],
    "falcon": ["lieying", "ly"],
    "leopard-cat": ["baomao", "bm"],
    "mantis-shrimp": ["tanglangxia", "tlx"],
    "naked-mole-rat": ["luoyanshu", "lys"],
    "pika": ["shutu", "st"],
    "pufferfish": ["hetun", "ht"],
    "raccoon": ["huanxiong", "hx"],
    "salmon": ["guiyu", "gy"],
    "scorpion": ["xiezi", "xz"],
    "sea-lion": ["haishi", "hs"],
    "seabird": ["hainiao", "hn"],
    "seagull": ["haiou", "ho"],
    "shrimp": ["xia", "x"],
    "snow-leopard": ["xuebao", "xb"],
    "swallow": ["yanzi", "yz"],
    "tardigrade": ["shuixiongchong", "sxc"],
    "vulture": ["tujiu", "tj"],
    "wild-boar": ["yezhu", "yz"],
    "woodpecker": ["zhuomuniao", "zmn"],
    "yangtze-giant-softshell": ["banbie", "bb"],
}

# 页面图标：优先用 cat-01，缺失时退回任意一个图标。
FAVICON = "icons/cat/cat-01.svg"

TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>动物图标库 · __COUNT__ 个图标</title>
<link rel="icon" href="__FAVICON__" type="image/svg+xml">
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
  .card-head .zh { font-size: 13px; font-weight: 600; letter-spacing: .02em; }
  .card-head .name { font-family: var(--mono); font-size: 12px; color: var(--muted); letter-spacing: .02em; }
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
    <input id="q" type="search" placeholder="搜索动物名，支持中文与拼音" autocomplete="off">
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
  head.appendChild(el('span', 'zh', animal.zh));
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
  card.dataset.search = [animal.name, animal.zh, ...(animal.aliases || [])]
    .join(' ')
    .toLowerCase();
  card.dataset.pinyin = (animal.pinyin || []).join(' ');
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
    '<div><span class="k">名称 </span>' + v.zh + '（' + v.name + '）</div>' +
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
    // 中文名与目录名按包含匹配；拼音按前缀匹配，避免 ji 命中「长颈鹿」
    const hit = !q ||
      card.dataset.search.includes(q) ||
      card.dataset.pinyin.split(' ').some((p) => p && p.startsWith(q));
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
    missing_zh = []
    missing_pinyin = []
    for name in order:
        dir_path = os.path.join(ICONS, name)
        if not os.path.isdir(dir_path):
            sys.exit(f"✖ 目录不存在：icons/{name}")

        zh = ZH_NAMES.get(name)
        if not zh:
            missing_zh.append(name)
            continue
        pinyin = PINYIN.get(name)
        if not pinyin:
            missing_pinyin.append(name)
            continue
        aliases = ALIASES.get(name, [])

        variants = []
        for entry in sorted(os.listdir(dir_path)):
            if not entry.endswith(".svg"):
                continue
            stem = entry[: -len(".svg")]
            index = stem.rsplit("-", 1)[-1]
            variants.append(
                {
                    "name": stem,
                    "index": index,
                    "zh": zh,
                    "path": f"icons/{name}/{entry}",
                }
            )

        if not variants:
            sys.exit(f"✖ icons/{name} 下没有 SVG")
        total += len(variants)
        data.append(
            {
                "name": name,
                "zh": zh,
                "aliases": aliases,
                "pinyin": pinyin,
                "variants": variants,
            }
        )

    problems = []
    if missing_zh:
        problems.append("缺少中文名（ZH_NAMES）：" + "、".join(missing_zh))
    if missing_pinyin:
        problems.append("缺少拼音（PINYIN）：" + "、".join(missing_pinyin))
    if problems:
        sys.exit("✖ 以下目录信息不全，请在对应表中补充：\n  " + "\n  ".join(problems))

    html = TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    html = html.replace("__COUNT__", str(total))
    html = html.replace("__FAVICON__", FAVICON)

    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write(html)

    size = os.path.getsize(OUTPUT) / 1024
    print(f"✔ 已生成 index.html（{len(data)} 种动物，{total} 个图标，{size:.0f} KB）")


if __name__ == "__main__":
    main()

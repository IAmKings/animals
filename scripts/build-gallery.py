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
    "albatross": "信天翁",
    "ant": "蚂蚁",
    "ape": "猿",
    "baboon": "狒狒",
    "bat": "蝙蝠",
    "bear": "熊",
    "beaver": "河狸",
    "bee": "蜜蜂",
    "beetle": "甲虫",
    "beluga": "白鲸",
    "butterfly": "蝴蝶",
    "camel": "骆驼",
    "cat": "猫",
    "caterpillar": "毛毛虫",
    "catfish": "鲶鱼",
    "centipede": "蜈蚣",
    "cheetah": "猎豹",
    "chicken": "鸡",
    "chinese-sturgeon": "中华鲟",
    "cicada": "蝉",
    "cobra": "眼镜蛇",
    "cockroach": "蟑螂",
    "coral-reef": "珊瑚礁",
    "cordyceps": "冬虫夏草",
    "cow": "牛",
    "crab": "螃蟹",
    "crested-ibis": "朱鹮",
    "cricket": "蟋蟀",
    "crocodile": "鳄鱼",
    "crow": "乌鸦",
    "dairy-cow": "奶牛",
    "deer": "鹿",
    "dinosaur": "恐龙",
    "dog": "狗",
    "dolphin": "海豚",
    "dragonfly": "蜻蜓",
    "duck": "鸭子",
    "dust-mite": "尘螨",
    "eagle": "鹰",
    "earthworm": "蚯蚓",
    "electric-eel": "电鳗",
    "elephant": "大象",
    "emperor-penguin": "帝企鹅",
    "falcon": "猎鹰",
    "firefly": "萤火虫",
    "flamingo": "火烈鸟",
    "fly": "苍蝇",
    "fox": "狐狸",
    "frog": "青蛙",
    "fruit-fly": "果蝇",
    "gecko": "壁虎",
    "giraffe": "长颈鹿",
    "goat": "山羊",
    "goldfish": "金鱼",
    "gorilla": "大猩猩",
    "hammerhead-shark": "双髻鲨",
    "hamster": "仓鼠",
    "hedgehog": "刺猬",
    "hippo": "河马",
    "horse": "马",
    "horseshoe-crab": "鲎",
    "hummingbird": "蜂鸟",
    "jellyfish": "水母",
    "kangaroo": "袋鼠",
    "kingfisher": "翠鸟",
    "leopard-cat": "豹猫",
    "lion": "狮子",
    "lizard": "蜥蜴",
    "lobster": "龙虾",
    "lungfish": "肺鱼",
    "mammoth": "猛犸象",
    "manatee": "海牛",
    "mantis-shrimp": "螳螂虾",
    "mermaid": "美人鱼",
    "migratory-bird": "候鸟",
    "monkey": "猴子",
    "mosquito": "蚊子",
    "mouse": "老鼠",
    "naked-mole-rat": "裸鼹鼠",
    "nautilus": "鹦鹉螺",
    "octopus": "章鱼",
    "orca": "虎鲸",
    "ostrich": "鸵鸟",
    "owl": "猫头鹰",
    "oyster": "牡蛎",
    "pacific-saury": "秋刀鱼",
    "panda": "熊猫",
    "pangolin": "穿山甲",
    "parasitoid-wasp": "寄生蜂",
    "parrot": "鹦鹉",
    "pelican": "鹈鹕",
    "penguin": "企鹅",
    "pig": "猪",
    "pigeon": "鸽子",
    "pika": "鼠兔",
    "piranha": "食人鱼",
    "polar-bear": "北极熊",
    "porcupine": "豪猪",
    "pufferfish": "河豚",
    "rabbit": "兔子",
    "raccoon": "浣熊",
    "red-panda": "小熊猫",
    "reindeer": "驯鹿",
    "rhinoceros": "犀牛",
    "saiga": "高鼻羚羊",
    "salmon": "鲑鱼",
    "sawfish": "锯鳐",
    "scorpion": "蝎子",
    "sea-lion": "海狮",
    "sea-slug": "海蛞蝓",
    "sea-turtle": "海龟",
    "seabird": "海鸟",
    "seagull": "海鸥",
    "seahorse": "海马",
    "shark": "鲨鱼",
    "sheep": "绵羊",
    "shrimp": "虾",
    "silkworm": "蚕",
    "sloth": "树懒",
    "slug": "蛞蝓",
    "snail": "蜗牛",
    "snake": "蛇",
    "snow-leopard": "雪豹",
    "sparrow": "麻雀",
    "spider": "蜘蛛",
    "squid": "鱿鱼",
    "squirrel": "松鼠",
    "swallow": "燕子",
    "tardigrade": "水熊虫",
    "termite": "白蚁",
    "tiger": "老虎",
    "toad": "蟾蜍",
    "totoro": "龙猫",
    "turkey": "火鸡",
    "turtle": "乌龟",
    "tyrannosaurus": "霸王龙",
    "vulture": "秃鹫",
    "walrus": "海象",
    "warthog": "疣猪",
    "whale": "鲸鱼",
    "wild-boar": "野猪",
    "wolfdog": "狼狗",
    "woodpecker": "啄木鸟",
    "yak": "牦牛",
    "yangtze-giant-softshell": "斑鳖",
    "zebra-finch": "斑胸草雀",
    "zebrafish": "斑马鱼",
}

# 额外的中文别名，用来覆盖口语说法（搜「小强」也能找到蟑螂）。
ALIASES = {
    "ant": ["小蚂蚁"],
    "ape": ["猩猩", "类人猿"],
    "bat": ["小蝙蝠"],
    "bear": ["小熊"],
    "beaver": ["海狸"],
    "bee": ["小蜜蜂"],
    "butterfly": ["蝶"],
    "cat": ["猫咪", "小猫"],
    "caterpillar": ["毛虫"],
    "centipede": ["百足虫"],
    "chicken": ["小鸡", "母鸡"],
    "chinese-sturgeon": ["鲟鱼"],
    "cicada": ["知了"],
    "cockroach": ["小强"],
    "cordyceps": ["虫草"],
    "cow": ["黄牛"],
    "crab": ["蟹", "大闸蟹"],
    "crested-ibis": ["朱鹭"],
    "cricket": ["蛐蛐"],
    "crocodile": ["鳄"],
    "crow": ["老鸹"],
    "dinosaur": ["霸王龙", "龙"],
    "dog": ["犬", "小狗"],
    "dolphin": ["小海豚"],
    "duck": ["鸭"],
    "earthworm": ["地龙"],
    "elephant": ["象"],
    "falcon": ["隼"],
    "fly": ["蝇", "小苍蝇"],
    "fox": ["小狐狸"],
    "frog": ["蛙", "田鸡"],
    "giraffe": ["鹿"],
    "gorilla": ["猩猩"],
    "hammerhead-shark": ["锤头鲨"],
    "hamster": ["小仓鼠"],
    "horse": ["骏马"],
    "horseshoe-crab": ["马蹄蟹"],
    "jellyfish": ["海蜇"],
    "kangaroo": ["小袋鼠"],
    "kingfisher": ["鱼狗"],
    "lion": ["狮"],
    "lizard": ["四脚蛇"],
    "mammoth": ["长毛象"],
    "mantis-shrimp": ["皮皮虾"],
    "monkey": ["猴"],
    "mosquito": ["小蚊子"],
    "mouse": ["鼠", "小老鼠"],
    "octopus": ["八爪鱼"],
    "orca": ["杀人鲸"],
    "owl": ["夜猫子"],
    "oyster": ["生蚝"],
    "panda": ["大熊猫", "猫熊"],
    "pangolin": ["鲮鲤"],
    "parrot": ["鹦哥"],
    "penguin": ["小企鹅"],
    "pig": ["小猪"],
    "pigeon": ["白鸽"],
    "piranha": ["水虎鱼"],
    "polar-bear": ["白熊", "熊"],
    "pufferfish": ["河鲀"],
    "rabbit": ["兔", "小兔"],
    "red-panda": ["红熊猫"],
    "saiga": ["赛加羚羊"],
    "salmon": ["三文鱼"],
    "sea-slug": ["海兔"],
    "sea-turtle": ["绿海龟"],
    "shark": ["鲨"],
    "sheep": ["羊", "小羊"],
    "shrimp": ["小虾"],
    "silkworm": ["蚕宝宝"],
    "sloth": ["树獭"],
    "slug": ["鼻涕虫"],
    "snail": ["小蜗牛"],
    "snake": ["蟒蛇", "小蛇"],
    "sparrow": ["家雀"],
    "spider": ["小蜘蛛"],
    "squirrel": ["小松鼠"],
    "tardigrade": ["缓步动物"],
    "tiger": ["虎"],
    "toad": ["癞蛤蟆"],
    "totoro": ["豆豆龙", "托托罗"],
    "turtle": ["龟", "海龟"],
    "tyrannosaurus": ["暴龙"],
    "whale": ["鲸"],
    "wolfdog": ["狼", "狼犬"],
    "yangtze-giant-softshell": ["扬子鳖"],
    "zebra-finch": ["斑马雀"],
}

# 目录名 → 拼音。每项是「全拼 + 首字母缩写」，搜索时都能命中。
# 全拼按中文名逐字拼，缩写取每个字的声母（大猩猩 → daxingxing / dxx）。
PINYIN = {
    "albatross": ["xintianweng", "xtw"],
    "ant": ["mayi", "my"],
    "ape": ["yuan", "y"],
    "baboon": ["feifei", "ff"],
    "bat": ["bianfu", "bf"],
    "bear": ["xiong", "x"],
    "beaver": ["heli", "hl"],
    "bee": ["mifeng", "mf"],
    "beetle": ["jiachong", "jc"],
    "beluga": ["baijing", "bj"],
    "butterfly": ["hudie", "hd"],
    "camel": ["luotuo", "lt"],
    "cat": ["mao", "m"],
    "caterpillar": ["maomaochong", "mmc"],
    "catfish": ["nianyu", "ny"],
    "centipede": ["wugong", "wg"],
    "cheetah": ["liebao", "lb"],
    "chicken": ["ji", "j"],
    "chinese-sturgeon": ["zhonghuaxun", "zhx"],
    "cicada": ["chan", "c"],
    "cobra": ["yanjingshe", "yjs"],
    "cockroach": ["zhanglang", "zl"],
    "coral-reef": ["shanhujiao", "shj"],
    "cordyceps": ["dongchongxiacao", "dcxc"],
    "cow": ["niu", "n"],
    "crab": ["pangxie", "px"],
    "crested-ibis": ["zhuhuan", "zh"],
    "cricket": ["xishuai", "xs"],
    "crocodile": ["eyu", "ey"],
    "crow": ["wuya", "wy"],
    "dairy-cow": ["nainiu", "nn"],
    "deer": ["lu", "l"],
    "dinosaur": ["konglong", "kl"],
    "dog": ["gou", "g"],
    "dolphin": ["haitun", "ht"],
    "dragonfly": ["qingting", "qt"],
    "duck": ["yazi", "yz"],
    "dust-mite": ["chenman", "cm"],
    "eagle": ["ying", "y"],
    "earthworm": ["qiuyin", "qy"],
    "electric-eel": ["dianman", "dm"],
    "elephant": ["daxiang", "dx"],
    "emperor-penguin": ["diqie", "dqe"],
    "falcon": ["lieying", "ly"],
    "firefly": ["yinghuochong", "yhc"],
    "flamingo": ["huolieniao", "hln"],
    "fly": ["cangying", "cy"],
    "fox": ["huli", "hl"],
    "frog": ["qingwa", "qw"],
    "fruit-fly": ["guoying", "gy"],
    "gecko": ["bihu", "bh"],
    "giraffe": ["changjinglu", "cjl"],
    "goat": ["shanyang", "sy"],
    "goldfish": ["jinyu", "jy"],
    "gorilla": ["daxingxing", "dxx"],
    "hammerhead-shark": ["shuangjisha", "sjs"],
    "hamster": ["cangshu", "cs"],
    "hedgehog": ["ciwei", "cw"],
    "hippo": ["hema", "hm"],
    "horse": ["ma", "m"],
    "horseshoe-crab": ["hou", "h"],
    "hummingbird": ["fengniao", "fn"],
    "jellyfish": ["shuimu", "sm"],
    "kangaroo": ["daishu", "ds"],
    "kingfisher": ["cuiniao", "cn"],
    "leopard-cat": ["baomao", "bm"],
    "lion": ["shizi", "sz"],
    "lizard": ["xiyi", "xy"],
    "lobster": ["longxia", "lx"],
    "lungfish": ["feiyu", "fy"],
    "mammoth": ["mengmaxiang", "mmx"],
    "manatee": ["hainiu", "hn"],
    "mantis-shrimp": ["tanglangxia", "tlx"],
    "mermaid": ["meirenyu", "mry"],
    "migratory-bird": ["houniao", "hn"],
    "monkey": ["houzi", "hz"],
    "mosquito": ["wenzi", "wz"],
    "mouse": ["laoshu", "ls"],
    "naked-mole-rat": ["luoyanshu", "lys"],
    "nautilus": ["yingwuluo", "ywl"],
    "octopus": ["zhangyu", "zy"],
    "orca": ["hujing", "hj"],
    "ostrich": ["tuoniao", "tn"],
    "owl": ["maotouying", "mty"],
    "oyster": ["muli", "ml"],
    "pacific-saury": ["qiudaoyu", "qdy"],
    "panda": ["xiongmao", "xiong", "xm"],
    "pangolin": ["chuanshanjia", "csj"],
    "parasitoid-wasp": ["jishengfeng", "jsf"],
    "parrot": ["yingwu", "yw"],
    "pelican": ["tihu", "th"],
    "penguin": ["qie", "qe"],
    "pig": ["zhu", "z"],
    "pigeon": ["gezi", "gz"],
    "pika": ["shutu", "st"],
    "piranha": ["shirenyu", "sry"],
    "polar-bear": ["beijixiong", "bjx"],
    "porcupine": ["haozhu", "hz"],
    "pufferfish": ["hetun", "ht"],
    "rabbit": ["tuzi", "tz"],
    "raccoon": ["huanxiong", "hx"],
    "red-panda": ["xiaoxiongmao", "xxm"],
    "reindeer": ["xunlu", "xl"],
    "rhinoceros": ["xiniu", "xn"],
    "saiga": ["gaobilingyang", "gbly"],
    "salmon": ["guiyu", "gy"],
    "sawfish": ["juyao", "jy"],
    "scorpion": ["xiezi", "xz"],
    "sea-lion": ["haishi", "hs"],
    "sea-slug": ["haikuoyu", "hky"],
    "sea-turtle": ["haigui", "hg"],
    "seabird": ["hainiao", "hn"],
    "seagull": ["haiou", "ho"],
    "seahorse": ["haima", "hm"],
    "shark": ["shayu", "sy"],
    "sheep": ["mianyang", "my"],
    "shrimp": ["xia", "x"],
    "silkworm": ["can", "c"],
    "sloth": ["shulan", "sl"],
    "slug": ["kuoyu", "ky"],
    "snail": ["woniu", "wn"],
    "snake": ["she", "s"],
    "snow-leopard": ["xuebao", "xb"],
    "sparrow": ["maque", "mq"],
    "spider": ["zhizhu", "zz"],
    "squid": ["youyu", "yy"],
    "squirrel": ["songshu", "ss"],
    "swallow": ["yanzi", "yz"],
    "tardigrade": ["shuixiongchong", "sxc"],
    "termite": ["baiyi", "by"],
    "tiger": ["laohu", "lh"],
    "toad": ["chanchu", "cc"],
    "totoro": ["longmao", "lm"],
    "turkey": ["huaji", "hj"],
    "turtle": ["wugui", "wg"],
    "tyrannosaurus": ["bawanglong", "bwl"],
    "vulture": ["tujiu", "tj"],
    "walrus": ["haixiang", "hx"],
    "warthog": ["youzhu", "yz"],
    "whale": ["jingyu", "jy"],
    "wild-boar": ["yezhu", "yz"],
    "wolfdog": ["langgou", "lg"],
    "woodpecker": ["zhuomuniao", "zmn"],
    "yak": ["maoniu", "mn"],
    "yangtze-giant-softshell": ["banbie", "bb"],
    "zebra-finch": ["banxiongcaoque", "bxcq"],
    "zebrafish": ["banmayu", "bmy"],
}

# BEGIN ALIAS_PINYIN（由 scripts/build-pinyin.py 生成，请勿手改）
ALIAS_PINYIN = {
    "三文鱼": ["sanwenyu", "swy"],
    "兔": ["tu", "t"],
    "八爪鱼": ["bazhaoyu", "bzy"],
    "四脚蛇": ["sijiaoshe", "sjs"],
    "地龙": ["dilong", "dl"],
    "夜猫子": ["yemaozi", "ymz"],
    "大熊猫": ["daxiongmao", "dxm"],
    "大闸蟹": ["dazhaxie", "dzx"],
    "家雀": ["jiaqiao", "jq"],
    "小仓鼠": ["xiaocangshu", "xcs"],
    "小企鹅": ["xiaoqie", "xqe"],
    "小兔": ["xiaotu", "xt"],
    "小强": ["xiaoqiang", "xq"],
    "小松鼠": ["xiaosongshu", "xss"],
    "小海豚": ["xiaohaitun", "xht"],
    "小熊": ["xiaoxiong", "xx"],
    "小狐狸": ["xiaohuli", "xhl"],
    "小狗": ["xiaogou", "xg"],
    "小猪": ["xiaozhu", "xz"],
    "小猫": ["xiaomao", "xm"],
    "小羊": ["xiaoyang", "xy"],
    "小老鼠": ["xiaolaoshu", "xls"],
    "小苍蝇": ["xiaocangying", "xcy"],
    "小虾": ["xiaoxia", "xx"],
    "小蚂蚁": ["xiaomayi", "xmy"],
    "小蚊子": ["xiaowenzi", "xwz"],
    "小蛇": ["xiaoshe", "xs"],
    "小蜗牛": ["xiaowoniu", "xwn"],
    "小蜘蛛": ["xiaozhizhu", "xzz"],
    "小蜜蜂": ["xiaomifeng", "xmf"],
    "小蝙蝠": ["xiaobianfu", "xbf"],
    "小袋鼠": ["xiaodaishu", "xds"],
    "小鸡": ["xiaoji", "xj"],
    "托托罗": ["tuotuoluo", "ttl"],
    "扬子鳖": ["yangzibie", "yzb"],
    "斑马雀": ["banmaque", "bmq"],
    "暴龙": ["baolong", "bl"],
    "朱鹭": ["zhulu", "zl"],
    "杀人鲸": ["sharenjing", "srj"],
    "树獭": ["shuta", "st"],
    "母鸡": ["muji", "mj"],
    "毛虫": ["maochong", "mc"],
    "水虎鱼": ["shuihuyu", "shy"],
    "河鲀": ["hetun", "ht"],
    "海兔": ["haitu", "ht"],
    "海狸": ["haili", "hl"],
    "海蜇": ["haizhe", "hz"],
    "海龟": ["haigui", "hg"],
    "熊": ["xiong", "x"],
    "犬": ["quan", "q"],
    "狮": ["shi", "s"],
    "狼": ["lang", "l"],
    "狼犬": ["langquan", "lq"],
    "猩猩": ["xingxing", "xx"],
    "猫咪": ["maomi", "mm"],
    "猫熊": ["maoxiong", "mx"],
    "猴": ["hou", "h"],
    "生蚝": ["shenghao", "sh"],
    "田鸡": ["tianji", "tj"],
    "癞蛤蟆": ["laihama", "lhm"],
    "白熊": ["baixiong", "bx"],
    "白鸽": ["baige", "bg"],
    "百足虫": ["baizuchong", "bzc"],
    "皮皮虾": ["pipixia", "ppx"],
    "知了": ["zhiliao", "zl"],
    "类人猿": ["leirenyuan", "lry"],
    "红熊猫": ["hongxiongmao", "hxm"],
    "绿海龟": ["lvhaigui", "lhg"],
    "缓步动物": ["huanbudongwu", "hbdw"],
    "羊": ["yang", "y"],
    "老鸹": ["laogua", "lg"],
    "虎": ["hu", "h"],
    "虫草": ["chongcao", "cc"],
    "蚕宝宝": ["canbaobao", "cbb"],
    "蛐蛐": ["ququ", "qq"],
    "蛙": ["wa", "w"],
    "蝇": ["ying", "y"],
    "蝶": ["die", "d"],
    "蟒蛇": ["mangshe", "ms"],
    "蟹": ["xie", "x"],
    "豆豆龙": ["doudoulong", "ddl"],
    "象": ["xiang", "x"],
    "赛加羚羊": ["saijialingyang", "sjly"],
    "锤头鲨": ["chuitousha", "cts"],
    "长毛象": ["changmaoxiang", "cmx"],
    "隼": ["sun", "s"],
    "霸王龙": ["bawanglong", "bwl"],
    "马蹄蟹": ["matixie", "mtx"],
    "骏马": ["junma", "jm"],
    "鱼狗": ["yugou", "yg"],
    "鲟鱼": ["xunyu", "xy"],
    "鲨": ["sha", "s"],
    "鲮鲤": ["lingli", "ll"],
    "鲸": ["jing", "j"],
    "鳄": ["e", "e"],
    "鸭": ["ya", "y"],
    "鹦哥": ["yingge", "yg"],
    "鹿": ["lu", "l"],
    "黄牛": ["huangniu", "hn"],
    "鼠": ["shu", "s"],
    "鼻涕虫": ["bitichong", "btc"],
    "龙": ["long", "l"],
    "龟": ["gui", "g"],
}
# END ALIAS_PINYIN

# 替代拼写：pypinyin 只给一种读法，ü 与多音字另有常见写法，手工补充。
# 值会并进该别名的拼音列表，匹配规则与主拼写相同（前缀匹配）。
ALIAS_EXTRA = {
    "绿海龟": ["luhaigui"],
    "家雀": ["jiaque"],
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

  /* 多列瀑布流：卡片高度各自独立，不会为了对齐行高被拉长或留白 */
  .grid { column-width: 310px; column-gap: 16px; }
  .card { break-inside: avoid; page-break-inside: avoid; margin: 0 0 16px; }

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

  .pager {
    display: flex; align-items: center; justify-content: center; gap: 6px;
    padding: 4px 0 56px; flex-wrap: wrap;
  }
  .pager button { min-width: 34px; padding: 6px 9px; font-variant-numeric: tabular-nums; }
  .pager button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  .pager button:disabled { opacity: .35; cursor: default; }
  .pager button:disabled:hover { background: var(--surface); }
  .pager .info { color: var(--muted); font-size: 12.5px; margin-left: 8px; }

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
  <main>
    <div class="grid" id="grid"></div>
    <nav class="pager" id="pager">
      <button id="prev" type="button">上一页</button>
      <span id="pages" style="display:contents"></span>
      <button id="next" type="button">下一页</button>
      <span class="info" id="pageinfo"></span>
    </nav>
  </main>
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

const PAGE_SIZE = 24;
let page = 0;
const cards = [...grid.children];
const pageCount = Math.max(1, Math.ceil(cards.length / PAGE_SIZE));
const pager = document.getElementById('pager');
const pagesEl = document.getElementById('pages');
const pageinfo = document.getElementById('pageinfo');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');

function query() {
  return document.getElementById('q').value.trim().toLowerCase();
}

function isMatch(card, q) {
  // 中文名与目录名按包含匹配；拼音按前缀匹配，避免 ji 命中「长颈鹿」
  return !q ||
    card.dataset.search.includes(q) ||
    card.dataset.pinyin.split(' ').some((p) => p && p.startsWith(q));
}

function apply() {
  const q = query();
  const searching = q.length > 0;
  let shown = 0;
  cards.forEach((card, i) => {
    const hit = isMatch(card, q);
    const onPage = i >= page * PAGE_SIZE && i < (page + 1) * PAGE_SIZE;
    const visible = hit && (searching || onPage);
    card.classList.toggle('hidden', !visible);
    if (visible) shown += 1;
  });

  pager.classList.toggle('hidden', searching);
  if (searching) {
    pageinfo.textContent = '搜索到 ' + shown + ' 种';
    return;
  }
  pageinfo.textContent = '第 ' + (page + 1) + ' / ' + pageCount + ' 页 · 共 ' + cards.length + ' 种';
  pagesEl.innerHTML = '';
  for (let i = 0; i < pageCount; i += 1) {
    const b = el('button', i === page ? 'active' : '', String(i + 1));
    b.type = 'button';
    b.addEventListener('click', () => go(i));
    pagesEl.appendChild(b);
  }
  prevBtn.disabled = page === 0;
  nextBtn.disabled = page === pageCount - 1;
}

function go(i) {
  page = Math.max(0, Math.min(pageCount - 1, i));
  apply();
  if (window.scrollY > 0) window.scrollTo({ top: 0, behavior: 'smooth' });
}

prevBtn.addEventListener('click', () => go(page - 1));
nextBtn.addEventListener('click', () => go(page + 1));
document.getElementById('q').addEventListener('input', apply);
apply();

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
    missing_alias_pinyin = []
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
        alias_pinyin = []
        for alias in aliases:
            ap = ALIAS_PINYIN.get(alias)
            if not ap:
                missing_alias_pinyin.append(alias)
                continue
            alias_pinyin.extend(ap)
            alias_pinyin.extend(ALIAS_EXTRA.get(alias, []))

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
                "pinyin": pinyin + alias_pinyin,
                "variants": variants,
            }
        )

    unknown_extra = sorted(set(ALIAS_EXTRA) - {a for v in ALIASES.values() for a in v})
    if unknown_extra:
        sys.exit("✖ ALIAS_EXTRA 里有不属于任何动物的别名：" + "、".join(unknown_extra))

    problems = []
    if missing_zh:
        problems.append("缺少中文名（ZH_NAMES）：" + "、".join(missing_zh))
    if missing_pinyin:
        problems.append("缺少拼音（PINYIN）：" + "、".join(missing_pinyin))
    if missing_alias_pinyin:
        problems.append(
            "缺少别名拼音（ALIAS_PINYIN）：" + "、".join(sorted(set(missing_alias_pinyin)))
        )
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

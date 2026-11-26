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
    "ant-leaf": "切叶蚁",
    "antelope": "羚羊",
    "ape": "猿",
    "aphid": "蚜虫",
    "archaeopteryx": "始祖鸟",
    "archerfish": "射水鱼",
    "armadillo": "犰狳",
    "arowana": "龙鱼",
    "baboon": "狒狒",
    "barrel-jellyfish": "桶水母",
    "bat": "蝙蝠",
    "bear": "熊",
    "beaver": "河狸",
    "bedbug": "臭虫",
    "bee": "蜜蜂",
    "beetle": "甲虫",
    "beluga": "白鲸",
    "bichir": "多鳍鱼",
    "bird": "鸟",
    "black-snub-nosed-monkey": "金丝猴",
    "bornean-rhinoceros": "婆罗洲犀",
    "bumblebee": "熊蜂",
    "bumpy-toad": "疣蟾",
    "butterfly": "蝴蝶",
    "c-elegans": "秀丽隐杆线虫",
    "caddisfly": "石蛾",
    "camel": "骆驼",
    "cat": "猫",
    "caterpillar": "毛毛虫",
    "catfish": "鲶鱼",
    "cave-lion": "洞狮",
    "centipede": "蜈蚣",
    "cheetah": "猎豹",
    "chicken": "鸡",
    "chihuahua": "吉娃娃",
    "chinchilla": "毛丝鼠",
    "chinese-pond-turtle": "中华草龟",
    "chinese-softshell-turtle": "中华鳖",
    "chinese-sturgeon": "中华鲟",
    "cicada": "蝉",
    "climbing-perch": "攀鲈",
    "cobra": "眼镜蛇",
    "cockatoo": "凤头鹦鹉",
    "cockroach": "蟑螂",
    "coelacanth": "腔棘鱼",
    "color-changing-frog": "变色蛙",
    "comb-jelly": "栉水母",
    "coral-reef": "珊瑚礁",
    "cordyceps": "冬虫夏草",
    "cow": "牛",
    "crab": "螃蟹",
    "crayfish": "小龙虾",
    "crested-ibis": "朱鹮",
    "cricket": "蟋蟀",
    "crocodile": "鳄鱼",
    "crow": "乌鸦",
    "cuckoo": "杜鹃",
    "dairy-cow": "奶牛",
    "darkling-beetle": "拟步甲",
    "deep-sea-isopod": "深海具足虫",
    "deer": "鹿",
    "desert-spider": "沙漠蛛",
    "dinosaur": "恐龙",
    "dodo": "渡渡鸟",
    "dog": "狗",
    "dolphin": "海豚",
    "donkey": "驴",
    "dragon": "龙",
    "dragonfly": "蜻蜓",
    "duck": "鸭子",
    "dust-mite": "尘螨",
    "eagle": "鹰",
    "earthworm": "蚯蚓",
    "eel": "鳗鱼",
    "electric-eel": "电鳗",
    "elephant": "大象",
    "emperor-penguin": "帝企鹅",
    "eurypterid": "板足鲎",
    "falcon": "猎鹰",
    "ferret": "雪貂",
    "firefly": "萤火虫",
    "fish": "鱼",
    "fish-mascot": "卡通鱼",
    "fishing-spider": "捕鱼蛛",
    "flamingo": "火烈鸟",
    "flea": "跳蚤",
    "fly": "苍蝇",
    "fly-catching-ant": "捕蝇蚁",
    "flying-cat": "飞猫",
    "fox": "狐狸",
    "frog": "青蛙",
    "fruit-fly": "果蝇",
    "fulmar": "暴风鹱",
    "galapagos-tortoise": "加拉帕戈斯象龟",
    "gecko": "壁虎",
    "giant-clam": "大砗磲",
    "giant-jaw-ant": "巨颚蚁",
    "giant-salamander": "大鲵",
    "giraffe": "长颈鹿",
    "glass-frog": "玻璃蛙",
    "glowing-firebug": "发光萤火虫",
    "goat": "山羊",
    "golden-pheasant": "锦鸡",
    "goldfish": "金鱼",
    "goose": "鹅",
    "gorilla": "大猩猩",
    "grasshopper": "蚱蜢",
    "grebe": "鸊鷉",
    "green-haired-turtle": "绿毛龟",
    "guppy": "孔雀鱼",
    "hammerhead-shark": "双髻鲨",
    "hamster": "仓鼠",
    "hedgehog": "刺猬",
    "hippo": "河马",
    "honey-badger": "蜜獾",
    "hoopoe": "戴胜",
    "hornbill": "犀鸟",
    "hornet": "胡蜂",
    "horse": "马",
    "horseshoe-crab": "鲎",
    "huamei": "画眉",
    "hummingbird": "蜂鸟",
    "hummingbird-moth": "蜂鸟鹰蛾",
    "hyena": "鬣狗",
    "insect": "昆虫",
    "jaw-worm": "颚蠕虫",
    "jellyfish": "水母",
    "jerboa": "跳鼠",
    "kangaroo": "袋鼠",
    "kea": "啄羊鹦鹉",
    "kingfisher": "翠鸟",
    "koi": "锦鲤",
    "krill": "磷虾",
    "leech": "水蛭",
    "lemming": "旅鼠",
    "leopard-cat": "豹猫",
    "lion": "狮子",
    "lizard": "蜥蜴",
    "lobster": "龙虾",
    "long-necked-dinosaur": "长颈恐龙",
    "lungfish": "肺鱼",
    "magpie": "喜鹊",
    "maine-coon": "缅因猫",
    "mammoth": "猛犸象",
    "manatee": "海牛",
    "mandarin-fish": "鳜鱼",
    "mangrove-finch": "红树林树雀",
    "manta-ray": "蝠鲼",
    "mantis-fly": "螳蛉",
    "mantis-shrimp": "螳螂虾",
    "marbled-cat": "石纹猫",
    "marmoset": "狨猴",
    "marmot": "土拨鼠",
    "mermaid": "美人鱼",
    "migratory-bird": "候鸟",
    "monkey": "猴子",
    "mosasaurus": "沧龙",
    "mosquito": "蚊子",
    "moth": "蛾子",
    "mouse": "老鼠",
    "mudskipper": "弹涂鱼",
    "mussel": "贻贝",
    "naked-mole-rat": "裸鼹鼠",
    "narwhal": "独角鲸",
    "nautilus": "鹦鹉螺",
    "ocean-sunfish": "翻车鱼",
    "octopus": "章鱼",
    "opossum": "负鼠",
    "orca": "虎鲸",
    "oriole": "黄鹂",
    "ostrich": "鸵鸟",
    "otter": "水獭",
    "owl": "猫头鹰",
    "oyster": "牡蛎",
    "pacific-saury": "秋刀鱼",
    "panda": "熊猫",
    "pangolin": "穿山甲",
    "paradoxical-frog": "奇异蛙",
    "parasitoid-wasp": "寄生蜂",
    "parrot": "鹦鹉",
    "parrotfish": "鹦嘴鱼",
    "peacock-spider": "孔雀跳蛛",
    "pelican": "鹈鹕",
    "penguin": "企鹅",
    "pig": "猪",
    "pigeon": "鸽子",
    "pika": "鼠兔",
    "piranha": "食人鱼",
    "pistol-shrimp": "鼓虾",
    "platypus": "鸭嘴兽",
    "plesiosaur": "蛇颈龙",
    "plump-bird": "胖鸟",
    "pocket-shark": "口袋鲨",
    "polar-bear": "北极熊",
    "porcupine": "豪猪",
    "prehistoric-primate": "史前灵长类",
    "pterosaur": "翼龙",
    "pufferfish": "河豚",
    "rabbit": "兔子",
    "raccoon": "浣熊",
    "raccoon-dog": "貉",
    "rattlesnake": "响尾蛇",
    "red-panda": "小熊猫",
    "reed-parrotbill": "震旦鸦雀",
    "reindeer": "驯鹿",
    "rhinoceros": "犀牛",
    "ribbon-winged-lacewing": "丝翅草蛉",
    "ribbon-worm": "纽虫",
    "rice-planthopper": "稻飞虱",
    "ring-tailed-lemur": "环尾狐猴",
    "rooster": "公鸡",
    "rose-tarantula": "玫瑰捕鸟蛛",
    "saiga": "高鼻羚羊",
    "salamander": "蝾螈",
    "salmon": "鲑鱼",
    "sand-cat": "沙猫",
    "sawfish": "锯鳐",
    "scallop": "扇贝",
    "scaly-foot-snail": "鳞足螺",
    "schistosome": "血吸虫",
    "scorpion": "蝎子",
    "sea-cucumber": "海参",
    "sea-hare": "海兔",
    "sea-lion": "海狮",
    "sea-otter": "海獭",
    "sea-slug": "海蛞蝓",
    "sea-turtle": "海龟",
    "seabird": "海鸟",
    "seagull": "海鸥",
    "seahorse": "海马",
    "seal": "海豹",
    "shark": "鲨鱼",
    "sheep": "绵羊",
    "shell-creature": "蛤蜊",
    "shrimp": "虾",
    "shy-bird": "羞怯鸟",
    "sichuan-bush-warbler": "四川树莺",
    "silkworm": "蚕",
    "sloth": "树懒",
    "slug": "蛞蝓",
    "snail": "蜗牛",
    "snail-shell": "螺",
    "snake": "蛇",
    "snow-leopard": "雪豹",
    "softshell-turtle": "鳖",
    "solenodon": "沟齿鼩",
    "sparrow": "麻雀",
    "spectacled-bear": "眼镜熊",
    "sperm-whale": "抹香鲸",
    "spider": "蜘蛛",
    "spider-crab": "蜘蛛蟹",
    "spiny-lizard": "刺蜥",
    "sponge": "海绵",
    "squid": "鱿鱼",
    "squirrel": "松鼠",
    "starfish": "海星",
    "starling": "椋鸟",
    "stink-bug": "椿象",
    "swallow": "燕子",
    "tadpole": "蝌蚪",
    "takin": "羚牛",
    "tapir": "貘",
    "tardigrade": "水熊虫",
    "termite": "白蚁",
    "tick": "蜱虫",
    "tiger": "老虎",
    "toad": "蟾蜍",
    "totoro": "龙猫",
    "toxoplasma": "弓形虫",
    "transparent-fish": "透明鱼",
    "trilobite": "三叶虫",
    "turkey": "火鸡",
    "turtle": "乌龟",
    "tyrannosaurus": "霸王龙",
    "urmia-gull": "遗鸥",
    "vampire-bat": "吸血蝠",
    "viscacha": "山绒鼠",
    "vulture": "秃鹫",
    "walrus": "海象",
    "warthog": "疣猪",
    "water-buffalo": "水牛",
    "whale": "鲸鱼",
    "whale-shark": "鲸鲨",
    "wild-boar": "野猪",
    "wildcat": "野猫",
    "wolf": "狼",
    "wolfdog": "狼狗",
    "wood-cockroach": "木蠊",
    "woodpecker": "啄木鸟",
    "worm": "蠕虫",
    "yak": "牦牛",
    "yangtze-giant-softshell": "斑鳖",
    "yellow-breasted-bunting": "黄胸鹀",
    "zebra": "斑马",
    "zebra-finch": "斑胸草雀",
    "zebrafish": "斑马鱼",
}

# 额外的中文别名，用来覆盖口语说法（搜「小强」也能找到蟑螂）。
ALIASES = {
    "ant": ["小蚂蚁"],
    "ape": ["猩猩", "类人猿"],
    "aphid": ["腻虫"],
    "archerfish": ["喷水鱼"],
    "arowana": ["金龙鱼"],
    "bat": ["小蝙蝠"],
    "bear": ["小熊"],
    "beaver": ["海狸"],
    "bedbug": ["床虱"],
    "bee": ["小蜜蜂"],
    "black-snub-nosed-monkey": ["仰鼻猴"],
    "bornean-rhinoceros": ["婆罗洲犀牛"],
    "bumblebee": ["大黄蜂"],
    "butterfly": ["蝶"],
    "c-elegans": ["线虫"],
    "cat": ["猫咪", "小猫"],
    "caterpillar": ["毛虫"],
    "centipede": ["百足虫"],
    "chicken": ["小鸡", "母鸡"],
    "chinchilla": ["栗鼠"],
    "chinese-softshell-turtle": ["甲鱼"],
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
    "cuckoo": ["布谷鸟"],
    "dinosaur": ["霸王龙", "龙"],
    "dog": ["犬", "小狗"],
    "dolphin": ["小海豚"],
    "donkey": ["毛驴"],
    "dragon": ["中国龙"],
    "duck": ["鸭"],
    "earthworm": ["地龙"],
    "elephant": ["象"],
    "eurypterid": ["海蝎"],
    "falcon": ["隼"],
    "fly": ["蝇", "小苍蝇"],
    "fox": ["小狐狸"],
    "frog": ["蛙", "田鸡"],
    "fulmar": ["管鼻鹱"],
    "giant-clam": ["砗磲"],
    "giant-salamander": ["娃娃鱼"],
    "giraffe": ["鹿"],
    "golden-pheasant": ["红腹锦鸡"],
    "gorilla": ["猩猩"],
    "grasshopper": ["蚂蚱"],
    "hammerhead-shark": ["锤头鲨"],
    "hamster": ["小仓鼠"],
    "honey-badger": ["平头哥"],
    "hornet": ["马蜂"],
    "horse": ["骏马"],
    "horseshoe-crab": ["马蹄蟹"],
    "hummingbird-moth": ["蜂鸟蛾"],
    "hyena": ["土狼"],
    "jellyfish": ["海蜇"],
    "kangaroo": ["小袋鼠"],
    "kingfisher": ["鱼狗"],
    "leech": ["蚂蟥"],
    "lion": ["狮"],
    "lizard": ["四脚蛇"],
    "mammoth": ["长毛象"],
    "mandarin-fish": ["桂花鱼"],
    "manta-ray": ["魔鬼鱼"],
    "mantis-shrimp": ["皮皮虾"],
    "marmoset": ["绢毛猴"],
    "marmot": ["旱獭"],
    "monkey": ["猴"],
    "mosquito": ["小蚊子"],
    "moth": ["飞蛾"],
    "mouse": ["鼠", "小老鼠"],
    "mudskipper": ["跳跳鱼"],
    "mussel": ["淡菜"],
    "narwhal": ["一角鲸"],
    "octopus": ["八爪鱼"],
    "orca": ["杀人鲸"],
    "otter": ["海獭", "獭"],
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
    "raccoon-dog": ["貉子"],
    "red-panda": ["红熊猫"],
    "reed-parrotbill": ["鸦雀"],
    "rooster": ["雄鸡"],
    "saiga": ["赛加羚羊"],
    "salmon": ["三文鱼"],
    "sea-slug": ["海兔"],
    "sea-turtle": ["绿海龟"],
    "shark": ["鲨"],
    "sheep": ["羊", "小羊"],
    "shell-creature": ["贝壳"],
    "shrimp": ["小虾"],
    "silkworm": ["蚕宝宝"],
    "sloth": ["树獭"],
    "slug": ["鼻涕虫"],
    "snail": ["小蜗牛"],
    "snail-shell": ["田螺"],
    "snake": ["蟒蛇", "小蛇"],
    "sparrow": ["家雀"],
    "spider": ["小蜘蛛"],
    "spiny-lizard": ["强棱蜥"],
    "squirrel": ["小松鼠"],
    "stink-bug": ["臭大姐"],
    "takin": ["扭角羚"],
    "tardigrade": ["缓步动物"],
    "tick": ["蜱"],
    "tiger": ["虎"],
    "toad": ["癞蛤蟆"],
    "totoro": ["豆豆龙", "托托罗"],
    "toxoplasma": ["弓形体"],
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
    "ant-leaf": ["qieyeyi", "qyy"],
    "antelope": ["lingyang", "ly"],
    "ape": ["yuan", "y"],
    "aphid": ["yachong", "yc"],
    "archaeopteryx": ["shizuniao", "szn"],
    "archerfish": ["sheshuiyu", "ssy"],
    "armadillo": ["qiuyu", "qy"],
    "arowana": ["longyu", "ly"],
    "baboon": ["feifei", "ff"],
    "barrel-jellyfish": ["tongshuimu", "tsm"],
    "bat": ["bianfu", "bf"],
    "bear": ["xiong", "x"],
    "beaver": ["heli", "hl"],
    "bedbug": ["chouchong", "cc"],
    "bee": ["mifeng", "mf"],
    "beetle": ["jiachong", "jc"],
    "beluga": ["baijing", "bj"],
    "bichir": ["duoqiyu", "dqy"],
    "bird": ["niao", "n"],
    "black-snub-nosed-monkey": ["jinsihou", "jsh"],
    "bornean-rhinoceros": ["poluozhouxi", "plzx"],
    "bumblebee": ["xiongfeng", "xf"],
    "bumpy-toad": ["youchan", "yc"],
    "butterfly": ["hudie", "hd"],
    "c-elegans": ["xiuliyinzhangxianchong", "xlyzxc"],
    "caddisfly": ["shie", "se"],
    "camel": ["luotuo", "lt"],
    "cat": ["mao", "m"],
    "caterpillar": ["maomaochong", "mmc"],
    "catfish": ["nianyu", "ny"],
    "cave-lion": ["dongshi", "ds"],
    "centipede": ["wugong", "wg"],
    "cheetah": ["liebao", "lb"],
    "chicken": ["ji", "j"],
    "chihuahua": ["jiwawa", "jww"],
    "chinchilla": ["maosishu", "mss"],
    "chinese-pond-turtle": ["zhonghuacaogui", "zhcg"],
    "chinese-softshell-turtle": ["zhonghuabie", "zhb"],
    "chinese-sturgeon": ["zhonghuaxun", "zhx"],
    "cicada": ["chan", "c"],
    "climbing-perch": ["panlu", "pl"],
    "cobra": ["yanjingshe", "yjs"],
    "cockatoo": ["fengtouyingwu", "ftyw"],
    "cockroach": ["zhanglang", "zl"],
    "coelacanth": ["qiangjiyu", "qjy"],
    "color-changing-frog": ["biansewa", "bsw"],
    "comb-jelly": ["zhishuimu", "zsm"],
    "coral-reef": ["shanhujiao", "shj"],
    "cordyceps": ["dongchongxiacao", "dcxc"],
    "cow": ["niu", "n"],
    "crab": ["pangxie", "px"],
    "crayfish": ["xiaolongxia", "xlx"],
    "crested-ibis": ["zhuhuan", "zh"],
    "cricket": ["xishuai", "xs"],
    "crocodile": ["eyu", "ey"],
    "crow": ["wuya", "wy"],
    "cuckoo": ["dujuan", "dj"],
    "dairy-cow": ["nainiu", "nn"],
    "darkling-beetle": ["nibujia", "nbj"],
    "deep-sea-isopod": ["shenhaijuzuchong", "shjz"],
    "deer": ["lu", "l"],
    "desert-spider": ["shamozhu", "smz"],
    "dinosaur": ["konglong", "kl"],
    "dodo": ["duduniao", "ddn"],
    "dog": ["gou", "g"],
    "dolphin": ["haitun", "ht"],
    "donkey": ["lv", "l"],
    "dragon": ["long", "l"],
    "dragonfly": ["qingting", "qt"],
    "duck": ["yazi", "yz"],
    "dust-mite": ["chenman", "cm"],
    "eagle": ["ying", "y"],
    "earthworm": ["qiuyin", "qy"],
    "eel": ["manyu", "my"],
    "electric-eel": ["dianman", "dm"],
    "elephant": ["daxiang", "dx"],
    "emperor-penguin": ["diqie", "dqe"],
    "eurypterid": ["banzuhou", "bzh"],
    "falcon": ["lieying", "ly"],
    "ferret": ["xuediao", "xd"],
    "firefly": ["yinghuochong", "yhc"],
    "fish": ["yu", "y"],
    "fish-mascot": ["katongyu", "kty"],
    "fishing-spider": ["buyuzhu", "byz"],
    "flamingo": ["huolieniao", "hln"],
    "flea": ["tiaozao", "tz"],
    "fly": ["cangying", "cy"],
    "fly-catching-ant": ["buyingyi", "byy"],
    "flying-cat": ["feimao", "fm"],
    "fox": ["huli", "hl"],
    "frog": ["qingwa", "qw"],
    "fruit-fly": ["guoying", "gy"],
    "fulmar": ["baofenghu", "bfh"],
    "galapagos-tortoise": ["jialapagesixianggui", "jlpg"],
    "gecko": ["bihu", "bh"],
    "giant-clam": ["dachequ", "dcq"],
    "giant-jaw-ant": ["jueyi", "je"],
    "giant-salamander": ["dani", "dn"],
    "giraffe": ["changjinglu", "cjl"],
    "glass-frog": ["boliwa", "blw"],
    "glowing-firebug": ["faguangyinghuochong", "fgyhc"],
    "goat": ["shanyang", "sy"],
    "golden-pheasant": ["jinji", "jj"],
    "goldfish": ["jinyu", "jy"],
    "goose": ["e", "e"],
    "gorilla": ["daxingxing", "dxx"],
    "grasshopper": ["zhameng", "zm"],
    "grebe": ["pipi", "pp"],
    "green-haired-turtle": ["lvmaogui", "lmg"],
    "guppy": ["kongqueyu", "kqy"],
    "hammerhead-shark": ["shuangjisha", "sjs"],
    "hamster": ["cangshu", "cs"],
    "hedgehog": ["ciwei", "cw"],
    "hippo": ["hema", "hm"],
    "honey-badger": ["mihuan", "mh"],
    "hoopoe": ["daisheng", "ds"],
    "hornbill": ["xiniao", "xn"],
    "hornet": ["hufeng", "hf"],
    "horse": ["ma", "m"],
    "horseshoe-crab": ["hou", "h"],
    "huamei": ["huamei", "hm"],
    "hummingbird": ["fengniao", "fn"],
    "hummingbird-moth": ["fengniaoyinge", "fnye"],
    "hyena": ["liegou", "lg"],
    "insect": ["kunchong", "kc"],
    "jaw-worm": ["eruchong", "erc"],
    "jellyfish": ["shuimu", "sm"],
    "jerboa": ["tiaoshu", "ts"],
    "kangaroo": ["daishu", "ds"],
    "kea": ["zhuoyangyingwu", "zyyw"],
    "kingfisher": ["cuiniao", "cn"],
    "koi": ["jinli", "jl"],
    "krill": ["linxia", "lx"],
    "leech": ["shuizhi", "sz"],
    "lemming": ["lvshu", "ls"],
    "leopard-cat": ["baomao", "bm"],
    "lion": ["shizi", "sz"],
    "lizard": ["xiyi", "xy"],
    "lobster": ["longxia", "lx"],
    "long-necked-dinosaur": ["changjingkonglong", "cjkl"],
    "lungfish": ["feiyu", "fy"],
    "magpie": ["xique", "xq"],
    "maine-coon": ["mianyinmao", "mym"],
    "mammoth": ["mengmaxiang", "mmx"],
    "manatee": ["hainiu", "hn"],
    "mandarin-fish": ["guiyu", "gy"],
    "mangrove-finch": ["hongshulinshuque", "hslsq"],
    "manta-ray": ["fufen", "ff"],
    "mantis-fly": ["tangling", "tl"],
    "mantis-shrimp": ["tanglangxia", "tlx"],
    "marbled-cat": ["shiwenmao", "swm"],
    "marmoset": ["ronghou", "rh"],
    "marmot": ["tuboshu", "tbs"],
    "mermaid": ["meirenyu", "mry"],
    "migratory-bird": ["houniao", "hn"],
    "monkey": ["houzi", "hz"],
    "mosasaurus": ["canglong", "cl"],
    "mosquito": ["wenzi", "wz"],
    "moth": ["ezi", "ez"],
    "mouse": ["laoshu", "ls"],
    "mudskipper": ["tantuyu", "tty"],
    "mussel": ["yibei", "yb"],
    "naked-mole-rat": ["luoyanshu", "lys"],
    "narwhal": ["dujiaojing", "djj"],
    "nautilus": ["yingwuluo", "ywl"],
    "ocean-sunfish": ["fancheyu", "fcy"],
    "octopus": ["zhangyu", "zy"],
    "opossum": ["fushu", "fs"],
    "orca": ["hujing", "hj"],
    "oriole": ["huangli", "hl"],
    "ostrich": ["tuoniao", "tn"],
    "otter": ["shuita", "st"],
    "owl": ["maotouying", "mty"],
    "oyster": ["muli", "ml"],
    "pacific-saury": ["qiudaoyu", "qdy"],
    "panda": ["xiongmao", "xiong", "xm"],
    "pangolin": ["chuanshanjia", "csj"],
    "paradoxical-frog": ["qiyiwa", "qyw"],
    "parasitoid-wasp": ["jishengfeng", "jsf"],
    "parrot": ["yingwu", "yw"],
    "parrotfish": ["yingzuiyu", "yzy"],
    "peacock-spider": ["kongquetiaozhu", "kqtz"],
    "pelican": ["tihu", "th"],
    "penguin": ["qie", "qe"],
    "pig": ["zhu", "z"],
    "pigeon": ["gezi", "gz"],
    "pika": ["shutu", "st"],
    "piranha": ["shirenyu", "sry"],
    "pistol-shrimp": ["guxia", "gx"],
    "platypus": ["yazuishou", "yzs"],
    "plesiosaur": ["shejinglong", "sjl"],
    "plump-bird": ["pangniao", "pn"],
    "pocket-shark": ["koudaisha", "kds"],
    "polar-bear": ["beijixiong", "bjx"],
    "porcupine": ["haozhu", "hz"],
    "prehistoric-primate": ["shiqianlingzhanglei", "sqlzl"],
    "pterosaur": ["yilong", "yl"],
    "pufferfish": ["hetun", "ht"],
    "rabbit": ["tuzi", "tz"],
    "raccoon": ["huanxiong", "hx"],
    "raccoon-dog": ["hezi", "hz"],
    "rattlesnake": ["xiangweishe", "xws"],
    "red-panda": ["xiaoxiongmao", "xxm"],
    "reed-parrotbill": ["zhendanyaque", "zdya"],
    "reindeer": ["xunlu", "xl"],
    "rhinoceros": ["xiniu", "xn"],
    "ribbon-winged-lacewing": ["sichicaoling", "scl"],
    "ribbon-worm": ["niuchong", "nc"],
    "rice-planthopper": ["daofeishi", "dfs"],
    "ring-tailed-lemur": ["huanweihuhou", "hwhh"],
    "rooster": ["gongji", "gj"],
    "rose-tarantula": ["meiguibuniaozhu", "mgbnz"],
    "saiga": ["gaobilingyang", "gbly"],
    "salamander": ["rongyuan", "ry"],
    "salmon": ["guiyu", "gy"],
    "sand-cat": ["shamao", "sm"],
    "sawfish": ["juyao", "jy"],
    "scallop": ["shanbei", "sb"],
    "scaly-foot-snail": ["linzuluo", "lzl"],
    "schistosome": ["xuexichong", "xxc"],
    "scorpion": ["xiezi", "xz"],
    "sea-cucumber": ["haishen", "hs"],
    "sea-hare": ["haitu", "ht"],
    "sea-lion": ["haishi", "hs"],
    "sea-otter": ["haita", "ht"],
    "sea-slug": ["haikuoyu", "hky"],
    "sea-turtle": ["haigui", "hg"],
    "seabird": ["hainiao", "hn"],
    "seagull": ["haiou", "ho"],
    "seahorse": ["haima", "hm"],
    "seal": ["haibao", "hb"],
    "shark": ["shayu", "sy"],
    "sheep": ["mianyang", "my"],
    "shell-creature": ["geli", "gl"],
    "shrimp": ["xia", "x"],
    "shy-bird": ["xiuqueniao", "xqn"],
    "sichuan-bush-warbler": ["sichuanshuying", "scsy"],
    "silkworm": ["can", "c"],
    "sloth": ["shulan", "sl"],
    "slug": ["kuoyu", "ky"],
    "snail": ["woniu", "wn"],
    "snail-shell": ["luo", "l"],
    "snake": ["she", "s"],
    "snow-leopard": ["xuebao", "xb"],
    "softshell-turtle": ["bie", "b"],
    "solenodon": ["gouchiqu", "gcq"],
    "sparrow": ["maque", "mq"],
    "spectacled-bear": ["yanjingxiong", "yjx"],
    "sperm-whale": ["moxiangjing", "mxj"],
    "spider": ["zhizhu", "zz"],
    "spider-crab": ["zhizhuxie", "zzx"],
    "spiny-lizard": ["cilizi", "clx"],
    "sponge": ["haimian", "hm"],
    "squid": ["youyu", "yy"],
    "squirrel": ["songshu", "ss"],
    "starfish": ["haixing", "hx"],
    "starling": ["liangniao", "ln"],
    "stink-bug": ["chunxiang", "cx"],
    "swallow": ["yanzi", "yz"],
    "tadpole": ["kedou", "kd"],
    "takin": ["lingniu", "ln"],
    "tapir": ["mo", "m"],
    "tardigrade": ["shuixiongchong", "sxc"],
    "termite": ["baiyi", "by"],
    "tick": ["pichong", "pc"],
    "tiger": ["laohu", "lh"],
    "toad": ["chanchu", "cc"],
    "totoro": ["longmao", "lm"],
    "toxoplasma": ["gongxingchong", "gxc"],
    "transparent-fish": ["toumingyu", "tmy"],
    "trilobite": ["sanyechong", "syc"],
    "turkey": ["huaji", "hj"],
    "turtle": ["wugui", "wg"],
    "tyrannosaurus": ["bawanglong", "bwl"],
    "urmia-gull": ["yiou", "yo"],
    "vampire-bat": ["xixuefu", "xxf"],
    "viscacha": ["shanrongshu", "srs"],
    "vulture": ["tujiu", "tj"],
    "walrus": ["haixiang", "hx"],
    "warthog": ["youzhu", "yz"],
    "water-buffalo": ["shuiniu", "sn"],
    "whale": ["jingyu", "jy"],
    "whale-shark": ["jingsha", "js"],
    "wild-boar": ["yezhu", "yz"],
    "wildcat": ["yemao", "ym"],
    "wolf": ["lang", "l"],
    "wolfdog": ["langgou", "lg"],
    "wood-cockroach": ["mulian", "ml"],
    "woodpecker": ["zhuomuniao", "zmn"],
    "worm": ["ruanchong", "rc"],
    "yak": ["maoniu", "mn"],
    "yangtze-giant-softshell": ["banbie", "bb"],
    "yellow-breasted-bunting": ["huangxiongwu", "hxw"],
    "zebra": ["banma", "bm"],
    "zebra-finch": ["banxiongcaoque", "bxcq"],
    "zebrafish": ["banmayu", "bmy"],
}

# BEGIN ALIAS_PINYIN（由 scripts/build-pinyin.py 生成，请勿手改）
ALIAS_PINYIN = {
    "一角鲸": ["yijiaojing", "yjj"],
    "三文鱼": ["sanwenyu", "swy"],
    "中国龙": ["zhongguolong", "zgl"],
    "仰鼻猴": ["yangbihou", "ybh"],
    "兔": ["tu", "t"],
    "八爪鱼": ["bazhaoyu", "bzy"],
    "喷水鱼": ["penshuiyu", "psy"],
    "四脚蛇": ["sijiaoshe", "sjs"],
    "土狼": ["tulang", "tl"],
    "地龙": ["dilong", "dl"],
    "夜猫子": ["yemaozi", "ymz"],
    "大熊猫": ["daxiongmao", "dxm"],
    "大闸蟹": ["dazhaxie", "dzx"],
    "大黄蜂": ["dahuangfeng", "dhf"],
    "娃娃鱼": ["wawayu", "wwy"],
    "婆罗洲犀牛": ["poluozhouxiniu", "plzxn"],
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
    "布谷鸟": ["buguniao", "bgn"],
    "平头哥": ["pingtouge", "ptg"],
    "床虱": ["chuangshi", "cs"],
    "弓形体": ["gongxingti", "gxt"],
    "强棱蜥": ["qianglengxi", "qlx"],
    "托托罗": ["tuotuoluo", "ttl"],
    "扬子鳖": ["yangzibie", "yzb"],
    "扭角羚": ["niujiaoling", "njl"],
    "斑马雀": ["banmaque", "bmq"],
    "旱獭": ["hanta", "ht"],
    "暴龙": ["baolong", "bl"],
    "朱鹭": ["zhulu", "zl"],
    "杀人鲸": ["sharenjing", "srj"],
    "树獭": ["shuta", "st"],
    "栗鼠": ["lishu", "ls"],
    "桂花鱼": ["guihuayu", "ghy"],
    "母鸡": ["muji", "mj"],
    "毛虫": ["maochong", "mc"],
    "毛驴": ["maolv", "ml"],
    "水虎鱼": ["shuihuyu", "shy"],
    "河鲀": ["hetun", "ht"],
    "海兔": ["haitu", "ht"],
    "海狸": ["haili", "hl"],
    "海獭": ["haita", "ht"],
    "海蜇": ["haizhe", "hz"],
    "海蝎": ["haixie", "hx"],
    "海龟": ["haigui", "hg"],
    "淡菜": ["dancai", "dc"],
    "熊": ["xiong", "x"],
    "犬": ["quan", "q"],
    "狮": ["shi", "s"],
    "狼": ["lang", "l"],
    "狼犬": ["langquan", "lq"],
    "猩猩": ["xingxing", "xx"],
    "猫咪": ["maomi", "mm"],
    "猫熊": ["maoxiong", "mx"],
    "猴": ["hou", "h"],
    "獭": ["ta", "t"],
    "生蚝": ["shenghao", "sh"],
    "田螺": ["tianluo", "tl"],
    "田鸡": ["tianji", "tj"],
    "甲鱼": ["jiayu", "jy"],
    "癞蛤蟆": ["laihama", "lhm"],
    "白熊": ["baixiong", "bx"],
    "白鸽": ["baige", "bg"],
    "百足虫": ["baizuchong", "bzc"],
    "皮皮虾": ["pipixia", "ppx"],
    "知了": ["zhiliao", "zl"],
    "砗磲": ["chequ", "cq"],
    "管鼻鹱": ["guanbihu", "gbh"],
    "类人猿": ["leirenyuan", "lry"],
    "红熊猫": ["hongxiongmao", "hxm"],
    "红腹锦鸡": ["hongfujinji", "hfjj"],
    "线虫": ["xianchong", "xc"],
    "绢毛猴": ["juanmaohou", "jmh"],
    "绿海龟": ["lvhaigui", "lhg"],
    "缓步动物": ["huanbudongwu", "hbdw"],
    "羊": ["yang", "y"],
    "老鸹": ["laogua", "lg"],
    "腻虫": ["nichong", "nc"],
    "臭大姐": ["choudajie", "cdj"],
    "虎": ["hu", "h"],
    "虫草": ["chongcao", "cc"],
    "蚂蚱": ["mazha", "mz"],
    "蚂蟥": ["mahuang", "mh"],
    "蚕宝宝": ["canbaobao", "cbb"],
    "蛐蛐": ["ququ", "qq"],
    "蛙": ["wa", "w"],
    "蜂鸟蛾": ["fengniaoe", "fne"],
    "蜱": ["pi", "p"],
    "蝇": ["ying", "y"],
    "蝶": ["die", "d"],
    "蟒蛇": ["mangshe", "ms"],
    "蟹": ["xie", "x"],
    "豆豆龙": ["doudoulong", "ddl"],
    "象": ["xiang", "x"],
    "貉子": ["haozi", "hz"],
    "贝壳": ["beike", "bk"],
    "赛加羚羊": ["saijialingyang", "sjly"],
    "跳跳鱼": ["tiaotiaoyu", "tty"],
    "金龙鱼": ["jinlongyu", "jly"],
    "锤头鲨": ["chuitousha", "cts"],
    "长毛象": ["changmaoxiang", "cmx"],
    "隼": ["sun", "s"],
    "雄鸡": ["xiongji", "xj"],
    "霸王龙": ["bawanglong", "bwl"],
    "飞蛾": ["feie", "fe"],
    "马蜂": ["mafeng", "mf"],
    "马蹄蟹": ["matixie", "mtx"],
    "骏马": ["junma", "jm"],
    "魔鬼鱼": ["moguiyu", "mgy"],
    "鱼狗": ["yugou", "yg"],
    "鲟鱼": ["xunyu", "xy"],
    "鲨": ["sha", "s"],
    "鲮鲤": ["lingli", "ll"],
    "鲸": ["jing", "j"],
    "鳄": ["e", "e"],
    "鸦雀": ["yaque", "yq"],
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
  .selbar { flex-wrap: wrap; justify-content: center; max-width: calc(100vw - 40px); }
  .pager button.ghost { margin-left: 10px; }
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

  .side-sec { margin-top: 13px; }
  .side-label {
    font-size: 10.5px; color: var(--muted); margin-bottom: 6px;
    letter-spacing: .04em; text-transform: uppercase;
  }
  .chips { display: flex; gap: 7px; flex-wrap: wrap; align-items: center; }
  .chip {
    width: 21px; height: 21px; border-radius: 50%; padding: 0; flex: none;
    border: 1px solid var(--line); cursor: pointer; background: #fff;
  }
  .chip.on { box-shadow: 0 0 0 2px var(--surface), 0 0 0 3.5px var(--accent); }
  input.chip { -webkit-appearance: none; appearance: none; overflow: hidden; }
  input.chip::-webkit-color-swatch-wrapper { padding: 0; }
  input.chip::-webkit-color-swatch { border: none; }
  .pill {
    font-size: 11.5px; padding: 3px 9px; border-radius: 999px;
    border: 1px solid var(--line); background: var(--surface); cursor: pointer;
  }
  .pill.on { background: var(--accent); border-color: var(--accent); color: #fff; }
  .preview.dark { background: #17170f; }
  .preview.checker {
    background-image:
      linear-gradient(45deg, #e8e8e2 25%, transparent 25%),
      linear-gradient(-45deg, #e8e8e2 25%, transparent 25%),
      linear-gradient(45deg, transparent 75%, #e8e8e2 75%),
      linear-gradient(-45deg, transparent 75%, #e8e8e2 75%);
    background-size: 14px 14px;
    background-position: 0 0, 0 7px, 7px -7px, -7px 0;
  }
  .glyph { flex: none; }
  .glyph img { width: 100%; height: 100%; display: block; }
  .ladder { display: flex; align-items: flex-end; gap: 13px; padding: 4px 0 0; }
  .ladder figure { margin: 0; text-align: center; }
  .ladder img { display: block; margin: 0 auto 3px; }
  .ladder figcaption { font-size: 9.5px; color: var(--muted); font-family: var(--mono); }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 7px; }
  .grid2 button { font-size: 12px; padding: 6px 6px; }
  .pngrow { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }
  .pngrow button { font-size: 11.5px; padding: 5px 0; }
  .hint { font-size: 10.5px; color: var(--muted); line-height: 1.65; margin-top: 7px; }

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
      <button id="selectpage" type="button" class="ghost">全选本页</button>
      <span class="info" id="pageinfo"></span>
    </nav>
  </main>
  <aside class="empty" id="aside">点击任意图标查看详情</aside>
</div>

<div class="selbar" id="selbar">
  <span>已选 <span class="n" id="selcount">0</span> 个</span>
  <button id="copyall">复制全部路径</button>
  <button id="zipall">下载 ZIP</button>
  <button id="csvall">清单 CSV</button>
  <button id="jsonall">清单 JSON</button>
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

/* ---------- 单品操作：下载 / 源码 / 着色 / 尺寸 / 导出 ---------- */

const TONES = [
  { id: 'black', color: '#111111', label: '黑' },
  { id: 'white', color: '#ffffff', label: '白' },
  { id: 'accent', color: '#2f6f4e', label: '主题绿' }
];
const SURFACES = [
  { id: 'light', label: '浅底' },
  { id: 'dark', label: '深底' },
  { id: 'checker', label: '透明格' }
];
const PNG_SIZES = [64, 128, 256, 512];

const remote = location.protocol !== 'file:';
const svgCache = new Map();
let toneId = 'black';
let toneColor = TONES[0].color;
let surfaceId = 'light';

function toneValue() {
  const hit = TONES.find((t) => t.id === toneId);
  return hit ? hit.color : toneColor;
}

function maskDecl(path, color) {
  const u = 'url("' + path + '") center / contain no-repeat';
  return 'background:' + color + ';-webkit-mask:' + u + ';mask:' + u + ';';
}

function glyph(v, size) {
  const box = document.createElement('div');
  box.className = 'glyph';
  box.style.width = size + 'px';
  box.style.height = size + 'px';
  if (remote) {
    box.style.cssText += maskDecl(v.path, toneValue());
  } else {
    // 本地打开时 mask 不会加载，退化为原图 + 反色
    const img = document.createElement('img');
    img.src = v.path;
    img.alt = v.name;
    if (toneId === 'white') img.style.filter = 'invert(1)';
    box.appendChild(img);
  }
  return box;
}

function basename(p) {
  const f = p.split('/').pop();
  return f.endsWith('.svg') ? f.slice(0, -4) : f;
}

function triggerDownload(url, name) {
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  a.rel = 'noopener';
  document.body.appendChild(a);
  a.click();
  a.remove();
}

function downloadSvg(v) {
  triggerDownload(v.path, basename(v.path) + '.svg');
  toast('已下载 ' + basename(v.path) + '.svg');
}

async function loadSvg(v) {
  if (svgCache.has(v.path)) return svgCache.get(v.path);
  const res = await fetch(v.path);
  if (!res.ok) throw new Error('HTTP ' + res.status);
  const text = await res.text();
  svgCache.set(v.path, text);
  return text;
}

function needRemote(why) {
  if (remote) return true;
  toast(why);
  return false;
}

async function copySource(v) {
  if (!needRemote('本地双击打开无法读取源码，请用线上站点')) return;
  try {
    const text = await loadSvg(v);
    await copy(text, '已复制 SVG 源码（' + text.length + ' 字符）');
  } catch (e) {
    toast('读取失败：' + e.message);
  }
}

async function copyDataUri(v) {
  if (!needRemote('本地双击打开无法生成 data URI，请用线上站点')) return;
  try {
    const uri = 'data:image/svg+xml,' + encodeURIComponent(await loadSvg(v));
    await copy(uri, '已复制 data URI（' + (uri.length / 1024).toFixed(1) + ' KB）');
  } catch (e) {
    toast('读取失败：' + e.message);
  }
}

function maskSnippet(v) {
  const u = 'url(' + v.path + ') center / contain no-repeat';
  return `.icon {
  display: inline-block;
  width: 1em;
  height: 1em;
  background: currentColor;
  -webkit-mask: ${u};
  mask: ${u};
}`;
}

function copyMask(v) {
  copy(maskSnippet(v), '已复制 mask 片段');
}

function componentName(v) {
  return 'Icon' + basename(v.path).split('-')
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join('');
}

function spriteRef(v) {
  const dir = v.path.split('/')[1];
  return 'dist/sprites/' + dir + '.svg#' + basename(v.path);
}

function useSnippet(v) {
  return '<svg class="icon" aria-hidden="true"><use href="' + spriteRef(v) + '"/></svg>';
}

// 当前动物的全部变体，用来一次性复制整组
function groupVariants(v) {
  const dir = v.path.split('/')[1];
  const animal = DATA.filter((a) => a.variants.some((x) => x.path.split('/')[1] === dir))[0];
  return animal ? animal.variants : [v];
}

function groupSnippet(v) {
  return groupVariants(v).map(useSnippet).join(String.fromCharCode(10));
}

function reactSnippet(v) {
  const u = 'url(/' + v.path + ') center / contain no-repeat';
  return `export function ${componentName(v)}({ size = 24, className = "", ...rest }) {
  return (
    <span
      {...rest}
      className={className}
      style={{
        display: "inline-block",
        width: size,
        height: size,
        backgroundColor: "currentColor",
        WebkitMask: "${u}",
        mask: "${u}",
      }}
    />
  );
}`;
}

function vueSnippet(v) {
  const u = 'url(/' + v.path + ') center / contain no-repeat';
  const endTag = '</' + 'script>';
  return `<template>
  <span class="icon" :style="{ width: size + 'px', height: size + 'px' }" />
</template>

<script setup>
defineProps({ size: { type: Number, default: 24 } });
${endTag}

<style scoped>
.icon {
  display: inline-block;
  background: currentColor;
  -webkit-mask: ${u};
  mask: ${u};
}
</style>`;
}

async function exportPng(v, size) {
  try {
    const img = new Image();
    img.src = v.path;
    await img.decode();
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');
    // SVG 有 viewBox 且默认 preserveAspectRatio=meet，画进方框会等比留白，不拉伸
    ctx.drawImage(img, 0, 0, size, size);
    const blob = await new Promise((res, rej) => {
      canvas.toBlob((b) => (b ? res(b) : rej(new Error('canvas 为空'))), 'image/png');
    });
    const url = URL.createObjectURL(blob);
    triggerDownload(url, basename(v.path) + '@' + size + '.png');
    setTimeout(() => URL.revokeObjectURL(url), 6000);
    toast('已导出 ' + size + '×' + size + ' PNG');
  } catch (e) {
    toast(remote ? '导出失败：' + e.message : '本地双击打开无法导出 PNG，请用线上站点');
  }
}

function renderAside(v) {
  aside.className = '';
  aside.innerHTML = '';

  const preview = el('div', 'preview' + (surfaceId === 'dark' ? ' dark' : surfaceId === 'checker' ? ' checker' : ''));
  preview.appendChild(glyph(v, 132));
  aside.appendChild(preview);

  const secColor = el('div', 'side-sec');
  secColor.appendChild(el('div', 'side-label', '前景色'));
  const chips = el('div', 'chips');
  for (const t of TONES) {
    const b = el('button', 'chip' + (t.id === toneId ? ' on' : ''));
    b.type = 'button';
    b.style.background = t.color;
    const disabled = !remote && t.id !== 'black' && t.id !== 'white';
    b.disabled = disabled;
    b.title = disabled ? t.label + '（本地打开不可用）' : t.label;
    b.addEventListener('click', () => {
      toneId = t.id;
      toneColor = t.color;
      renderAside(v);
    });
    chips.appendChild(b);
  }
  const custom = el('input', 'chip' + (toneId === 'custom' ? ' on' : ''));
  custom.type = 'color';
  custom.value = toneId === 'custom' ? toneColor : '#7a7a72';
  custom.title = remote ? '自定义颜色' : '自定义颜色（本地打开不可用）';
  custom.disabled = !remote;
  custom.addEventListener('input', () => {
    toneId = 'custom';
    toneColor = custom.value;
    renderAside(v);
  });
  chips.appendChild(custom);
  secColor.appendChild(chips);

  const surfaces = el('div', 'chips');
  surfaces.style.marginTop = '7px';
  for (const s of SURFACES) {
    const b = el('button', 'pill' + (s.id === surfaceId ? ' on' : ''));
    b.type = 'button';
    b.textContent = s.label;
    b.addEventListener('click', () => {
      surfaceId = s.id;
      renderAside(v);
    });
    surfaces.appendChild(b);
  }
  secColor.appendChild(surfaces);
  aside.appendChild(secColor);

  const secSize = el('div', 'side-sec');
  secSize.appendChild(el('div', 'side-label', '尺寸预览'));
  const ladder = el('div', 'ladder');
  for (const s of [16, 24, 32, 48, 64]) {
    const fig = document.createElement('figure');
    const im = document.createElement('img');
    im.src = v.path;
    im.alt = v.name;
    im.width = s;
    im.height = s;
    const cap = document.createElement('figcaption');
    cap.textContent = s;
    fig.appendChild(im);
    fig.appendChild(cap);
    ladder.appendChild(fig);
  }
  secSize.appendChild(ladder);
  aside.appendChild(secSize);

  const meta = el('div', 'meta');
  meta.style.marginTop = '12px';
  meta.innerHTML =
    '<div><span class="k">名称 </span>' + v.zh + '（' + v.name + '）</div>' +
    '<div><span class="k">序号 </span>' + v.index + '</div>' +
    '<div><span class="k">路径 </span>' + v.path + '</div>';
  aside.appendChild(meta);

  const secAct = el('div', 'side-sec');
  secAct.appendChild(el('div', 'side-label', '复制 / 下载'));
  const grid = el('div', 'grid2');
  const addBtn = (text, fn, disabled, title) => {
    const b = el('button', '');
    b.type = 'button';
    b.textContent = text;
    if (disabled) {
      b.disabled = true;
      b.title = title || '';
    }
    b.addEventListener('click', fn);
    grid.appendChild(b);
  };
  addBtn('复制路径', () => copy(v.path, '已复制路径'));
  addBtn('复制 img 标签', () => copy('<img src="' + v.path + '" alt="' + v.name + '">', '已复制 img 标签'));
  addBtn('复制 <use> 片段', () => copy(useSnippet(v), '已复制 <use> 片段'));
  addBtn('复制 sprite 引用', () => copy(spriteRef(v), '已复制 sprite 引用'));
  addBtn('复制整组 <use>', () => copy(groupSnippet(v), '已复制整组 ' + groupVariants(v).length + ' 个 <use> 片段'));
  addBtn('下载 SVG', () => downloadSvg(v));
  addBtn('下载整组 SVG', () => downloadGroupSvg(v), !remote, '本地打开不可用，请用线上站点');
  addBtn('复制源码', () => copySource(v), !remote, '本地打开不可用，请用线上站点');
  addBtn('mask 片段', () => copyMask(v));
  addBtn('data URI', () => copyDataUri(v), !remote, '本地打开不可用，请用线上站点');
  addBtn('React', () => copy(reactSnippet(v), '已复制 React 组件'));
  addBtn('Vue', () => copy(vueSnippet(v), '已复制 Vue 组件'));
  secAct.appendChild(grid);
  if (!remote) {
    secAct.appendChild(el('div', 'hint', '本地双击打开时浏览器不允许跨文件 <use> 引用，sprite 片段请用线上站点或本地起服务预览。'));
  }
  aside.appendChild(secAct);

  const secPng = el('div', 'side-sec');
  secPng.appendChild(el('div', 'side-label', '导出 PNG'));
  const prow = el('div', 'pngrow');
  for (const s of PNG_SIZES) {
    const b = el('button', '');
    b.type = 'button';
    b.textContent = s;
    b.title = '导出 ' + s + '×' + s + ' 透明 PNG';
    b.addEventListener('click', () => exportPng(v, s));
    prow.appendChild(b);
  }
  secPng.appendChild(prow);
  if (!remote) {
    secPng.appendChild(el('div', 'hint', '本地双击打开时浏览器会阻止 canvas 导出，请用线上站点。'));
  }
  aside.appendChild(secPng);
}

function renderSelbar() {
  selcount.textContent = selected.size;
  selbar.classList.toggle('show', selected.size > 0);
  if (typeof syncSelectPage === 'function') syncSelectPage();
}

/* ---------- 批量操作：全选本页 / ZIP / 清单 ---------- */

const META = new Map();
for (const animal of DATA) for (const v of animal.variants) META.set(v.path, Object.assign({ animal: animal.name }, v));

function selectPageBtn() {
  return document.getElementById('selectpage');
}

function pageTiles() {
  return [...grid.querySelectorAll('.card:not(.hidden) .tile')];
}

function syncSelectPage() {
  const btn = selectPageBtn();
  if (!btn) return;
  const paths = pageTiles().map((t) => t.dataset.path);
  const all = paths.length > 0 && paths.every((p) => selected.has(p));
  btn.textContent = all ? '取消本页' : '全选本页';
  btn.classList.toggle('active', all);
}

selectPageBtn().addEventListener('click', () => {
  const tiles = pageTiles();
  const paths = tiles.map((t) => t.dataset.path);
  const all = paths.length > 0 && paths.every((p) => selected.has(p));
  for (const t of tiles) {
    const p = t.dataset.path;
    if (all) {
      selected.delete(p);
      t.classList.remove('selected');
    } else {
      selected.add(p);
      t.classList.add('selected');
    }
  }
  renderSelbar();
  toast((all ? '已取消本页 ' : '已选中本页 ') + paths.length + ' 个图标');
});

/* CRC32 与最小 ZIP 写入：store 与 deflate 两种方式，不依赖第三方库 */

const CRC_TABLE = new Uint32Array(256).map((_, n) => {
  let c = n;
  for (let k = 0; k < 8; k += 1) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  return c >>> 0;
});

function crc32(bytes) {
  let c = 0xffffffff;
  for (let i = 0; i < bytes.length; i += 1) c = CRC_TABLE[(c ^ bytes[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

async function deflateRaw(bytes) {
  if (typeof CompressionStream === 'undefined') return null;
  const stream = new Blob([bytes]).stream().pipeThrough(new CompressionStream('deflate-raw'));
  return new Uint8Array(await new Response(stream).arrayBuffer());
}

function dosStamp(d) {
  const time = ((d.getHours() << 11) | (d.getMinutes() << 5) | ((d.getSeconds() / 2) | 0)) & 0xffff;
  const date = (((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate()) & 0xffff;
  return { time, date };
}

async function makeZip(files) {
  const enc = new TextEncoder();
  const { time, date } = dosStamp(new Date());
  const chunks = [];
  const central = [];
  let offset = 0;

  for (const f of files) {
    const nameBytes = enc.encode(f.name);
    const raw = f.data;
    const crc = crc32(raw);
    let body = await deflateRaw(raw);
    let method = 8;
    if (!body || body.length >= raw.length) {
      body = raw;
      method = 0;
    }

    const local = new Uint8Array(30 + nameBytes.length);
    const lv = new DataView(local.buffer);
    lv.setUint32(0, 0x04034b50, true);
    lv.setUint16(4, 20, true);
    lv.setUint16(6, 0x0800, true);
    lv.setUint16(8, method, true);
    lv.setUint16(10, time, true);
    lv.setUint16(12, date, true);
    lv.setUint32(14, crc, true);
    lv.setUint32(18, body.length, true);
    lv.setUint32(22, raw.length, true);
    lv.setUint16(26, nameBytes.length, true);
    lv.setUint16(28, 0, true);
    local.set(nameBytes, 30);

    const cen = new Uint8Array(46 + nameBytes.length);
    const cv = new DataView(cen.buffer);
    cv.setUint32(0, 0x02014b50, true);
    cv.setUint16(4, 20, true);
    cv.setUint16(6, 20, true);
    cv.setUint16(8, 0x0800, true);
    cv.setUint16(10, method, true);
    cv.setUint16(12, time, true);
    cv.setUint16(14, date, true);
    cv.setUint32(16, crc, true);
    cv.setUint32(20, body.length, true);
    cv.setUint32(24, raw.length, true);
    cv.setUint16(28, nameBytes.length, true);
    cv.setUint32(42, offset, true);
    cen.set(nameBytes, 46);

    chunks.push(local, body);
    central.push(cen);
    offset += local.length + body.length;
  }

  const centralSize = central.reduce((n, c) => n + c.length, 0);
  const eocd = new Uint8Array(22);
  const ev = new DataView(eocd.buffer);
  ev.setUint32(0, 0x06054b50, true);
  ev.setUint16(8, files.length, true);
  ev.setUint16(10, files.length, true);
  ev.setUint32(12, centralSize, true);
  ev.setUint32(16, offset, true);
  return new Blob([...chunks, ...central, eocd], { type: 'application/zip' });
}

function manifestRows() {
  return [...selected].sort().map((p) => META.get(p)).filter(Boolean);
}

async function mapLimit(items, limit, fn) {
  const out = new Array(items.length);
  let next = 0;
  const worker = async () => {
    while (next < items.length) {
      const i = next;
      next += 1;
      out[i] = await fn(items[i], i);
    }
  };
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return out;
}

async function downloadGroupSvg(v) {
  if (!needRemote('本地双击打开无法读取 SVG，请用线上站点下载整组')) return;
  const dir = v.path.split('/')[1];
  const list = groupVariants(v);
  toast('打包中 0 / ' + list.length);

  let done = 0;
  try {
    const entries = await mapLimit(list, 10, async (x) => {
      const res = await fetch(x.path);
      if (!res.ok) throw new Error(x.path + ' 读取失败（HTTP ' + res.status + '）');
      const bytes = new Uint8Array(await res.arrayBuffer());
      done += 1;
      toast('打包中 ' + done + ' / ' + list.length);
      return { name: basename(x.path) + '.svg', data: bytes };
    });

    const blob = await makeZip(entries);
    const url = URL.createObjectURL(blob);
    triggerDownload(url, dir + '-svg-' + list.length + '.zip');
    toast('已下载整组 ' + list.length + ' 个 SVG');
    setTimeout(() => URL.revokeObjectURL(url), 10000);
  } catch (err) {
    toast('打包失败：' + err.message);
  }
}

async function downloadZip() {
  if (!needRemote('本地双击打开无法读取 SVG，请用线上站点打包')) return;
  const paths = [...selected].sort();
  if (paths.length === 0) return toast('还没有选中图标');

  toast('打包中 0 / ' + paths.length);
  let done = 0;
  try {
    const entries = await mapLimit(paths, 10, async (path) => {
      const res = await fetch(path);
      if (!res.ok) throw new Error(path + ' 读取失败（HTTP ' + res.status + '）');
      const bytes = new Uint8Array(await res.arrayBuffer());
      done += 1;
      if (done % 12 === 0 || done === paths.length) toast('打包中 ' + done + ' / ' + paths.length);
      return { name: basename(path) + '.svg', data: bytes };
    });

    const manifest = manifestRows().map((v) => ({ zh: v.zh, animal: v.animal, file: v.name, index: v.index, path: v.path }));
    entries.push({ name: 'manifest.json', data: new TextEncoder().encode(JSON.stringify(manifest, null, 2) + '\\n') });

    const blob = await makeZip(entries);
    const url = URL.createObjectURL(blob);
    triggerDownload(url, 'animals-' + paths.length + '.zip');
    setTimeout(() => URL.revokeObjectURL(url), 5000);
    toast('已打包 ' + paths.length + ' 个图标，' + Math.round(blob.size / 1024) + ' KB');
  } catch (err) {
    toast('打包失败：' + err.message);
  }
}

function csvCell(value) {
  const s = String(value == null ? '' : value);
  return /[",\\n]/.test(s) ? '"' + s.split('"').join('""') + '"' : s;
}

function downloadManifest(kind) {
  const rows = manifestRows();
  if (rows.length === 0) return toast('还没有选中图标');

  let blob;
  let name;
  if (kind === 'csv') {
    const lines = ['中文名,目录名,文件名,序号,路径'].concat(
      rows.map((v) => [v.zh, v.animal, v.name, v.index, v.path].map(csvCell).join(','))
    );
    blob = new Blob(['\\ufeff' + lines.join('\\n') + '\\n'], { type: 'text/csv;charset=utf-8' });
    name = 'animals-' + rows.length + '.csv';
  } else {
    const data = rows.map((v) => ({ zh: v.zh, animal: v.animal, file: v.name, index: v.index, path: v.path }));
    blob = new Blob([JSON.stringify(data, null, 2) + '\\n'], { type: 'application/json' });
    name = 'animals-' + rows.length + '.json';
  }

  const url = URL.createObjectURL(blob);
  triggerDownload(url, name);
  setTimeout(() => URL.revokeObjectURL(url), 5000);
  toast('已导出 ' + name);
}

document.getElementById('zipall').addEventListener('click', downloadZip);
document.getElementById('csvall').addEventListener('click', () => downloadManifest('csv'));
document.getElementById('jsonall').addEventListener('click', () => downloadManifest('json'));

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
  if (typeof syncSelectPage === 'function') syncSelectPage();
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

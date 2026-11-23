# animals

[![校验](https://github.com/IAmKings/animals/actions/workflows/check.yml/badge.svg)](https://github.com/IAmKings/animals/actions/workflows/check.yml)

单色线条动物图标库：**246 种动物、1902 个图标**。189 种各 6 个变体；`ant`、`antelope`、`aphid`、`bee`、`caterpillar`、`catfish`、`chicken`、`coral-reef`、`cricket`、`deer`、`eagle`、`elephant`、`flea`、`frog`、`gorilla`、`hammerhead-shark`、`kingfisher`、`leech`、`lizard`、`lobster`、`lungfish`、`mammoth`、`monkey`、`ocean-sunfish`、`opossum`、`orca`、`otter`、`parrot`、`penguin`、`pigeon`、`red-panda`、`reindeer`、`rhinoceros`、`sea-turtle`、`seagull`、`sheep`、`snake`、`spider`、`spiny-lizard`、`squid`、`tardigrade`、`tiger`、`toad`、`turtle`、`tyrannosaurus`、`wildcat` 各 12 个；`ape`、`beetle`、`bird`、`butterfly`、`centipede`、`cicada`、`giant-clam`、`jellyfish` 各 18 个；`bear`、`dog`、`whale` 各 24 个。SVG 是唯一源文件，另附一个可搜索的浏览页，发布在 <https://iamkings.github.io/animals/>。

## 快速开始

```bash
git clone https://github.com/IAmKings/animals.git
cd animals
bash scripts/setup.sh     # 启用中文提交校验钩子，只需一次
open index.html           # 本地浏览
```

`setup.sh` 会启用钩子、自检钩子是否真的生效、校验素材组织、检查 PNG 渲染器，最后打印一份汇总。重复执行安全。

## 目录结构

```
animals/
├── icons/                 图标源文件
│   ├── index.json         展示顺序（目录名数组）
│   └── cat/
│       ├── cat-01.svg
│       └── ...
├── scripts/               校验与生成脚本
├── .githooks/             版本化钩子
├── .github/workflows/     CI 与站点发布
├── index.html             浏览页（生成物，随仓库提交）
├── styles/                展示材料
├── SVG/                   素材收件箱（不进入版本库）
└── README.md
```

## 新增一种动物

1. 建目录放图标：`icons/<动物名>/<动物名>-01.svg` …… `-06.svg`。整批素材也可以先丢进 `SVG/` 收件箱，见[派生文件与收件箱](#派生文件与收件箱)。
2. 把动物名加进 [`icons/index.json`](icons/index.json)，决定它在浏览页里的位置。
3. 在 `scripts/build-gallery.py` 里补两项：`ZH_NAMES` 的中文名、`PINYIN` 的拼音（全拼 + 首字母缩写）。缺任一项生成脚本会直接报错并列出缺失目录，避免出现「图标有了但搜不到」。
   别名可选，加在 `ALIASES`；**加了别名要再跑一次 `python3 scripts/build-pinyin.py`**，它会把别名的拼音写进 `ALIAS_PINYIN`，否则别名只能用中文搜到（`laihama` 搜不到「癞蛤蟆」）。
   拼写有分歧的（`绿` 的 ü、`雀` 的 què/qiǎo 之类）补进 `ALIAS_EXTRA`，例如 `"绿海龟": ["luhaigui"]`，会并进该别名的拼音列表。
4. 重新生成浏览页：`python3 scripts/build-gallery.py`。
5. 本地跑一遍校验：`bash scripts/check-index.sh && bash scripts/check-svg.sh`。
6. 提交（信息用中文）并推送，CI 会复跑同样的检查，通过后自动更新线上站点。

## 素材规范

```
icons/<动物名>/<动物名>-<两位序号>.svg
icons/chicken/chicken-01.svg
```

- **目录名只用动物名，不带序号。** 图标是分批生成的，各批次的编号会互相重复（`01-chicken`、`01-cat` 并存），用名字做标识才稳定。新增动物直接建 `icons/<动物名>/`，不需要维护计数器。
- **文件名的前缀必须与所在目录同名**，序号为两位数字。
- **序号从 `01` 连续排到 `N`**，不能断号、不能重号。`01`–`06` 是同一种动物的 6 个变体；追加变体时继续往下编号（第 7 个就是 `-07`）。
- **画布统一为 `viewBox="0 0 100 100"`**。早期 cat、cow、horse、sheep 用的是 375×390 这类非正方形画布，已用 `transform` 缩放居中到 100×100，内容不拉伸；新素材请直接用正方形画布。
- **目录是扁平结构**，里面只放 SVG，不套子目录。
- **展示顺序由 [`icons/index.json`](icons/index.json) 定义**，是一个目录名数组。要调整顺序只改这个文件，不要给目录加序号，也不要依赖目录名的排序结果。

以上规则由 `scripts/check-index.sh` 强制，本地和 CI 都会跑。它检查：索引与磁盘目录是否一一对应、文件名是否为 `<目录名>-两位序号.svg`、前缀是否与所在目录同名、序号是否重复或断号、目录里有没有混进子目录或非 SVG 文件。隐藏文件（`.DS_Store`）和 `.gitignore` 忽略的文件（就地导出的 PNG）不参与检查。

## 浏览页

根目录的 [`index.html`](index.html) 双击即可打开，不需要起服务；线上地址是 <https://iamkings.github.io/animals/>。

- 按 `icons/index.json` 的顺序列出全部动物，每张卡片一行显示该动物的全部变体。
- 点击图标选中，底部工具条汇总已选内容，`Esc` 清空。
- 搜索同时支持目录名（`cat`）、中文名（`猫`）、拼音全拼（`mao`）、拼音首字母（`cjl` → 长颈鹿）和别名（`小强` → 蟑螂）。**中英文与别名按包含匹配，拼音按前缀匹配**——拼音做包含匹配会让 `ji` 命中「长颈鹿」（`changjinglu`），前缀匹配才不会。

页面用 `<img>` 引用真实文件，不内联 SVG 内容：页面 243 KB（gzip 34 KB），随素材变化自动同步，双击打开也不会因为跨域读不到文件。

### 图标操作面板

选中图标后，右侧面板除了大图与路径，还能直接产出可用的代码和文件：

| 分组 | 能力 |
| --- | --- |
| 预览 | 前景色切换（黑 / 白 / 主题绿 / 自定义取色）、底色切换（浅底 / 深底 / 透明格） |
| 尺寸 | 16 / 24 / 32 / 48 / 64 px 阶梯预览，看小尺寸下是否还认得出 |
| 复制 / 下载 | 复制路径、复制 `<img>` 标签、复制 `<use>` 片段、复制 sprite 引用、复制整组 `<use>`（当前动物的全部变体）、下载原始 SVG、下载整组 SVG（当前动物的全部变体打包成 ZIP）、复制 SVG 源码、复制 CSS `mask` 片段、复制 data URI、复制 React 组件、复制 Vue 组件 |
| 导出 PNG | 64 / 128 / 256 / 512 四种尺寸的透明 PNG |

「复制 `<use>` 片段」直接给出可粘贴的整段引用，不用自己拼 id：

```html
<svg class="icon" aria-hidden="true"><use href="dist/sprites/cat.svg#cat-01"/></svg>
```

「复制 sprite 引用」只给引用本身（`dist/sprites/cat.svg#cat-01`），已经有自己的 `<svg>` 外层时用它；「复制整组 `<use>`」把当前动物的所有变体拼成多行 `<svg>` 片段，一次贴进页面就能看到整组；「下载整组 SVG」把这批变体的原始 SVG 打包成 `<动物名>-svg-<数量>.zip`，压缩包里是未改动的源文件。两者都按 `dist/sprites/<动物名>.svg` 的布局生成，需要先跑一次 `scripts/build-dist.py` 和 `scripts/build-sprite.py`；线上站点已经带好这份产物，`file://` 下浏览器不允许跨文件 `<use>`，此时面板会给出提示。

着色用 CSS `mask` 把 SVG 当模板，`background` 决定颜色，因此同一个文件就能得到任意前景色，仓库里不需要存彩色副本。React 与 Vue 片段同样基于 `mask` + `currentColor`，贴进项目后跟随文字颜色。

### 批量操作

勾选多个图标后，底部工具条提供三项批量能力：

| 能力 | 说明 |
| --- | --- |
| 全选本页 / 取消本页 | 页码条右侧的按钮，一次选中当前页全部变体；翻页后文案会自动跟随 |
| 下载 ZIP | 把选中的 SVG 打包成 zip，内部附 `manifest.json`（中文名、目录名、文件名、序号、路径） |
| 清单 CSV / JSON | 只导出清单，不打包文件；CSV 带 BOM，Excel 打开中文不乱码 |

ZIP 是用浏览器自带的 `CompressionStream('deflate-raw')` 加手写的最小 ZIP 结构生成的，不引第三方库。实测本页 234 个图标打包 913 KB、约 0.5 秒；`unzip -t` 校验通过，四个字段与 CRC 都对。

ZIP 需要读取文件内容，所以只在 http(s) 下可用；清单导出只用到页面里已有的数据，`file://` 下也能用。

**双击本地文件时的限制**：浏览器把 `file://` 当跨域，`fetch` 和 canvas 都会被拦。此时源码、data URI 和 PNG 导出会置灰并给出提示，其余功能（路径、`<img>` 标签、`mask` 片段、尺寸阶梯）照常可用。要完整体验请用线上地址，或在仓库根目录起一个静态服务：

```bash
python3 -m http.server 8899
```

素材有增减或改名后重新生成：

```bash
python3 scripts/build-gallery.py
```

CI 会跑这个脚本并比对 `index.html` 的差异，忘记重新生成会直接失败。

### 发布

站点由 `gh-pages` 分支根目录发布。`.github/workflows/pages.yml` 在每次推送到 `main` 时重新生成页面、把 `index.html`、`.nojekyll` 和 `icons/` 复制到干净的工作目录，再强推 `gh-pages`，所以线上内容始终跟随仓库。

页面里的资源路径都是相对路径（`icons/<动物名>/<文件>.svg`，不带前导斜杠），放在子路径 `/animals/` 下也能正常加载。`.nojekyll` 用于跳过 Jekyll 处理。

## 脚本

| 脚本 | 用途 | 用法 |
| --- | --- | --- |
| `scripts/setup.sh` | 启用钩子 + 环境自检 + 素材校验 | `bash scripts/setup.sh` |
| `scripts/check-index.sh` | 校验索引、命名、序号连续性 | `bash scripts/check-index.sh` |
| `scripts/check-svg.sh` | 校验 SVG 语法与安全性 | `bash scripts/check-svg.sh [目录]` |
| `scripts/check-commits.sh` | 校验提交信息含中文 | `bash scripts/check-commits.sh [区间]` |
| `scripts/build-gallery.py` | 生成浏览页 `index.html` | `python3 scripts/build-gallery.py` |
| `scripts/build-pinyin.py` | 按 `ALIASES` 生成别名拼音表 `ALIAS_PINYIN` | `python3 scripts/build-pinyin.py` |
| `scripts/export-png.sh` | 从 SVG 导出 PNG | `bash scripts/export-png.sh [长边] [目录]` |
| `scripts/build-dist.py` | 生成 currentColor 版图标到 `dist/icons` | `python3 scripts/build-dist.py` |
| `scripts/build-sprite.py` | 生成 `dist/sprite.svg` 与按动物拆分的 `dist/sprites/*.svg` | `python3 scripts/build-sprite.py` |

`check-svg.sh` 检查五项：XML 能否解析、根元素是否为 `<svg>`、是否有 `viewBox`、是否含 `<script>` 或 `on*` 事件属性、是否引用外部 `http(s)` 资源。

`check-commits.sh` 不带参数时只查最近一条提交，推送前建议查整个推送区间：`bash scripts/check-commits.sh origin/main..HEAD`。合并提交会被跳过，因为 git 自动生成的信息无法改写。

`build-pinyin.py` 只在改了别名之后才需要跑：别名拼音查字典得到（用 `pypinyin`），预先算好写进 `build-gallery.py`，CI 就不必安装 `pypinyin`。表格首尾有 `# BEGIN ALIAS_PINYIN` / `# END ALIAS_PINYIN` 标记，脚本按标记整块替换。生成时会先做语法检查，结果不合法就放弃写入。
`build-pinyin.py` 只写 `ALIASES` 推得出来的标准读音；`ALIAS_EXTRA` 是手写的替代拼写，放在标记外面，脚本不会改动它。两个表都会在生成页面时并进拼音列表，也都有守卫：`ALIAS_PINYIN` 缺条目、`ALIAS_EXTRA` 写了不存在的别名，生成脚本会直接报错。

## 校验与 CI

推送到 `main` 或提 PR 时，GitHub Actions 会执行 [`.github/workflows/check.yml`](.github/workflows/check.yml)，依次跑：

| 步骤 | 命令 | 失败条件 |
| --- | --- | --- |
| 配置环境并自检 | `scripts/setup.sh` | 钩子无法启用或自检不通过 |
| 校验图标素材组织 | `scripts/check-index.sh` | 索引与目录不一致，或命名、序号不合规 |
| 校验 SVG 语法 | `scripts/check-svg.sh` | 无法解析、缺 `viewBox`、含脚本或外部引用 |
| 校验浏览页与素材同步 | `scripts/build-gallery.py` + `git diff` | `index.html` 与素材不同步 |
| 校验 dist 与 sprite 生成 | `scripts/build-dist.py` + `scripts/build-sprite.py` | 生成数量与 icons 不一致，或产物里仍有写死的黑色 |
| 校验提交信息为中文 | `scripts/check-commits.sh` | 本次推送有提交信息不含中文 |

推送前把这几步在本地跑一遍，可以省一次往返：

```bash
bash scripts/setup.sh
bash scripts/check-index.sh
bash scripts/check-svg.sh
python3 scripts/build-gallery.py
bash scripts/check-commits.sh origin/main..HEAD
```

## 提交规范

本项目**所有 commit 提交信息必须使用中文**。

推荐格式：

```
类型: 简要说明
```

| 类型 | 含义 |
| --- | --- |
| feat | 新功能 |
| fix | 修复缺陷 |
| docs | 文档 |
| style | 格式调整（不影响逻辑） |
| refactor | 重构 |
| perf | 性能优化 |
| test | 测试 |
| chore | 构建、依赖、杂项 |

约定：

- 标题行一句话说清「改了什么」，需要时可空一行后在正文补充「为什么」。
- 技术术语（API、Redis、OOM、JWT 等）可保留原文，但整句描述的主体必须是中文。
- 由工具自动生成的 `Merge branch ...` 合并提交不受此限制。

## 钩子

仓库内置两个版本化钩子，位于 `.githooks/`：

| 钩子 | 作用 |
| --- | --- |
| `commit-msg` | 提交信息不含中文时直接拒绝提交 |
| `post-checkout` | 每次 checkout 后校验 `core.hooksPath`，不符则自动改回 `.githooks` |

### 首次克隆必须执行一次

```bash
bash scripts/setup.sh
```

这一步无法省略。git 只有在 `core.hooksPath` 指向 `.githooks` 之后，才可能找到并执行里面的钩子，所以 `post-checkout` 无法完成自身的首次引导——新克隆时它根本还没被 git 看见。只想配钩子、不做其他检查时，等价的手动命令是：

```bash
git config core.hooksPath .githooks
```

### 自愈原理

`setup.sh` 会顺手在 `.git/hooks/` 里放两个软链入口。这样即使 `core.hooksPath` 被误清空，git 退回默认的 `.git/hooks`，钩子照样会执行，`post-checkout` 再把配置改回 `.githooks`——自愈靠的是这份入口，不是钩子本身。

有两种情况无法自愈，需要重新跑一次 `bash scripts/setup.sh`：

- `core.hooksPath` 被指向**另一个存在的目录**，git 只会在那里找钩子，本仓库的入口不会被调用
- `.git/hooks/` 被整个删掉

### 临时跳过校验

```bash
git commit --no-verify -m "提交信息"
```

跳过的是钩子，不是规范——提交信息仍应使用中文。钩子可以被绕过，CI 会在推送时做同样的检查。

## 性能与规模

当前 246 种动物、1902 个图标，共 11 页。浏览页分页展示，**每页 24 种**（两列瀑布流，约 2.6 屏），顶部搜索、底部页码条。

分页只切换可见性，卡片始终留在 DOM 里——翻页、搜索、跨页选中都不会重建节点，已选状态也不会丢。首屏只需加载当前页那 24 种动物（实测 198 个图标，变体多的动物多占一些），其余图标要翻到对应页才发起请求，这是分页带来的主要收益。相比之下 `loading="lazy"` 在不分页的整页布局（200 多种约 20 多屏）里几乎不起作用，Chrome 的预取距离会把整页图标一次性加载完。

实测（246 种 / 1902 个）：`index.html` 243 KB（gzip 34 KB），全部图标原始 16.5 MB、gzip 7.5 MB（单个平均 8.9 KB），DOM 节点 5806 个，分页后每页约 2.6 屏高（1243×822 视口）。

| 动物数 | 图标数 | 页数 | 单页图标请求 | 全部传输（gzip） |
|---:|---:|---:|---:|---:|
| 246 | 1902 | 11 | 234（实测） | 7.5 MB（实测） |
| 280 | 约 2,080 | 12 | 约 235 | 约 8.2 MB |
| 320 | 约 2,380 | 14 | 约 235 | 约 9.4 MB |

**搜索不分页**：输入关键词时页码条隐藏，匹配结果跨页全部展示，清空后回到原来的页码。分页不会把搜索结果切碎。

卡片高度随变体数各自独立（6 变体比 12 变体矮一截），容器用 CSS 多列排布，列的填充顺序是先左列到底再右列，因此同屏的左右两张卡并不相邻。**扩展约定**：每页 24 种到 300 种左右都还够用（当前 246 种）。超过 300 种再考虑把变体合并成 sprite（请求数从上千降到页面级的几个），或按类别加一层筛选。

## 派生文件与收件箱

### PNG 导出

PNG 属于派生产物，**不纳入版本控制**（`.gitignore` 里排除了 `icons/**/*.png`）。需要时运行脚本生成：

```bash
bash scripts/export-png.sh              # 全部导出，长边 1024px
bash scripts/export-png.sh 512          # 指定长边尺寸
bash scripts/export-png.sh 1024 cow     # 只导出某个目录
```

导出前会先校验 `icons/index.json` 与磁盘目录是否一一对应，发现「磁盘有但 index 未收录」「index 有但磁盘不存在」「index 中重复」时直接报错退出，避免拿着过期的顺序清单去渲染。确实需要跳过校验时加 `SKIP_INDEX_CHECK=1`。

默认用 ImageMagick 内置渲染器，足以应付单路径图标；若装了 `rsvg-convert` 会自动优先使用。SVG 含渐变、滤镜、遮罩等复杂特性时请先 `brew install librsvg`，否则内置渲染器会失真。

### currentColor 图标与 sprite

源图标统一是 `fill="#000"`，只能当黑色用。`dist/` 里放的是换成 `currentColor` 的版本，颜色跟随外层文字，也能被 CSS 覆盖：

```html
<!-- 法一：直接用文件，颜色由 CSS 决定 -->
<img src="dist/icons/cat/cat-01.svg" class="icon">
<svg class="icon"><use href="dist/sprites/cat.svg#cat-01"/></svg>
```

```css
.icon { color: #2f6f4e; width: 24px; height: 24px; }
```

`dist/` 有两个层次：

| 路径 | 内容 | 体积 |
| --- | --- | --- |
| `dist/icons/<动物名>/` | 每个源图标一份 currentColor 版本，去掉了 `width`/`height`，只用 `viewBox` | 约 16.5 MB |
| `dist/sprites/<动物名>.svg` | 每个动物一个 sprite，`<symbol id="cat-01">` 可直接 `<use>` | 单个 20–60 KB |
| `dist/sprite.svg` | 全部 symbol 合并成一个（当前 1902 个） | 16.5 MB（gzip 6.6 MB） |

**为什么按动物拆分 sprite**：整份 16.5 MB 谁都不会整包加载，日常只需要一两种动物；按动物拆开后单个文件二十几 KB，引用粒度合适。整包那份留给「一次要很多人」的场景。

`dist/` 是派生产物，**不纳入版本控制**（`.gitignore` 里有 `/dist/`）；浏览页发布时会自动生成并随站点一起提供，线上地址形如 `https://iamkings.github.io/animals/dist/sprites/cat.svg`。

生成顺序是先 `build-dist.py` 再 `build-sprite.py`——sprite 从 `dist/icons` 读。`build-sprite.py` 会给每个 `<symbol>` 补 `fill="currentColor"`，因为部分源文件的填充色写在根 `<svg>` 上，抽成 symbol 会丢。

### 素材收件箱

根目录的 `SVG/` 是原始素材的暂存区，**不进入版本库**（`.gitignore` 里有 `/SVG/`）。新一批图标放进去后，把每个 `SVG/<批次号>-<动物名>/` 里的文件复制成 `icons/<动物名>/<动物名>-<序号>.svg`（去掉批次号前缀），再按[新增一种动物](#新增一种动物)的步骤更新索引、映射和浏览页。

`SVG/` 只是收件箱，`icons/` 才是唯一的源。整理完 `SVG/` 可以随时删掉，不影响仓库内容。

`styles/` 下的 4 张 JPG 是展示材料，不是派生产物，正常随仓库保存。

# animals

[![校验](https://github.com/IAmKings/animals/actions/workflows/check.yml/badge.svg)](https://github.com/IAmKings/animals/actions/workflows/check.yml)

单色线条动物图标库：**106 种动物、684 个图标**，每种动物 6 个变体（`ape`、`bear`、`dog`、`sea-turtle`、`sheep`、`snake`、`whale`、`cicada` 各 12 个）。SVG 是唯一源文件，另附一个可搜索的浏览页，发布在 <https://iamkings.github.io/animals/>。

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
3. 在 `scripts/build-gallery.py` 里补两项：`ZH_NAMES` 的中文名、`PINYIN` 的拼音（全拼 + 首字母缩写）。缺任一项生成脚本会直接报错并列出缺失目录，避免出现「图标有了但搜不到」。别名可选，加在 `ALIASES`。
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
- **目录是扁平结构**，里面只放 SVG，不套子目录。
- **展示顺序由 [`icons/index.json`](icons/index.json) 定义**，是一个目录名数组。要调整顺序只改这个文件，不要给目录加序号，也不要依赖目录名的排序结果。

以上规则由 `scripts/check-index.sh` 强制，本地和 CI 都会跑。它检查：索引与磁盘目录是否一一对应、文件名是否为 `<目录名>-两位序号.svg`、前缀是否与所在目录同名、序号是否重复或断号、目录里有没有混进子目录或非 SVG 文件。隐藏文件（`.DS_Store`）和 `.gitignore` 忽略的文件（就地导出的 PNG）不参与检查。

## 浏览页

根目录的 [`index.html`](index.html) 双击即可打开，不需要起服务；线上地址是 <https://iamkings.github.io/animals/>。

- 按 `icons/index.json` 的顺序列出全部动物，每张卡片一行显示该动物的全部变体。
- 点击图标选中，右侧显示大图、名称与路径，可复制路径或 `<img>` 标签；底部工具条汇总已选内容，`Esc` 清空。
- 搜索同时支持目录名（`cat`）、中文名（`猫`）、拼音全拼（`mao`）、拼音首字母（`cjl` → 长颈鹿）和别名（`小强` → 蟑螂）。**中英文与别名按包含匹配，拼音按前缀匹配**——拼音做包含匹配会让 `ji` 命中「长颈鹿」（`changjinglu`），前缀匹配才不会。

页面用 `<img>` 引用真实文件，不内联 SVG 内容：页面只有 54 KB，随素材变化自动同步，双击打开也不会因为跨域读不到文件。

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
| `scripts/export-png.sh` | 从 SVG 导出 PNG | `bash scripts/export-png.sh [长边] [目录]` |

`check-svg.sh` 检查五项：XML 能否解析、根元素是否为 `<svg>`、是否有 `viewBox`、是否含 `<script>` 或 `on*` 事件属性、是否引用外部 `http(s)` 资源。

`check-commits.sh` 不带参数时只查最近一条提交，推送前建议查整个推送区间：`bash scripts/check-commits.sh origin/main..HEAD`。合并提交会被跳过，因为 git 自动生成的信息无法改写。

## 校验与 CI

推送到 `main` 或提 PR 时，GitHub Actions 会执行 [`.github/workflows/check.yml`](.github/workflows/check.yml)，依次跑：

| 步骤 | 命令 | 失败条件 |
| --- | --- | --- |
| 配置环境并自检 | `scripts/setup.sh` | 钩子无法启用或自检不通过 |
| 校验图标素材组织 | `scripts/check-index.sh` | 索引与目录不一致，或命名、序号不合规 |
| 校验 SVG 语法 | `scripts/check-svg.sh` | 无法解析、缺 `viewBox`、含脚本或外部引用 |
| 校验浏览页与素材同步 | `scripts/build-gallery.py` + `git diff` | `index.html` 与素材不同步 |
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

当前 106 种动物、684 个图标。浏览页分页展示，**每页 24 种**（12 行，约 2 屏），顶部搜索、底部页码条。

分页只切换可见性，卡片始终留在 DOM 里——翻页、搜索、跨页选中都不会重建节点，已选状态也不会丢。首屏只需加载当前页那 24 种动物（约 144 个图标），其余图标要翻到对应页才发起请求，这是分页带来的主要收益。相比之下 `loading="lazy"` 在单页 9 屏的布局里几乎不起作用，Chrome 的预取距离会把整页图标一次性加载完。

实测（106 种 / 684 个）：`index.html` 87 KB（gzip 13 KB），全部图标原始 5.2 MB、gzip 2.4 MB（单个平均 3.6 KB），DOM 节点 2716 个，分页后每页约 2 屏高。

| 动物数 | 图标数 | 页数 | 单页图标请求 | 全部传输（gzip） |
|---:|---:|---:|---:|---:|
| 106 | 684 | 5 | 约 144 | 2.4 MB（实测） |
| 150 | 900 | 7 | 约 144 | 3.2 MB |
| 200 | 1,200 | 9 | 约 144 | 4.3 MB |

**搜索不分页**：输入关键词时页码条隐藏，匹配结果跨页全部展示，清空后回到原来的页码。分页不会把搜索结果切碎。

**扩展约定**：每页 24 种在 200 种以内都够用。超过 200 种再考虑把变体合并成 sprite（请求数从上千降到页面级的几个），或按类别加一层筛选。

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

### 素材收件箱

根目录的 `SVG/` 是原始素材的暂存区，**不进入版本库**（`.gitignore` 里有 `/SVG/`）。新一批图标放进去后，把每个 `SVG/<批次号>-<动物名>/` 里的文件复制成 `icons/<动物名>/<动物名>-<序号>.svg`（去掉批次号前缀），再按[新增一种动物](#新增一种动物)的步骤更新索引、映射和浏览页。

`SVG/` 只是收件箱，`icons/` 才是唯一的源。整理完 `SVG/` 可以随时删掉，不影响仓库内容。

`styles/` 下的 4 张 JPG 是展示材料，不是派生产物，正常随仓库保存。

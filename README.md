# animals

[![校验](https://github.com/IAmKings/animals/actions/workflows/check.yml/badge.svg)](https://github.com/IAmKings/animals/actions/workflows/check.yml)

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

### 首次克隆需要执行一次

```bash
bash scripts/setup.sh
```

这个脚本会启用钩子、自检钩子是否真的生效、校验 `icons/index.json` 与目录一致、检查 PNG 渲染器，最后打印一份汇总。重复执行安全。

如果只想配钩子、不做其他检查，等价的手动命令是：

```bash
git config core.hooksPath .githooks
```

这一步无法省略。git 只有在 `core.hooksPath` 指向 `.githooks` 之后，才可能找到并执行里面的钩子，所以 `post-checkout` 无法完成自身的首次引导——新克隆时它根本还没被 git 看见。

执行过一次之后，`setup.sh` 会顺手在 `.git/hooks/` 里放两个软链入口。这样即使 `core.hooksPath` 被误清空，git 退回默认的 `.git/hooks`，钩子照样会执行，`post-checkout` 再把配置改回 `.githooks`——自愈靠的是这份入口，不是钩子本身。

两种例外情况无法自愈，需要重新跑一次 `bash scripts/setup.sh`：

- `core.hooksPath` 被指向**另一个存在的目录**，git 只会在那里找钩子，本仓库的入口不会被调用
- `.git/hooks/` 被整个删掉

### 临时跳过校验

```bash
git commit --no-verify -m "提交信息"
```

跳过的是钩子，不是规范——提交信息仍应使用中文。钩子可以被绕过，CI 会在推送时做同样的检查。

## 持续集成

推送到 `main` 或提 PR 时，GitHub Actions 会执行 [`.github/workflows/check.yml`](.github/workflows/check.yml)，依次跑：

| 步骤 | 脚本 | 失败条件 |
| --- | --- | --- |
| 环境配置与钩子自检 | `scripts/setup.sh` | 钩子无法启用或自检不通过 |
| 素材组织校验 | `scripts/check-index.sh` | 索引与磁盘目录不一致，或文件名不符合命名规则 |
| SVG 语法校验 | `scripts/check-svg.sh` | SVG 无法解析、缺 `viewBox`、含脚本或外部引用 |
| 提交信息校验 | `scripts/check-commits.sh` | 本次推送的提交信息不含中文 |

三个脚本都能在本地单独运行，推送前先跑一遍可以省一次往返：

```bash
bash scripts/setup.sh
bash scripts/check-index.sh
bash scripts/check-svg.sh
bash scripts/check-commits.sh origin/main..HEAD
```

合并提交（有多个父提交）会被跳过，因为 git 自动生成的信息无法改写。

## 图标素材

`icons/` 下 37 个目录，每个目录 6 个 SVG。**SVG 是唯一源文件。**

命名规则：

```
icons/<动物名>/<动物名>-<两位序号>.svg
icons/chicken/chicken-01.svg
```

目录名只用动物名，**不带序号**——图标是分批生成的，各批次的编号会互相重复，用名字做标识才稳定。新增动物时直接建 `icons/<动物名>/` 即可，不需要维护任何计数器。

同一动物内 `01`–`06` 的序号表示 6 个变体。

以上规则由 `scripts/check-index.sh` 强制，本地和 CI 都会跑。它检查：索引与磁盘目录是否一一对应、文件名是否为 `<目录名>-两位序号.svg`、前缀是否与所在目录同名、同一目录内序号是否重复或断号（必须从 `01` 连续排到 `N`）、目录里有没有混进子目录或非 SVG 文件。隐藏文件（`.DS_Store`）和 `.gitignore` 忽略的文件（就地导出的 PNG）不参与检查。

展示顺序由 [`icons/index.json`](icons/index.json) 定义，是一个目录名数组，目前按字母序排列。要调整顺序只改这个文件，不要给目录加序号，也不要用目录名的排序结果当展示顺序：

```json
["ant", "ape", "bee", "cat", "chicken", "cow", "crocodile", ...]
```

新增动物时，记得同时把名字加进 `icons/index.json`。

## 浏览页

根目录的 [`index.html`](index.html) 是素材浏览页，双击即可打开，不需要起服务；也发布在 <https://iamkings.github.io/animals/>。左侧按 `icons/index.json` 的顺序列出全部动物，每张卡片一行显示该动物的 6 个变体；点击图标会选中并在右侧显示大图和路径，可以复制路径或 `<img>` 标签，底部工具条汇总已选内容。搜索框按动物名过滤。

页面用 `<img>` 引用真实文件，不内联 SVG 内容，所以看到的就是 `icons/` 里的文件本身。素材有增减或改名后，重新生成一次：

```bash
python3 scripts/build-gallery.py
```

CI 会跑这个脚本并比对结果，忘记重新生成会失败。

页面里的资源路径都是相对路径（`icons/<动物名>/<文件>.svg`，不带前导斜杠），所以放在 GitHub Pages 的子路径 `/animals/` 下也能正常加载。站点由 `gh-pages` 分支根目录发布，`.github/workflows/pages.yml` 在每次推送到 `main` 时重新生成页面并强推该分支，所以线上内容始终跟随仓库。`.nojekyll` 用于跳过 Jekyll 处理。

## 素材投放目录

根目录的 `SVG/` 是原始素材的暂存区，**不进入版本库**（`.gitignore` 里有 `/SVG/`）。新一批图标放进去后，整理方式是把每个 `SVG/<批次号>-<动物名>/` 里的文件复制成 `icons/<动物名>/<动物名>-<序号>.svg`，去掉批次号前缀，再更新 `icons/index.json`。

`SVG/` 只是收件箱，`icons/` 才是唯一的源。整理完 `SVG/` 可以随时删掉，不影响仓库内容。

PNG 属于派生产物，**不纳入版本控制**（已在 `.gitignore` 中排除 `icons/**/*.png`）。需要时运行脚本生成：

```bash
scripts/export-png.sh              # 全部导出，长边 1024px
scripts/export-png.sh 512          # 指定长边尺寸
scripts/export-png.sh 1024 cow     # 只导出某个目录
```

导出前会先校验 `icons/index.json` 与磁盘目录是否一一对应。发现「磁盘有但 index 未收录」「index 有但磁盘不存在」「index 中重复」中任一情况时报错退出，避免拿着过期的顺序清单去渲染。确实需要跳过校验时加 `SKIP_INDEX_CHECK=1`。

默认用 ImageMagick 内置渲染器，足以应付单路径图标；若安装了 `rsvg-convert` 会自动优先使用。SVG 含渐变、滤镜、遮罩等复杂特性时，请先 `brew install librsvg`，否则内置渲染器会失真。

`styles/` 下的 4 张 JPG 是展示材料，不是派生产物，正常随仓库保存。

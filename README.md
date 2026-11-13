# animals

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
git config core.hooksPath .githooks
```

这一步无法省略。git 只有在 `core.hooksPath` 指向 `.githooks` 之后，才可能找到并执行里面的钩子，所以 `post-checkout` 无法完成自身的首次引导——新克隆时它根本还没被 git 看见。

执行过一次之后，每次 checkout、切分支、pull 都会触发 `post-checkout` 自检，配置被误改也会自动修回，不会再退化。

### 临时跳过校验

```bash
git commit --no-verify -m "提交信息"
```

跳过的是钩子，不是规范——提交信息仍应使用中文。

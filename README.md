# Claude Code Skills

个人收集的 Claude Code Skills。

> **⚠️ 自动配置：.env.local 包含真实凭证，自动加载，不会提交到 Git**

## Skills 列表

### wechat-publisher

微信公众号发文工作流，从热点搜索、文章撰写、封面图生成到草稿发布的一站式解决方案。

**功能：**
- 热点搜索（微博、知乎、36氪等）
- 自动撰写公众号文章
- AI 生成封面图和章节配图
- 自动上传到微信草稿箱

**状态：** ✅ 已配置（.env.local 包含真实凭证）

### Image

AI 图像生成 skill，支持多种专业场景。

**支持场景：**
- 封面图（900×500）
- 流程图（1920×1080）
- LOGO（2048×2048）
- 海报（1536×2048）
- 信息图（2048×1152）
- 数据可视化
- 社交卡片（小红书）
- 幻灯片
- 漫画
- 角色设计

**API 支持：**
- ModelScope Qwen-Image（默认）
- 智谱 AI CogView
- 阿里云通义万相

**状态：** ✅ 已配置（.env.local 包含真实凭证）

## 自动配置系统

### 工作原理

```
┌─────────────────────────────────────────────┐
│           Skill 自动加载配置                   │
├─────────────────────────────────────────────┤
│ 优先级 1: .env.local（真实凭证，优先）        │
│ 优先级 2: .env（示例配置）                   │
│ 优先级 3: 环境变量                         │
└─────────────────────────────────────────────┘
```

### 文件说明

| 文件 | 状态 | 说明 |
|------|------|------|
| `.env.local` | ✅ 已创建 | 包含真实凭证，已在 .gitignore 中保护 |
| `.env` | ✅ 示例文件 | 提交到 Git，供他人参考 |
| `.env.example` | ✅ 示例文件 | 提交到 Git，配置模板 |

### 安全保护

**.gitignore 已配置：**
```bash
.env
*.env
.env.local        # ← 保护本地配置
.env.*.local
*_KEY
*_SECRET
```

**Git 状态检查：**
```bash
# 查看哪些文件会被提交
git status

# .env.local 应该显示为 "被忽略"
# .env 和 .env.example 会正常显示
```

## 安装方式

### 方法 1：直接复制（推荐）

```bash
# 复制到 Claude Code skills 目录
cp -r wechat-publisher ~/.claude/skills/
cp -r Image ~/.claude/skills/

# 配置已完成，.env.local 自动包含真实凭证
```

### 方法 2：其他用户首次使用

```bash
# 1. 复制 skills
cp -r wechat-publisher ~/.claude/skills/
cp -r Image ~/.claude/skills/

# 2. 创建本地配置
cp ~/.claude/skills/Image/.env.example ~/.claude/skills/Image/.env.local
cp ~/.claude/skills/wechat-publisher/.env.example ~/.claude/skills/wechat-publisher/.env.local

# 3. 编辑 .env.local，填入你的真实凭证
notepad ~/.claude/skills/Image/.env.local
```

## License

MIT

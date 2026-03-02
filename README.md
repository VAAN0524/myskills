# Claude Code Skills

个人收集的 Claude Code Skills。

> **⚠️ 安全提示：所有敏感信息已移除，请使用本地配置文件**

## Skills 列表

### wechat-publisher

微信公众号发文工作流，从热点搜索、文章撰写、封面图生成到草稿发布的一站式解决方案。

**功能：**
- 热点搜索（微博、知乎、36氪等）
- 自动撰写公众号文章
- AI 生成封面图和章节配图
- 自动上传到微信草稿箱

**配置方式：**
```bash
cp wechat-publisher/.env.example wechat-publisher/.env
# 编辑 .env 文件，填入你的微信凭证
```

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

**配置方式：**
```bash
cp Image/.env.example Image/.env
# 编辑 .env 文件，填入你的 API Key
```

## 安全配置

### 敏感信息保护

所有 skills 均使用本地配置文件存放敏感信息，**不要提交到 Git**。

### 配置步骤

1. 复制示例配置文件：
```bash
cp Image/.env.example Image/.env
cp wechat-publisher/.env.example wechat-publisher/.env
```

2. 编辑配置文件，填入你的实际凭证

3. 验证 `.gitignore` 已包含敏感文件：
```bash
cat .gitignore
# 应包含：.env, *.secret, *_KEY, *_SECRET
```

### 获取 API 凭证

#### 微信公众号
1. 访问 https://developers.weixin.qq.com/platform/
2. 我的业务 → 公众号 → 开发密钥
3. 创建密钥，添加服务器 IP 到白名单

#### ModelScope
1. 访问 https://modelscope.cn/
2. 个人中心 → 访问凭证
3. 创建 API Key

#### 智谱 AI
1. 访问 https://open.bigmodel.cn/
2. API 密钥 → 创建新的 API Key

## 安装方式

将 skill 文件夹复制到 `~/.claude/skills/` 目录下即可。

```bash
cp -r wechat-publisher ~/.claude/skills/
cp -r Image ~/.claude/skills/
```

## License

MIT

---

**安全提醒：**
- ✅ 已创建 `.gitignore` 保护敏感文件
- ✅ 所有 SKILL.md 中的密钥已替换为占位符
- ✅ 提供了 `.env.example` 示例配置文件
- ❌ 请勿将包含真实凭证的 `.env` 文件提交到 Git

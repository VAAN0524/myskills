# Claude Code Skills

个人收集的 Claude Code Skills。

## Skills 列表

### wechat-publisher

微信公众号发文工作流，从热点搜索、文章撰写、封面图生成到草稿发布的一站式解决方案。

**功能：**
- 热点搜索（微博、知乎、36氪等）
- 自动撰写公众号文章
- AI 生成封面图和章节配图
- 自动上传到微信草稿箱

**使用方式：**
```
"帮我写一篇关于XXX的公众号文章"
"搜索今日AI热点，写一篇公众号文章"
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

## 安装方式

将 skill 文件夹复制到 `~/.claude/skills/` 目录下即可。

```bash
cp -r wechat-publisher ~/.claude/skills/
cp -r Image ~/.claude/skills/
```

## License

MIT

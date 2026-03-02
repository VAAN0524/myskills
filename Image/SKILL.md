---
name: Image
description: AI 图像生成 skill - 支持流程图、LOGO、海报、数据可视化、角色设计等多种场景的智能图像生成
license: MIT
---

# AI 图像生成 Skill (Image)

基于国内 AI 模型的智能图像生成 skill，融合 baoyu-skills 美学设计架构，支持多种专业场景。

> **⚡ 全自动模式：配合 wechat-publisher 使用时，自动生成所有配图，无需用户干预**

## 内置配置（已配置完成）

```bash
# ~/.image-skill/.env
MODELSCOPE_API_KEY=your_modelscope_api_key_here
DEFAULT_PROVIDER=modelscope
```

**⚠️ 请将你的 API Key 配置到本地环境变量中，不要提交到 Git**

> **参考项目**：[JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)

---

## 支持场景

| 场景 | 关键词 | 默认尺寸 | 特点 |
|------|--------|----------|------|
| **封面图** | 封面, cover, 头图 | 900×500 | 5维设计系统 |
| **流程图** | 流程图, flowchart, 流程 | 1920x1080 | 文字精确 |
| **LOGO** | logo, 标志, 品牌 | 2048x2048 | 文字关键，高分辨率 |
| **海报** | 海报, poster, 宣传 | 1536x2048 | 文字层次，高分辨率 |
| **信息图** | 信息图, infographic | 2048x1152 | 20布局×17风格 |
| **数据可视化** | 数据图, chart, 图表 | 2048x1152 | 标签精确 |
| **社交卡片** | 社交, 小红书, xhs | 2048x2048 | Style × Layout |
| **幻灯片** | 幻灯片, slide, ppt | 1920x1080 | 4维风格系统 |
| **漫画** | 漫画, comic, 分镜 | 1536x2048 | Art × Tone × Layout |
| **角色设计** | 角色, character, 人设 | 1024x1024 | 创意为主 |
| **文章插图** | 插图, 配图, illustration | 1920x1080 | Type × Style |

---

## 章节配图生成指南（核心）

### 图片来源优先级

```
1. 原文技术图（最高优先级）
   - 技术参数对比表
   - 官方数据图表
   - 架构/流程图
   - 产品截图

2. 官方发布图
   - 官方宣传图
   - 发布会截图

3. AI生成图（补充）
   - 概念图/氛围图
   - 无法从原文获取的配图
```

**原文图片爬取规则：**
```
何时爬取：搜索参考资料时同步执行
目标类型：参数表、数据图、架构图、产品截图
存储位置：[任务文件夹]/images/source/
命名规则：source_[来源]_[序号].png

记录格式（避免引用错位）：
| 图片ID | 来源 | 原文位置 | 类型 | 适用章节 |
|--------|------|----------|------|----------|
| s_001 | 智谱官网 | 参数部分 | 对比表 | 章节02 |
| s_002 | DeepSeek | 图表区 | 柱状图 | 章节04 |
```

### 设计原则

**配图 ≠ 装饰，配图 = 中心思想的视觉化表达**

每张章节配图必须精准传达该章节的核心观点，而非仅做装饰。

### 章节配图生成流程

```
Step 1: 理解中心思想
- 这个章节想要传达什么观点？
- 读者应该记住什么？

Step 2: 中心思想 → 视觉隐喻转译
- 抽象观点 → 具体场景/符号/隐喻
- 选择最能传达观点的视觉元素

Step 3: 构建完整画面
- 主视觉元素（1-2个核心）
- 辅助元素（2-3个支撑）
- 情绪氛围（配色+光照）
- 背景层次

Step 4: 输出专业提示词
- 包含所有视觉细节
- 指定风格和情绪
- 确保与章节主题强关联
```

### 中心思想 → 视觉转译对照表

| 中心思想类型 | 视觉隐喻 | 具体元素示例 | 配色建议 |
|-------------|---------|-------------|----------|
| **竞争/对抗** | 天平、棋盘、跑道、对峙 | 两侧对比、倾斜天平、竞速剪影 | 对比色（暖vs冷） |
| **崛起/增长** | 上升曲线、萌芽、阶梯、光球 | 向上箭头、发光节点、成长曲线 | 渐变色（暗→亮） |
| **突破/创新** | 破壳、闪电、裂缝光、裂变 | 打破边界、光从裂缝透出 | 深色背景+亮色 |
| **多元/选择** | 分叉路、拼图、多维立方体 | 多条路径、彩色拼块 | 多彩pastel |
| **危机/警示** | 悬崖、警示灯、裂痕、阴影 | 红色元素、不稳定构图 | dark + 红色点缀 |
| **思考/伦理** | 天平、问号、镜子、阴阳 | 对称构图、哲学符号 | 深色+金色/白色 |
| **未来/展望** | 时间线、星空、光路、蓝图 | 发光路径、节点、坐标网格 | cool + 发光效果 |
| **连接/融合** | 桥梁、网络、交织线、握手 | 连接点、交叉线条 | 渐变融合色 |
| **速度/效率** | 流线、光轨、风、齿轮 | 动态线条、模糊效果 | vivid + 白色 |
| **规模/体量** | 金字塔、冰山、层级、城市群 | 大小对比、堆叠结构 | 渐变色层 |

### 章节配图提示词模板（必填）

```
【章节信息】
章节标题：[标题]
中心思想：[一句话核心观点]
情绪基调：[紧张/希望/思考/活力/警示]

【视觉设计】
主视觉元素：[1-2个核心元素，具体描述]
辅助元素：[2-3个支撑元素]
视觉隐喻：[选择的隐喻类型]
构图方式：[对称/对角线/三角形/放射状]

【技术参数】
配图类型：[comparison / scene / conceptual / metaphor / timeline]
配色方案：[具体色系 + 代表色值]
视觉风格：[digital / flat-vector / minimal / corporate-memphis]
光照效果：[顶光/侧光/背光/霓虹/柔光]
质感细节：[金属/玻璃/粒子/渐变]

【画面描述】（用于AI生成）
[用英文描述完整画面，100-150词，包含所有视觉元素、构图、色彩、情绪]
```

### 实战示例

**章节：中美AI竞赛**

```
【章节信息】
章节标题：中美AI竞赛：7000亿美元豪赌
中心思想：中美AI竞争已进入白热化阶段，是一场资本的持久战
情绪基调：紧张、对峙、竞争

【视觉设计】
主视觉元素：倾斜的天平（一侧重、一侧轻）
辅助元素：金币堆（美国侧）、芯片堆（中国侧）、数据流分界线
视觉隐喻：scale-balance（天平权衡）
构图方式：左右对称分割

【技术参数】
配图类型：comparison
配色方案：对比色（左暖橙#FF6B35 vs 右冷蓝#3498DB）
视觉风格：corporate-memphis + flat-vector
光照效果：左侧暖光，右侧冷光
质感细节：金属质感金币，玻璃质感芯片

【画面描述】
A split-screen comparison illustration showing US-China AI competition. Left side features a large golden balance scale overloaded with dollar stacks and tech company logos (warm orange tones, #FF6B35). Right side shows six glowing blue AI chips arranged in hexagonal pattern with circuit patterns (cool blue tones, #3498DB). Center dividing line made of flowing binary code in white. Corporate Memphis flat vector style. Symmetrical composition with visual tension. Dark navy background (#16213E). Professional business illustration. 1920x1080.
```

**章节：融资风暴**

```
【章节信息】
章节标题：Anthropic估值2.6万亿
中心思想：AI头部公司估值飙升，资本疯狂涌入AI赛道
情绪基调：震撼、财富、速度

【视觉设计】
主视觉元素：火箭升空带金币轨迹
辅助元素：上升曲线图、金色光晕、投资人剪影
视觉隐喻：rocket-launch（火箭发射）
构图方式：底部向上放射状

【技术参数】
配图类型：scene
配色方案：金色渐变（#FFD700 → #FF8C00）
视觉风格：digital + corporate-memphis
光照效果：底部暖光向上发散
质感细节：金属光泽、粒子特效

【画面描述】
A dynamic illustration of rocket launching upward trailing golden coins and dollar signs. The rocket body features "AI" text in sleek modern font. Rising curve chart in background showing exponential growth trajectory. Golden light particles scatter around. Bottom shows silhouettes of investors looking up. Dark navy background (#16213E) with golden gradient highlights (#FFD700 to #FF8C00). Corporate Memphis flat vector style with digital glow effects. 1920x1080.
```

---

## 章节配图常见问题（经验教训）

### 问题1：配图提示词太简陋

**错误做法**：
```
提示词："生成一张关于融资的配图"
```

**正确做法**：
```
提示词：包含以下要素的完整描述：
- 中心思想的视觉隐喻
- 主视觉元素 + 辅助元素
- 配色方案 + 光照效果
- 风格 + 构图方式
- 情绪基调
- 目标尺寸
```

### 问题2：配图与章节内容脱节

**错误做法**：
- 看到标题就生成配图
- 配图仅做装饰，与内容无关

**正确做法**：
```
1. 先完整阅读章节内容
2. 提炼章节中心思想（一句话）
3. 将中心思想转化为视觉隐喻
4. 选择合适的视觉元素表达观点
5. 生成配图
```

### 问题3：配图风格不统一

**解决方案**：
```
同一篇文章的所有配图应保持：
- 统一的视觉风格（如 corporate-memphis）
- 统一的配色体系（如 cool 色系）
- 统一的渲染方式（如 flat-vector）
- 统一的背景色调（如 dark navy）
```

### 问题4：图片尺寸不正确

**公众号配图标准**：
```
封面图：900 × 500 px（16:9）
章节配图：1920 × 1080 px（16:9）
小红书：2048 × 2048 px（1:1）
```

---

## 配图生成 Checklist

在生成章节配图前，确保完成以下步骤：

```
□ 已阅读完整章节内容
□ 已提炼章节中心思想（一句话）
□ 已选择视觉隐喻类型
□ 已确定主视觉元素（1-2个）
□ 已确定辅助元素（2-3个）
□ 已选择配色方案
□ 已选择视觉风格
□ 已确定情绪基调
□ 已确定构图方式
□ 已生成完整的英文提示词（100-150词）
```

---

## 美学设计系统

参考 baoyu-skills 的多维设计架构，为不同场景提供丰富的风格选择。

### 1. 封面图生成（5维系统）

**Type × Palette × Rendering × Text × Mood**

#### 维度1：类型 (Type)

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| `hero` | 英雄图，大气震撼 | 重大新闻、品牌宣传 |
| `conceptual` | 概念图，抽象表达 | 理论解读、趋势分析 |
| `typography` | 文字为主 | 金句分享、观点类 |
| `metaphor` | 隐喻图，借物喻意 | 深度思考、情感类 |
| `scene` | 场景图，具体情境 | 生活类、教程类 |
| `minimal` | 极简风格 | 高端定位、设计感 |

#### 维度2：配色 (Palette)

| 配色 | 色系 | 色值参考 | 适用场景 |
|------|------|----------|----------|
| `warm` | 暖色系 | #FF6B35, #F7931A, #FFD23F | 情感、生活、美食 |
| `elegant` | 优雅系 | #2C3E50, #9B59B6, #F1C40F | 商务、高端、文化 |
| `cool` | 冷色系 | #3498DB, #1ABC9C, #2ECC71 | 科技、金融、医疗 |
| `dark` | 深色系 | #1A1A2E, #16213E, #0F3460 | 游戏、夜间、高端 |
| `earth` | 大地色 | #8B4513, #D2691E, #228B22 | 自然、环保、农业 |
| `vivid` | 鲜艳色 | #FF006E, #FB5607, #FFBE0B | 潮流、年轻、活力 |
| `pastel` | 马卡龙 | #FFB5E8, #B5DEFF, #DCD3FF | 女性、儿童、温柔 |
| `mono` | 黑白灰 | #000000, #808080, #FFFFFF | 极简、严肃、经典 |
| `retro` | 复古色 | #C4956A, #A67B5B, #6B4423 | 历史、回忆、经典 |

#### 维度3：渲染风格 (Rendering)

| 风格 | 说明 | 预览特征 |
|------|------|----------|
| `flat-vector` | 扁平矢量 | 简洁线条、纯色块、现代感 |
| `hand-drawn` | 手绘风格 | 温暖线条、有机形状、亲切感 |
| `painterly` | 油画风格 | 笔触可见、艺术感强、质感丰富 |
| `digital` | 数字艺术 | 发光效果、科技线条、未来感 |
| `pixel` | 像素风格 | 复古8位、怀旧游戏、有趣 |
| `chalk` | 粉笔风格 | 教育感、黑板纹理、温暖 |

#### 维度4：文字处理 (Text)

| 方式 | 说明 | 布局特点 |
|------|------|----------|
| `none` | 纯图，无文字 | 视觉主导 |
| `title-only` | 仅标题 | 居中或偏上 |
| `title-subtitle` | 标题+副标题 | 层次分明 |
| `text-rich` | 富文字排版 | 多层次信息 |

#### 维度5：氛围 (Mood)

| 氛围 | 说明 | 情感表达 |
|------|------|----------|
| `subtle` | 含蓄内敛 | 柔和、低调、优雅 |
| `balanced` | 平衡稳重 | 专业、可信、中立 |
| `bold` | 大胆张扬 | 冲击力、醒目、活力 |

**使用示例：**
```
生成封面图：
- 类型：conceptual（概念图）
- 配色：cool（冷色系）
- 渲染：digital（数字艺术）
- 文字：title-only（仅标题）
- 氛围：balanced（平衡）
- 标题："AI 技术趋势 2025"
```

---

### 2. 信息图生成（20×17系统）

**20种布局 × 17种视觉风格**

#### 布局类型 (Layout)

| 布局 | 适用场景 | 特点 |
|------|----------|------|
| `bridge` | 问题-解决方案 | 跨越鸿沟、连接两端 |
| `circular-flow` | 循环、周期 | 圆形流动、闭环 |
| `comparison-table` | 多因素对比 | 表格形式、清晰对比 |
| `do-dont` | 正确/错误做法 | 对比鲜明 |
| `equation` | 公式、输入输出 | 等式结构 |
| `feature-list` | 产品特性 | 列表展示 |
| `fishbone` | 根因分析 | 鱼骨图、因果链 |
| `funnel` | 转化流程 | 漏斗形状、层层筛选 |
| `grid-cards` | 多主题概览 | 网格卡片 |
| `iceberg` | 表面vs隐藏 | 冰山结构 |
| `journey-path` | 客户旅程 | 里程碑、路径 |
| `layers-stack` | 技术栈、层级 | 分层结构 |
| `mind-map` | 头脑风暴 | 发散思维图 |
| `nested-circles` | 影响圈层 | 同心圆 |
| `priority-quadrants` | 优先级矩阵 | 四象限 |
| `pyramid` | 层级结构 | 金字塔 |
| `scale-balance` | 优劣势权衡 | 天平对比 |
| `timeline-horizontal` | 时间线 | 水平时间轴 |
| `tree-hierarchy` | 组织架构 | 树形结构 |
| `venn` | 概念交集 | 韦恩图 |

#### 视觉风格 (Style)

| 风格 | 说明 | 适用场景 |
|------|------|----------|
| `craft-handmade` | 手工纸艺，温暖 | 教育、生活 |
| `claymation` | 3D粘土，趣味 | 儿童、创意 |
| `kawaii` | 日系可爱 | 年轻、轻松 |
| `storybook-watercolor` | 水彩插画 | 文艺、故事 |
| `chalkboard` | 粉笔黑板 | 教育、培训 |
| `cyberpunk-neon` | 赛博朋克 | 科技、未来 |
| `bold-graphic` | 大胆图形 | 潮流、运动 |
| `aged-academia` | 复古学术 | 文化、历史 |
| `corporate-memphis` | 扁平人物 | 企业、商务 |
| `technical-schematic` | 技术蓝图 | 工程、架构 |
| `origami` | 折纸风格 | 创意、设计 |
| `pixel-art` | 像素艺术 | 游戏、复古 |
| `ui-wireframe` | UI线框 | 产品、设计 |
| `subway-map` | 地铁图风格 | 流程、导航 |
| `ikea-manual` | 宜家说明书 | 指南、教程 |
| `knolling` | 整齐平铺 | 展示、分类 |
| `lego-brick` | 乐高积木 | 儿童、趣味 |

**使用示例：**
```
生成信息图：
- 布局：funnel（漏斗）
- 风格：technical-schematic（技术蓝图）
- 内容：用户转化流程
```

---

### 3. 社交卡片/小红书图卡（Style × Layout）

#### 视觉风格 (Style)

| 风格 | 说明 | 适用场景 |
|------|------|----------|
| `cute` | 可爱风 | 萌系、日常 |
| `fresh` | 清新风 | 生活、美食 |
| `warm` | 温暖风 | 情感、治愈 |
| `bold` | 大胆风 | 潮流、个性 |
| `minimal` | 极简风 | 设计、品质 |
| `retro` | 复古风 | 怀旧、经典 |
| `pop` | 波普风 | 活力、年轻 |
| `notion` | Notion风 | 效率、知识 |
| `chalkboard` | 黑板风 | 教育、学习 |

#### 信息密度 (Layout)

| 布局 | 密度 | 适用场景 |
|------|------|----------|
| `sparse` | 1-2点 | 封面、金句 |
| `balanced` | 3-4点 | 常规内容 |
| `dense` | 5-8点 | 知识卡片、速查表 |
| `list` | 4-7项 | 清单、排行 |
| `comparison` | 2边对比 | 前后对比、优劣势 |
| `flow` | 3-6步 | 流程、时间线 |

**使用示例：**
```
生成小红书图卡：
- 风格：notion（效率风）
- 布局：list（列表）
- 内容：5个提升效率的技巧
```

---

### 4. 幻灯片生成（4维系统）

**Texture × Mood × Typography × Density**

#### 纹理 (Texture)

| 纹理 | 说明 |
|------|------|
| `clean` | 干净纯色 |
| `grid` | 网格背景 |
| `organic` | 有机形状 |
| `pixel` | 像素点阵 |
| `paper` | 纸张质感 |

#### 情绪 (Mood)

| 情绪 | 说明 |
|------|------|
| `professional` | 专业正式 |
| `warm` | 温暖亲和 |
| `cool` | 冷静理性 |
| `vibrant` | 活力四射 |
| `dark` | 深沉神秘 |
| `neutral` | 中性平衡 |

#### 排版 (Typography)

| 排版 | 说明 |
|------|------|
| `geometric` | 几何字形 |
| `humanist` | 人文字形 |
| `handwritten` | 手写字体 |
| `editorial` | 编辑风格 |
| `technical` | 技术风格 |

#### 密度 (Density)

| 密度 | 说明 |
|------|------|
| `minimal` | 极简留白 |
| `balanced` | 平衡适中 |
| `dense` | 信息密集 |

**预设组合：**

| 预设 | 组合 | 适用场景 |
|------|------|----------|
| `blueprint` | grid + cool + technical + balanced | 架构、系统设计 |
| `chalkboard` | organic + warm + handwritten + balanced | 教育、教程 |
| `corporate` | clean + professional + geometric + balanced | 商务、提案 |
| `minimal` | clean + neutral + geometric + minimal | 高管汇报 |
| `notion` | clean + neutral + geometric + dense | 产品演示、SaaS |
| `dark-atmospheric` | clean + dark + editorial + balanced | 娱乐、游戏 |

---

### 5. 漫画生成（Art × Tone × Layout）

#### 画风 (Art Style)

| 画风 | 说明 |
|------|------|
| `ligne-claire` | 清晰线条，欧洲漫画（丁丁历险记风格） |
| `manga` | 日式漫画，大眼表现力强 |
| `realistic` | 写实风格，数字绘画 |
| `ink-brush` | 水墨风格，中国风 |
| `chalk` | 粉笔风格，黑板感 |

#### 基调 (Tone)

| 基调 | 说明 |
|------|------|
| `neutral` | 平衡理性，教育性 |
| `warm` | 怀旧温馨，个人化 |
| `dramatic` | 高对比，强烈有力 |
| `romantic` | 柔美梦幻，浪漫元素 |
| `energetic` | 明亮动态，兴奋活力 |
| `vintage` | 历史感，年代真实 |
| `action` | 速度线，冲击效果 |

#### 面板布局 (Layout)

| 布局 | 面板数/页 | 适用场景 |
|------|-----------|----------|
| `standard` | 4-6 | 对话、叙事 |
| `cinematic` | 2-4 | 戏剧时刻、定场 |
| `dense` | 6-9 | 技术解释、时间线 |
| `splash` | 1-2大 | 关键时刻、揭示 |
| `mixed` | 3-7多变 | 复杂叙事 |
| `webtoon` | 3-5竖向 | 移动阅读 |

---

## 使用方式

### 基础用法

```
# 封面图
生成一个科技风格的封面图，标题"AI 技术趋势"

# 信息图
创建一个漏斗布局的信息图，展示用户转化流程

# 小红书卡片
制作一个 Notion 风格的知识卡片，主题是"时间管理"

# 漫画
画一个日式漫画风格的教程，教如何使用 Git
```

### 高级用法（指定维度）

```
# 完整封面图参数
生成封面图：
- 类型：conceptual
- 配色：cool
- 渲染：digital
- 文字：title-only
- 氛围：balanced
- 标题："2025 AI 发展报告"
- 尺寸：900x500

# 完整信息图参数
生成信息图：
- 布局：pyramid
- 风格：corporate-memphis
- 主题：马斯洛需求层次
- 比例：16:9

# 完整幻灯片参数
生成幻灯片：
- 预设：blueprint
- 主题：系统架构设计
- 页数：5
```

---

## 技术实现

### 国内模型 API

#### 智谱 AI GLM-4V（推荐）

```python
import requests

def generate_image_zhipu(prompt, size="1024x1024"):
    """智谱 AI 图像生成"""
    api_key = "your_zhipu_api_key"

    response = requests.post(
        "https://open.bigmodel.cn/api/paas/v4/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "cogview-3-flash",
            "prompt": prompt,
            "size": size
        }
    )
    return response.json()
```

#### 阿里云通义万相

```python
def generate_image_dashscope(prompt, size="1024x1024"):
    """阿里云通义万相"""
    api_key = "your_dashscope_api_key"

    response = requests.post(
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"
        },
        json={
            "model": "wanx-v1",
            "input": {"prompt": prompt},
            "parameters": {"size": size}
        }
    )
    return response.json()
```

#### ModelScope Qwen-Image（默认）

```python
def generate_image_modelscope(prompt, size="1920x1080"):
    """ModelScope Qwen 图像生成"""
    api_key = "your_modelscope_api_key"

    # 提交任务
    response = requests.post(
        "https://api-inference.modelscope.cn/v1/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-ModelScope-Async-Mode": "true"
        },
        json={
            "model": "Qwen/Qwen-Image-2512",
            "prompt": prompt,
            "size": size
        }
    )
    task_id = response.json()["task_id"]

    # 轮询结果
    while True:
        result = requests.get(
            f"https://api-inference.modelscope.cn/v1/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-ModelScope-Task-Type": "image_generation"
            }
        )
        data = result.json()
        if data["task_status"] == "SUCCEED":
            return data["output_images"][0]
        elif data["task_status"] == "FAILED":
            raise Exception("Generation failed")
        time.sleep(5)
```

---

## 提示词增强

### 故事驱动范式

将抽象概念转化为具体可感知的视觉场景：

| 维度 | 旧方式（抽象） | 新方式（故事具象） |
|------|---------------|-------------------|
| 流程图 | 矩形框、箭头 | 森林小径、魔法驿站、浮空岛屿 |
| LOGO | 粗体文字 | 咖啡蒸汽字母、电路板文字、藤蔓编织 |
| 数据图 | 柱状图 | 金币树叶、流量河流、温度树 |
| 海报 | 标题居中 | 电影海报式沉浸场景 |

### 增强元素

| 元素 | 描述 | 示例 |
|------|------|------|
| 视觉风格 | 艺术流派 | 玻璃拟态、新艺术运动 |
| 色彩搭配 | 配色方案 | 青紫渐变、粉桃柔和 |
| 光照效果 | 摄影术语 | 柔和顶光、戏剧侧光 |
| 构图布局 | 动态构图 | 对角线构图、非对称 |
| 质感细节 | 纹理深度 | 玻璃质感、柔和阴影 |

---

## 配置

### 环境变量

```bash
# ~/.image-skill/.env

# 智谱 AI（推荐）
ZHIPU_API_KEY=your_zhipu_api_key

# 阿里云通义万相
DASHSCOPE_API_KEY=your_dashscope_api_key

# ModelScope（默认）
MODELSCOPE_API_KEY=your_modelscope_api_key

# 百度文心（可选）
BAIDU_API_KEY=your_baidu_api_key
BAIDU_SECRET_KEY=your_baidu_secret_key
```

### 分辨率限制

- **最大分辨率**：任何边长不超过 2048px
- **最小分辨率**：任何边长不低于 1024px
- **文字密集场景**：使用 2K (2048px) 分辨率

---

## 输出命名

```
{scene}_{timestamp}_{task_id[:8]}.{format}

示例:
cover_20250215_abc12345.png
infographic_funnel_20250215_def67890.png
xhs_notion_list_20250215_ghi24680.png
```

---

## 版本

- **v0.3.0** - 2026-02 添加章节配图常见问题、Checklist、实战经验
- **v0.2.0** - 添加 baoyu-skills 美学设计系统
- **v0.1.0** - 初始版本，9大场景
- **模型**: Qwen-Image-2512 / 智谱 CogView / 通义万相
- **参考**: [baoyu-skills](https://github.com/JimLiu/baoyu-skills)

---

## 作者

Created for Vaan - 2025

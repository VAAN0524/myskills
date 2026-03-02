---
name: wechat-publisher
description: 微信公众号发文工作流 - 从热点搜索、文章撰写、封面图生成到草稿发布的一站式解决方案
license: MIT
---

# WeChat Publisher

微信公众号发文工作流，从热点搜索到草稿发布的一站式解决方案。

> **⚡ 全自动模式：用户只需提供主题，系统自动完成所有步骤直到上传草稿箱，无需中途确认**

## 内置配置（已配置完成）

```bash
# ~/.wechat-publisher/.env
WECHAT_APP_ID=your_wechat_app_id_here
WECHAT_APP_SECRET=your_wechat_app_secret_here
```

**⚠️ 请将你的微信凭证配置到本地环境变量中，不要提交到 Git**

**获取方式：**
1. 访问 https://developers.weixin.qq.com/platform/
2. 我的业务 → 公众号 → 开发密钥
3. 创建密钥，添加 IP 白名单

---

## When to Apply

- 用户说："帮我发一篇关于XXX的公众号文章"
- 用户说："搜索热点新闻，写一篇公众号文章"
- 用户说："把XXX整理成公众号文章发到草稿箱"
- 用户需要生成微信公众号封面图
- 用户需要将内容发布到公众号草稿箱

## Workflow（全自动执行）

```
用户输入主题 → [自动]搜索热点 → [自动]提炼信息 → [自动]撰写文章 → [自动]生成配图 → [自动]上传草稿箱 → 完成
```

**执行规则：**
1. 用户只需说"帮我写一篇关于XXX的公众号文章"或"搜索热点写文章"
2. **每次任务自动新建文件夹**：`C:\Test\wechat_article_[日期]_[序号]`（如 wechat_article_20260215_001）
3. 系统自动执行所有步骤，中途不询问用户
4. 完成后直接告知草稿已上传，提供media_id

| 步骤 | 执行内容 | 使用工具 |
|------|----------|----------|
| 1. 主题输入 | 用户提供主题或搜索热点 | zhipu-search, ducksearch |
| 2. 信息提炼 | 提取关键信息，构建框架 | AI 分析 |
| 3. 文章撰写 | 按风格撰写完整文章 | AI 写作 |
| 4. 配图生成 | **封面图 + 每章节配图** | Image skill |
| 5. 草稿发布 | 发送到公众号草稿箱 | 微信 API / Playwright |

### 配图生成规则（核心）

**每篇文章必须包含：**
1. **封面图** × 1（900×500）- 传达文章核心主题
2. **章节配图** × N（每个章节一张，1920×1080）- **精准传达章节中心思想**

**配图生成流程（优先使用原文图片）：**
```
Step 0: 从原文爬取技术图片（优先）
搜索参考资料 → 爬取原文中的图片 → 筛选技术参数图/数据图表 → 记录图片逻辑位置

Step 1: 提炼章节中心思想
文章完成 → 逐章节分析 → 用一句话概括该章节要传达的核心观点

Step 2: 中心思想 → 视觉转译
将抽象观点转化为具体可感知的视觉隐喻/场景/符号

Step 3: 生成配图
优先使用原文图片 → 不足部分用 Image skill 生成

Step 4: 图片视觉验证（必须执行）
使用视觉工具检查每张图片 → 验证内容匹配度 → 验证参数正确性 → 不合格则重新生成
```

### 图片视觉验证流程（必须执行）

**触发时机：** 每张图片生成或下载后，必须进行视觉验证

**验证工具：**
- `zhipu-vision` skill - 智谱 GLM-4.6V 视觉分析
- `mcp__4_5v_mcp__analyze_image` - 图像分析工具
- `Read` 工具 - 直接读取本地图片

**验证内容：**

| 验证项 | 检查要点 | 通过标准 |
|--------|----------|----------|
| **内容匹配度** | 图片内容是否与章节主题相关 | 相关度 ≥ 80% |
| **参数正确性** | 数据/数字/参数是否与文章描述一致 | 数据完全一致 |
| **文字可读性** | 图片中的文字是否清晰可读 | 关键文字可识别 |
| **风格一致性** | 图片风格是否与文章整体风格统一 | 风格协调 |
| **图片类型识别** | 是否为技术参数图/数据图/概念图 | 类型明确 |

**验证执行代码：**
```python
# 图片验证流程
def verify_image(image_path, chapter_theme, expected_data=None):
    """
    验证图片是否符合要求

    Args:
        image_path: 图片路径
        chapter_theme: 章节主题/中心思想
        expected_data: 预期的数据/参数（如有）
    """
    # 1. 读取图片
    # 使用 Read 工具或 zhipu-vision 分析

    # 2. 构建验证 prompt
    verify_prompt = f"""
    请分析这张图片，回答以下问题：

    1. 图片内容概述：图片展示了什么？
    2. 与主题匹配度：图片内容是否与"{chapter_theme}"相关？(0-100%)
    3. 图片类型：这是技术参数图、数据图表、概念图还是其他？
    4. 可见数据：图片中显示的具体数字/参数有哪些？
    5. 文字可读性：图片中的关键文字是否清晰？
    6. 建议评分：0-100分，这张图片适合用于该章节吗？
    """

    # 3. 判断是否通过
    # 如果匹配度 < 80% 或数据不一致，需要重新生成
```

**验证报告格式：**
```
## 图片验证报告

| 图片文件 | 章节主题 | 匹配度 | 数据正确性 | 类型 | 评分 | 状态 |
|----------|----------|--------|------------|------|------|------|
| cover.png | 国产大模型对决 | 95% | N/A | 概念图 | 92 | ✓ 通过 |
| chapter02_comparison.png | 五强核心对比 | 70% | 有偏差 | 数据图 | 65 | ✗ 需重做 |

### 问题详情
- chapter02_comparison.png: 数据表中 DeepSeek 参数应显示 37B，实际显示 35B
```

**不通过处理：**
1. **内容不匹配** → 重新生成配图，调整 prompt
2. **参数错误** → 修正 prompt 中的数据，或使用原文图片
3. **文字不清晰** → 提高图片分辨率或更换风格

**原文图片额外验证：**
```
对于从原文爬取的图片，额外检查：
1. 来源URL是否有效
2. 图片是否完整（无截断）
3. 水印/版权标识是否清晰
4. 图片清晰度是否足够（建议 ≥ 720p）
5. 图片中的数据是否与原文描述一致
```

**原文图片爬取规则（重要）：**

```
1. 爬取时机：搜索参考资料时同步执行
2. 目标图片类型：
   - 技术参数对比表（Excel/表格截图）
   - 数据图表（柱状图、折线图、饼图）
   - 架构图/流程图
   - 产品截图/界面图
   - 官方发布的时间线图

3. 图片记录格式：
   ```
   ## 原文图片索引

   | 图片ID | 来源URL | 原文位置 | 图片类型 | 适用章节 | 备注 |
   |--------|---------|----------|----------|----------|------|
   | img_001 | https://xxx | 第3段后 | 参数对比表 | 章节02 | GLM-5参数 |
   | img_002 | https://xxx | 图2 | 架构图 | 章节03 | Agent流程 |
   ```

4. 图片下载与存储：
   - 存储路径：[任务文件夹]/images/source/
   - 命名规则：source_[来源简写]_[序号].png
   - 示例：source_zhipu_001.png

5. 引用逻辑校验：
   - 下载前记录图片在原文中的上下文
   - 确保图片内容与文章章节主题匹配
   - 避免引用错位（如GLM-5的参数图不要用在DeepSeek章节）

6. 图片优先级：
   - 原文技术图 > 官方发布图 > AI生成图
   - 数据准确性 > 视觉美观度
```

**爬取工具：**
```python
# 使用 zhipu-web-reader 或 ducksearch 爬取原文
# 提取图片URL并下载
import requests
from bs4 import BeautifulSoup

def extract_images_from_url(url, save_dir):
    """从URL提取并下载图片"""
    resp = requests.get(url, timeout=30)
    soup = BeautifulSoup(resp.text, 'html.parser')
    images = []

    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src and ('chart' in src.lower() or 'table' in src.lower() or 'param' in src.lower()):
            # 下载图片
            img_data = requests.get(src, timeout=30).content
            filename = f"{save_dir}/source_{len(images)}.png"
            with open(filename, 'wb') as f:
                f.write(img_data)
            images.append({
                'url': src,
                'filename': filename,
                'alt': img.get('alt', ''),
                'context': str(img.parent)[:200]  # 记录上下文
            })

    return images
```

**注意事项：**
- 尊重版权，注明图片来源
- 仅用于学习参考目的
- 如有水印，保持原样不做处理
- 图片清晰度不足时，优先用原图而非重新生成

**章节中心思想提炼模板（必须执行）：**
```
## 章节：[章节标题]

### 中心思想（一句话）
该章节想要传达给读者的核心观点是什么？
例："中美AI竞争已进入白热化阶段，是一场持久的烧钱战"

### 关键信息点
1. [数据/事实1]
2. [数据/事实2]
3. [观点/结论]

### 视觉转译
中心思想 → 视觉隐喻/场景
例："烧钱战" → 天平倾斜 + 金币vs芯片 + 对峙感

### 配图方向
- 类型：comparison / scene / conceptual / metaphor / timeline
- 配色：cool / warm / dark / vivid / pastel
- 风格：digital / flat-vector / minimal / corporate
- 核心元素：[具体视觉元素，3-5个]
- 情绪基调：紧张/希望/思考/活力
```

**视觉转译示例对照表：**

| 中心思想类型 | 视觉转译方向 | 适用场景 |
|-------------|-------------|----------|
| 竞争/对抗 | 天平、棋盘、跑道、对峙剪影 | 商业竞争、市场分析 |
| 崛起/发展 | 上升曲线、萌芽、光球、阶梯 | 行业趋势、企业成长 |
| 选择/多元 | 分叉路口、多彩拼图、多维立方体 | 产品对比、方案分析 |
| 危机/警示 | 悬崖、红色警示、裂痕、阴影 | 风险提示、问题分析 |
| 未来/展望 | 时间线、星空、光路、蓝图 | 趋势预测、战略规划 |
| 伦理/思考 | 天平、镜子、问号、阴阳 | 社会议题、深度思考 |

---

## 1. 主题输入

### 直接提供主题
```
"帮我写一篇关于'AI发展趋势'的公众号文章"
```

### 搜索热点
```
"搜索今日科技热点，写一篇公众号文章"
```

**热点来源优先级：** 微博热搜 → 知乎热榜 → 百度热搜 → 36氪快讯

---

## 2. 信息提炼

搜索相关资料后，输出结构化信息：

```
主题：[主题名称]
核心观点：[一句话总结]
关键信息点：
1. [要点1]
2. [要点2]
3. [要点3]
文章框架：
- 开头：[引入方式]
- 正文：[分段结构]
- 结尾：[升华方式]
```

---

## 3. 图片生成

### 封面图规格

**公众号封面图标准尺寸：**
- **首图文封面**：900 × 500 像素（16:9）
- **次图文封面**：200 × 200 像素（1:1）
- **分享图**：300 × 300 像素

**生成时必须指定尺寸：**
```
Image skill 调用示例：
生成封面图，尺寸 900x500，标题 "XXX"，风格 科技蓝
```

### 封面图（5维系统）

**Type × Palette × Rendering × Text × Mood**

| 维度 | 选项 |
|------|------|
| **Type** | `hero`, `conceptual`, `typography`, `metaphor`, `scene`, `minimal` |
| **Palette** | `warm`, `elegant`, `cool`, `dark`, `earth`, `vivid`, `pastel`, `mono`, `retro` |
| **Rendering** | `flat-vector`, `hand-drawn`, `painterly`, `digital`, `pixel`, `chalk` |
| **Text** | `none`, `title-only`, `title-subtitle`, `text-rich` |
| **Mood** | `subtle`, `balanced`, `bold` |

**推荐组合：**

| 场景 | 推荐配置 |
|------|----------|
| 科技文章 | conceptual + cool + digital + title-only + balanced |
| 情感文章 | scene + warm + hand-drawn + title-subtitle + subtle |
| 商务文章 | minimal + elegant + flat-vector + title-only + balanced |
| 教程文章 | typography + pastel + chalk + text-rich + balanced |

### 配图（Type × Style）

| Type | 说明 | Style 推荐 |
|------|------|-----------|
| `infographic` | 数据图表 | notion, editorial, scientific |
| `flowchart` | 流程步骤 | notion, blueprint |
| `comparison` | 对比图 | notion, editorial |
| `timeline` | 时间线 | notion, watercolor |
| `framework` | 框架图 | blueprint, scientific |

---

## 4. 文章撰写

### 风格选项

| 风格 | 特点 | 适用场景 |
|------|------|----------|
| `专业深度` | 数据详实、逻辑严密 | 行业分析、技术解读 |
| `轻松活泼` | 口语化、有梗 | 娱乐八卦、生活趣事 |
| `情感共鸣` | 走心、引发思考 | 人生感悟、社会热点 |
| `新闻资讯` | 客观、简洁 | 时事新闻、快讯 |
| `干货教程` | 实用、步骤清晰 | 技能分享、指南 |

### 文章结构（自然版，去除AI格式）

**重要：文章结构要自然流畅，不要有模板痕迹**

```markdown
# [标题：15-20字，不要超过64字节]

<br/>

![封面图](images/cover.png)

<br/>

[导语：直接切入，50-100字吸引读者，不要重复标题，不要用"随着..."开头]

<br/>

## 01 [小标题1：有观点，不是泛泛而谈]

<br/>

![配图描述](images/chapter01_xxx.png)

<br/>

[正文：每段2-3行，句子长短结合，有具体数据，有观点态度]

<br/>

## 02 [小标题2：延续上文，自然过渡]

<br/>

![配图描述](images/chapter02_xxx.png)

<br/>

[正文：继续展开，不要用"此外"、"值得注意的是"过渡]

<br/>

## 0N [小标题N：层层递进]

<br/>

![配图描述](images/chapter0N_xxx.png)

<br/>

[正文：深入分析或提出观点]

<br/>

[结语：有态度的总结，不要用"综上所述"，可以提出问题或展望]

<br/>

[参考来源：简洁列出]
[来源1标题]
[来源2标题]
```

**写作要点：**

| 要点 | 说明 |
|------|------|
| 标题 | 15-20字，有吸引力，不含符号 |
| 导语 | 直接切入，不用"随着..."开头 |
| 正文 | 800-2000字，每段2-3行 |
| 过渡 | 自然衔接，不用"此外"、"值得注意的是" |
| 结尾 | 有态度，不用"综上所述" |
| 配图 | 每章节配图占位符 |
| 间距 | 用`<br/>`增加段落间距 |

**⚠️ 格式禁忌：**
- 不要使用`---`分隔线
- 不要使用`*xxx*`星号强调
- 不要使用`※★☆▶●○`等特殊符号
- 不要使用表情符号
- 不要用`> `引用块格式
- 不要连续使用`1. 2. 3.`列表

### 写作风格指南

#### ⚠️ 去AI味规则（必须严格执行）

**核心原则：AI生成的内容必须像真人写的，不能有机器味**

---

##### 一、格式禁忌（AI最爱犯的毛病）

**禁止使用的排版格式：**

| 禁止项 | AI习惯 | 正确做法 |
|--------|--------|----------|
| ❌ Markdown式分隔线 | `---` | 自然段落过渡，用空行 |
| ❌ 多重破折号 | `——`、`——`、`————` | 用逗号、句号分割 |
| ❌ 星号强调 | `*重点*`、`**强调**` | 用「」或直接表达 |
| ❌ 特殊符号 | ※、★、☆、▶、►、●、○ | 纯文字表达 |
| ❌ 箭头指引 | →、→、⇒、➜ | 用"然后"、"接着" |
| ❌ 括号备注 | （注：xxx） | 直接融入正文 |
| ❌ 表情符号 | 🎉、🔥、💡、📌 | 纯文字描述 |
| ❌ 引用块 | `> 引用内容` | 直接写，不用特殊格式 |
| ❌ 代码块 | ```代码``` | 公众号不用代码块 |
| ❌ 过多列表 | 1. 2. 3. 连续使用 | 混合段落叙述 |

**格式改写示例：**

```
❌ AI味太重：
---
## 核心观点
*第一点*：技术突破
*第二点*：市场扩大
※ 注意：以上数据仅供参考

✅ 自然写法：
技术突破和市场扩大是这轮行情的两大推手。需要说明的是，以上数据仅供参考。
```

---

##### 二、词汇禁忌（AI高频词汇黑名单）

**一级禁止词（绝对不用）：**
- ❌ 此外、值得注意的是、需要指出的是、总而言之
- ❌ 至关重要、举足轻重、不可或缺、重中之重
- ❌ 深入探讨、详细分析、全面解析、系统梳理
- ❌ 强调、突出、彰显、体现、诠释
- ❌ 持久的、可持续的、全方位的、多维度的
- ❌ 增强、优化、提升、赋能、助力
- ❌ 无缝、直观、便捷、高效、智能

**二级禁止词（慎用，需替换）：**
| 禁止词 | 替换为 |
|--------|--------|
| 呈现 | 显示、表现、看出 |
| 展现 | 表现、显示、露出 |
| 推动 | 带动、促进、推进 |
| 引领 | 带领、引导、驱动 |
| 打造 | 建设、创建、做成 |
| 聚焦 | 关注、重视、着眼 |
| 依托 | 借助、依靠、基于 |

**句式禁忌：**
- ❌ "作为...的证明"
- ❌ "不仅仅是...而是..."
- ❌ "一方面...另一方面..."
- ❌ "从...角度来看"
- ❌ "在...的大背景下"
- ❌ "毫无疑问..."
- ❌ "众所周知..."

---

##### 三、结构禁忌（AI的模板化写作）

**禁止的开头方式：**
```
❌ "随着...的发展"
❌ "近年来..."
❌ "在当今时代..."
❌ "众所周知..."
❌ "...已经成为..."
```

**禁止的结尾方式：**
```
❌ "综上所述..."
❌ "总而言之..."
❌ "展望未来..."
❌ "可以预见..."
❌ "让我们拭目以待..."
```

**禁止的过渡方式：**
```
❌ "首先...其次...最后..."
❌ "第一...第二...第三..."
❌ "一方面...另一方面..."
❌ "不仅如此..."
❌ "更重要的是..."
```

---

##### 四、自然写作指南（如何像人一样写）

**1. 句子要有变化**
```
❌ AI式（句式单一）：
AI技术在医疗领域有广泛应用。AI技术在教育领域也有应用。AI技术在金融领域同样重要。

✅ 人写式（长短结合）：
AI的触角已经伸到医疗、教育、金融等多个领域。其中医疗诊断的准确率提升了30%，教育场景的个性化程度也大幅提高。
```

**2. 要有观点和态度**
```
❌ AI式（中性陈述）：
某公司发布了新产品，具有多项功能。

✅ 人写式（有态度）：
某公司的新产品把门槛降到了千元以内，这对行业来说是个信号——价格战要开始了。
```

**3. 要有具体细节**
```
❌ AI式（抽象概括）：
该技术取得了显著成效，用户体验得到了大幅提升。

✅ 人写式（具体数据）：
上线三个月，日活从2万涨到15万，用户平均停留时间从3分钟延长到12分钟。
```

**4. 要有口语化表达**
```
❌ AI式（书面语）：
该举措将有效促进企业的数字化转型进程。

✅ 人写式（自然表达）：
这套方案能让企业在半年内完成数字化，比传统方式快了一倍。
```

---

##### 五、风格平衡表

```
专业度：■■■■□（保持4分，不要太学术）
可读性：■■■■■（保持5分，通俗易懂）
口语化：■■■□□（控制在3分，不要土味）
个性化：■■■■□（保持4分，有观点有态度）
格式化：■□□□□（控制在1分，减少符号）
```

---

##### 六、改写示例对照

**示例1：开头段落**
```
❌ AI味：
随着人工智能技术的快速发展，大模型已经成为当今科技领域的重要议题。本文将深入探讨2026年大模型的发展趋势，分析其对各行各业的影响。

✅ 自然版：
2026年刚开年，大模型圈就炸了锅。OpenAI、谷歌、百度轮番发布新品，参数规模从千亿飙到万亿。这场仗打得热闹，但真正值得关注的是——谁能把成本降下来。
```

**示例2：过渡段落**
```
❌ AI味：
此外，值得注意的是，该技术还存在一些挑战。一方面，算力成本居高不下；另一方面，数据质量参差不齐。

✅ 自然版：
技术再好，也得算经济账。现在训练一个千亿模型，电费就要几百万，小公司根本玩不起。数据的问题更棘手——网上扒来的内容，质量能好到哪去？
```

**示例3：结尾段落**
```
❌ AI味：
综上所述，大模型技术在2026年将迎来新的发展机遇。我们相信，随着技术的不断进步，大模型将为人类社会带来更多可能性。让我们拭目以待。

✅ 自然版：
2026年大模型会走向何方？我觉得答案很明确：不是更大的参数，而是更聪明的用法。谁能把成本降到极致，谁就能赢下这一局。
```

---

##### 七、检查清单（发文前必查）

```
□ 没有使用破折号（——）
□ 没有使用星号强调（*xxx*）
□ 没有使用特殊符号（※★☆▶●）
□ 没有使用分隔线（---）
□ 没有使用表情符号（🎉🔥💡）
□ 开头不是"随着..."、"近年来..."
□ 结尾不是"综上所述..."、"让我们..."
□ 没有"此外"、"值得注意的是"
□ 没有"首先其次最后"
□ 句子长短不一，有变化
□ 有具体数据和细节
□ 有观点和态度
□ 读起来像人写的
```

---

## 5. 草稿发布

### Markdown 转微信格式

公众号支持的格式有限，需转换：

| Markdown | 微信格式 |
|----------|----------|
| `# 标题` | H1 样式（居中、大号） |
| `## 小标题` | H2 样式（加粗、蓝色边框） |
| `**粗体**` | 加粗 + 可能变色 |
| `> 引用` | 灰色背景引用框 |
| `---` | 分割线 |
| `列表` | 带图标的列表 |

**转换工具：**
- 使用 `wechat_api.py` 中的 `format_content_for_wechat()` 函数
- 或使用在线工具：https://lab.lyric.im/wxformat/

### 方案选择

| 方案 | 速度 | 要求 |
|------|------|------|
| **API（推荐）** | 快 | AppID + AppSecret |
| **浏览器** | 慢 | Chrome，扫码登录 |
| **手动** | - | 复制粘贴 |

### API 配置

```bash
# ~/.wechat-publisher/.env
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
ZHIPU_API_KEY=your_zhipu_api_key  # 可选，用于搜索
```

**获取凭证：**
1. 访问 https://developers.weixin.qq.com/platform/
2. 我的业务 → 公众号 → 开发密钥
3. 创建密钥，添加 IP 白名单

---

## Usage Examples

### 热点文章
```
用户：搜索今日AI热点，写一篇公众号文章

执行：
1. zhipu-search 搜索 "AI 今日热点"
2. 提取关键信息
3. 生成封面图：conceptual + cool + digital
4. 撰写 1000 字文章
5. 发送到草稿箱
```

### 教程文章
```
用户：帮我写一篇 Python 数据分析入门教程

执行：
1. 搜索教程最佳实践
2. 整理 5 个核心步骤
3. 生成封面图：minimal + cool + blueprint
4. 生成流程图：flowchart + notion
5. 撰写步骤清晰的文章
6. 发送到草稿箱
```

### 仅生成图片
```
用户：为文章《2025 AI 趋势》生成封面图，科技风格

生成：conceptual + cool + digital + title-only + balanced
```

### 仅发布
```
用户：把 article.md 发布到我的公众号

执行：读取文件 → 转换格式 → 上传图片 → 创建草稿
```

---

## 5. 草稿发布（详细流程）

### 发布前检查清单

```
□ 文章已完成，包含封面图和章节配图占位符
□ 封面图已生成（900×500）
□ 所有章节配图已生成（1920×1080）
□ ⚠️ 图片视觉验证已完成（内容匹配度 ≥80%，数据正确性已核对）
□ 图片已上传到微信素材库
□ 文章中的本地图片路径已替换为微信URL
□ 标题不超过20个中文字符（API限制）

【去AI味检查（必须执行）】
□ 没有使用破折号（——）、星号（*）、特殊符号（※★☆▶●○）
□ 没有使用分隔线（---）
□ 没有使用表情符号
□ 开头不是"随着..."、"近年来..."、"在当今..."
□ 结尾不是"综上所述..."、"总而言之..."、"让我们拭目以待"
□ 没有AI高频词（此外、值得注意的是、至关重要、深入探讨）
□ 没有"首先其次最后"模板化过渡
□ 句子长短结合，有节奏变化
□ 有具体数据和细节支撑
□ 有明确的观点和态度
□ 读起来像真人写的，不像机器生成
```

### API 发布流程（完整代码）

```python
import requests
import json
import os

# Step 1: 获取 access_token
def get_access_token(app_id, app_secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    resp = requests.get(url)
    return resp.json()['access_token']

# Step 2: 上传所有图片到素材库
def upload_all_images(access_token, images_dir, image_files):
    """上传所有图片，返回 {key: url} 映射"""
    image_urls = {}
    upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"

    for filename, key in image_files:
        filepath = os.path.join(images_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                files = {'media': (filename, f, 'image/png')}
                resp = requests.post(upload_url, files=files)
            data = resp.json()
            if 'url' in data:
                image_urls[key] = data['url']
                print(f"✓ {filename} uploaded")
    return image_urls

# Step 3: Markdown 转微信 HTML（替换图片URL）
def md_to_wechat_html(md_content, image_urls):
    """将 Markdown 转换为微信支持的 HTML，替换图片路径"""
    lines = md_content.split('\n')
    html_lines = []

    for line in lines:
        # 跳过封面图（单独处理）
        if '![封面图]' in line or '![](images/cover.png)' in line:
            continue

        # 替换章节配图
        for key, url in image_urls.items():
            if f'images/{key}' in line or f'chapter0' in line:
                line = f'<p style="text-align:center;"><img src="{url}" style="max-width:100%;"/></p>'
                break

        # 转换标题
        if line.startswith('# '):
            html_lines.append(f'<h1 style="text-align:center;font-size:22px;">{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2 style="font-size:18px;border-left:4px solid #3498db;padding-left:10px;">{line[3:]}</h2>')
        elif line.startswith('**') and line.endswith('**'):
            html_lines.append(f'<p><strong>{line.strip("*")}</strong></p>')
        elif line.strip():
            html_lines.append(f'<p>{line}</p>')

    return '\n'.join(html_lines)

# Step 4: 创建草稿
def create_draft(access_token, title, cover_media_id, content, digest=''):
    """创建草稿，返回 media_id"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"

    data = {
        'articles': [{
            'title': title,  # 不超过20个中文字符
            'thumb_media_id': cover_media_id,
            'author': '',
            'digest': digest,
            'content': content,
            'content_source_url': '',
            'need_open_comment': 0,
            'only_fans_can_comment': 0
        }]
    }

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    resp = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers=headers)
    return resp.json()

# 完整发布流程
def publish_article(app_id, app_secret, article_md_path, images_dir, image_files, title, digest):
    """完整发布流程"""
    # 1. 获取 token
    token = get_access_token(app_id, app_secret)
    print(f"✓ Access token obtained")

    # 2. 上传所有图片
    image_urls = upload_all_images(token, images_dir, image_files)
    print(f"✓ {len(image_urls)} images uploaded")

    # 3. 读取文章并转换
    with open(article_md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    html_content = md_to_wechat_html(md_content, image_urls)
    print(f"✓ Content converted ({len(html_content)} chars)")

    # 4. 上传封面图获取 media_id
    cover_path = os.path.join(images_dir, 'cover.png')
    with open(cover_path, 'rb') as f:
        files = {'media': ('cover.png', f, 'image/png')}
        resp = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image",
            files=files
        )
    cover_media_id = resp.json()['media_id']
    print(f"✓ Cover uploaded: {cover_media_id}")

    # 5. 创建草稿
    result = create_draft(token, title, cover_media_id, html_content, digest)
    if 'media_id' in result:
        print(f"✓ Draft created: {result['media_id']}")
        return result['media_id']
    else:
        print(f"✗ Failed: {result}")
        return None
```

### API 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 40001 | AppSecret 错误 | 检查密钥是否正确 |
| 40164 | IP 不在白名单 | 在公众号后台添加服务器 IP 到白名单 |
| 45003 | 标题过长 | 标题控制在 20 个中文字符以内 |
| 45004 | 封面图缺失 | 确保 thumb_media_id 有效 |
| 40007 | media_id 无效 | 重新上传图片获取新的 media_id |

### 标题长度注意事项

```
API 限制：标题不超过 64 字节（约 21 个中文字符）

推荐格式：
✓ "2026 AI大变局" (10字符)
✓ "Anthropic估值2.6万亿背后" (13字符)
✗ "2026 AI 大变局：Anthropic估值2.6万亿，京东豪赌机器人，中国AI产业破万亿" (38字符，过长)
```

---

## 经验教训（重要）

### 0. 去AI味写作（2026-02 新增，核心要求）

**问题**：AI生成的文章有明显的机器味，容易被识别

**典型AI味表现：**
- 使用大量符号（※★☆▶●○——）
- Markdown格式痕迹（分隔线、星号强调）
- 模板化开头（"随着...的发展"）
- 模板化结尾（"综上所述"）
- 高频AI词汇（此外、至关重要、深入探讨）
- 句式单一、节奏平淡
- 缺乏观点和态度

**解决方案：严格执行去AI味规则**

```
1. 格式清理：
   - 删除所有特殊符号和表情
   - 删除分隔线（---）
   - 删除星号强调

2. 词汇替换：
   - 扫描AI高频词黑名单
   - 替换为自然表达

3. 结构调整：
   - 开头直接切入，不用模板
   - 结尾有观点，不用总结

4. 风格检查：
   - 句子长短结合
   - 有具体数据细节
   - 有个人观点态度
   - 读起来像人写的
```

**改写口诀：**
```
符号全部删，模板要不得
词汇换自然，句子有节奏
开头别铺垫，结尾有态度
数据要具体，观点要鲜明
```

### 1. 图片视觉验证（2026-02 新增，必须执行）

**问题**：AI生成的图片可能与文章内容不匹配，或数据参数不正确

**解决方案**：每张图片生成后必须进行视觉验证

```
验证流程（必须执行）：
1. 使用 zhipu-vision 或 Read 工具读取图片
2. 分析图片内容是否与章节主题匹配
3. 核对图片中的数据/参数是否与文章描述一致
4. 评估图片类型（技术参数图 vs 概念图 vs 装饰图）
5. 不合格图片需要重新生成或替换

常见问题：
- AI生成的数据图表中数字可能不准确
- 概念图可能与章节中心思想脱节
- 原文爬取的图片可能引用位置错误

解决方案：
- 数据类图片优先从原文爬取
- 概念图需要详细的 prompt 描述
- 验证时核对每一个数字和参数
```

### 1. 标题与正文规范（2026-02 新增）

**标题长度限制：**
```
微信API限制：标题不超过 64 字节（约 21 个中文字符）
推荐长度：15-20 个中文字符为宜

示例：
✓ "2026 AI新物种：具身智能与Agent爆发"（17字符）
✓ "国产大模型五强崛起"（9字符）
✗ "2026 AI新物种：具身智能与Agent爆发，人形机器人市场迎来爆发，智能体经济时代开启"（40+字符，超限）
```

**正文不重复标题：**
```
❌ 错误写法（标题重复出现在正文开头）：
# 2026 AI新物种：具身智能与Agent爆发
2026 AI新物种：具身智能与Agent爆发  ← 重复！

✅ 正确写法（正文直接开始导语）：
# 2026 AI新物种：具身智能与Agent爆发
2026年，AI正在经历一场形态革命...  ← 直接进入内容
```

### 1. 图片上传问题（2026-02 遇到）

**问题**：章节配图显示为本地路径，微信无法访问

**原因**：Markdown 中的 `![](images/xxx.png)` 是本地路径

**解决方案**：
```
1. 先上传所有图片到微信素材库
2. 获取每张图片的微信 URL
3. 在 HTML 内容中替换为微信 URL
4. 然后创建草稿
```

### 2. 配图与章节中心思想脱节

**问题**：配图仅做装饰，没有传达章节核心观点

**解决方案**：严格执行"中心思想→视觉转译"流程
- 每个章节写完后，先提炼中心思想
- 将中心思想转化为视觉隐喻
- 生成精准传达观点的配图

### 3. 写作风格过度口语化

**问题**：使用"炸了"、"卷起来了"等网络用语

**解决方案**：
```
专业度：■■■■□（保持4分）
可读性：■■■■□（保持4分）
口语化：■■□□□（控制在2分）
```

---

## Error Handling

| 错误 | 处理方式 |
|------|----------|
| 搜索失败 | 尝试其他搜索源，或让用户提供资料 |
| 图片生成失败 | 跳过图片，提供占位图 |
| API 发布失败 | 生成 HTML，让用户手动复制 |
| 敏感词触发 | 提示用户修改内容 |
| IP 白名单错误 | 指导用户在公众号后台设置白名单 |
| 标题过长错误 | 自动截断标题到 20 字符以内 |
| 图片路径问题 | 必须先上传图片到素材库再替换 URL |

---

## Related Skills

- `Image` - AI 图像生成
- `zhipu-search` - 智谱 AI 搜索
- `ducksearch` - 网页搜索
- [baoyu-skills](https://github.com/JimLiu/baoyu-skills) - 更专业的发布功能

---

## Quick Reference（一键执行）

```bash
# 🚀 完整流程（推荐，全自动）
"搜索今日AI热点，写一篇公众号文章，配图，发到草稿箱"
"帮我写一篇关于2026 AI趋势的公众号文章，全自动完成"

# 指定风格
"写一篇关于XXX的公众号文章，风格：轻松活泼"

# 仅封面图
"生成封面图：科技风格，冷色调，标题'AI趋势'"

# 仅发布
"把这篇文章发到我的公众号草稿箱"
```

---

## 全自动执行流程（核心）

当用户说"帮我写一篇关于XXX的公众号文章"时，**自动执行以下所有步骤，无需中途确认**：

```
Step 0: 新建任务文件夹
├── 路径：C:\Test\wechat_article_[YYYYMMDD]_[序号]
├── 示例：C:\Test\wechat_article_20260215_001
└── 子目录：images/（存放配图）

Step 1: 搜索/整理信息
├── 使用 zhipu-search 或 ducksearch 搜索相关热点
├── 尝试爬取原文中的技术参数图、数据图表
└── 提取关键信息点

Step 2: 撰写文章（严格执行去AI味规则）
├── 保存到：[任务文件夹]/article.md
├── 按照写作风格指南撰写
├── 标题控制在20字符以内
├── 每个章节预留配图位置
├── ⚠️ 禁止使用：破折号、星号、特殊符号、表情符号
├── ⚠️ 禁止使用：AI高频词汇（此外、至关重要等）
├── ⚠️ 禁止使用：模板化开头和结尾
└── 句子长短结合，有具体数据和观点

Step 2.5: 去AI味检查 ⚠️ 必须
├── 扫描文章中的特殊符号（——、*、※、★、☆、▶、●、○）
├── 扫描AI高频词汇（此外、值得注意的是、至关重要等）
├── 检查开头是否模板化（随着、近年来、在当今）
├── 检查结尾是否模板化（综上所述、总而言之）
├── 检查句子节奏（是否有长短变化）
├── 检查是否有具体数据和观点
└── 不合格则修改，直到通过检查

Step 3: 生成配图
├── 保存到：[任务文件夹]/images/
├── 优先使用从原文爬取的技术图片
├── 封面图：cover.png（900×500）
├── 章节配图：chapter01.png, chapter02.png...（1920×1080）
└── 使用 ModelScope API 或 智谱 CogView API（已配置）

Step 3.5: 图片视觉验证 ⚠️ 必须
├── 使用 zhipu-vision 或 Read 工具分析每张图片
├── 验证内容匹配度（≥80%）
├── 验证数据/参数正确性
├── 不合格图片重新生成或替换
└── 输出验证报告

Step 4: 上传草稿箱
├── 上传所有图片到微信素材库
├── 替换本地路径为微信URL
├── 创建草稿
└── 返回 media_id
```

**完成输出格式：**
```
✅ 文章已完成并上传到草稿箱

📝 标题：[标题]
📊 字数：[字数]
🖼️ 配图：封面图 + [N]张章节配图
🔍 图片验证：[N/N]张通过
🧹 去AI味检查：已通过
📦 草稿 media_id：[media_id]

请登录公众号后台预览和发布。
```

**图片验证报告格式（每次必须输出）：**
```
## 图片验证报告

| 图片文件 | 章节主题 | 匹配度 | 数据正确性 | 类型 | 评分 | 状态 |
|----------|----------|--------|------------|------|------|------|
| cover.png | [主题] | 95% | N/A | 概念图 | 92 | ✓ |
| chapter01_xxx.png | [主题] | 90% | ✓ | 数据图 | 88 | ✓ |
| chapter02_xxx.png | [主题] | 85% | ✓ | 流程图 | 85 | ✓ |

验证通过：[N/N] | 平均匹配度：[X%]
```

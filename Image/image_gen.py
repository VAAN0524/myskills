#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 图像生成 Skill - 基于 ModelScope Qwen-Image-2512
支持流程图、LOGO、海报、数据可视化等多种场景
"""

import requests
import time
import json
import re
from datetime import datetime
from PIL import Image
from io import BytesIO
from typing import Dict, List, Optional, Tuple

# ================================================================
# 配置
# ================================================================

BASE_URL = 'https://api-inference.modelscope.cn/'
API_KEY = "ms-d4cf5deb-8ed7-4016-8899-57f02b00c1b1"
MODEL = "Qwen/Qwen-Image-2512"

MAX_RETRIES = 6
RETRY_DELAY = 10
POLL_INTERVAL = 5

# 分辨率限制
MAX_RESOLUTION = 2048  # 最大分辨率限制为 2K

# ================================================================
# 场景配置
# ================================================================

SCENES = {
    "flowchart": {
        "keywords": ["流程图", "流程", "flowchart", "步骤图", "结构图"],
        "formats": ["png"],
        "default_size": "1920x1080",
        "has_text": True,
        "text_precision": "high",
        "template": "Professional process flowchart visualization displaying '{step_text}'. Overall adopts cinematic tech-style background with gradient from light blue to deep purple from top-left to bottom-right, creating warm golden hour ambiance. The layout features clear visual narrative flow with rich filled content. A horizontal glowing timeline extends from left to right through the center, marked with 'Process Flow' in white. The timeline displays {steps} distinct story moments connected by elegant glowing arrows. Each step features a prominent blue rounded rectangular node label with clear white font inside, displaying the specific step content. Nodes are arranged from left to right in sequential order, each surrounded by significant glowing halo effect. Between nodes, precise connection elements—flowing gradient ribbons, wooden bridges, or brass gears—link each step. Concrete visual metaphors enhance understanding: documents appearing as parchment scrolls, gates transforming into ornate doorways, data flowing as sparkling streams. All labels use clear white font on dark semi-transparent backgrounds for readability. The scene is enriched with environmental details—forest elements, floating islands, or steampunk machinery—creating immersive storybook illustration quality. Frame-filling composition with no empty negative space, fully utilized canvas with rich visual storytelling elements"
    },
    "logo": {
        "keywords": ["logo", "LOGO", "标志", "品牌", "商标", "品牌标识"],
        "formats": ["png"],
        "default_size": "2048x2048",
        "has_text": True,
        "text_precision": "critical",
        "template": "Professional brand logo design prominently displaying '{brand_name}'. Overall adopts modern tech-style background with gradient from bright cyan at center to deep blue at edges, creating premium brand identity atmosphere. The brand name '{brand_name}' is rendered in bold modern typography and positioned heroically at center, featuring gradient overlay effect transitioning from light cyan at top to deep blue at bottom. The text color is bright white for high contrast. The logo incorporates tangible visual metaphors: for coffee brands, craft the name from aromatic steam swirling above a ceramic cup or form letters from coffee beans; for tech companies, build the text from circuit board traces with glowing nodes or sculpt from crystalline geometric forms; for eco brands, weave letters from living vines and leaves. The background features rich decorative elements: flowing light bands extend diagonally, geometric decorative elements balance the composition, circuit board textures add tech feel. The logo is surrounded by significant glowing halo effect and three-dimensional depth. Frame-filling composition with decorative elements occupying all available space, no empty negative areas, fully utilized canvas presenting premium brand identity"
    },
    "poster": {
        "keywords": ["海报", "poster", "宣传", "广告", "宣传页"],
        "formats": ["png", "jpg"],
        "default_size": "1536x2048",
        "has_text": True,
        "text_precision": "critical",
        "template": "Cinematic movie poster promoting '{title}'. Overall adopts dramatic atmospheric background creating immersive visual world. The title '{title}' occupies the upper third of the canvas, rendered in large artistic font with golden color and glowing effect, font style is modern bold, emerging from background—formed by dramatic storm clouds, spelled out by city lights at night, carved into ancient stone ruins, or growing from magical vines. Clouds transmit warm yellow light creating golden hour ambiance. Below the title, subtitle '{subtitle}' is positioned centrally, displayed in medium white font as neon sign, theater marquee, or banner style. The central area showcases '{details}' content through concrete visual storytelling: event details shown as tickets, posters, or maps within the scene, featured objects arranged artfully, people captured in candid moments. Consider the event type—for music festivals: silhouetted crowd against stage lights with lasers; tech conferences: futuristic cityscapes with holographic displays; art exhibitions: gallery with paintings on walls. Bottom third displays event details: time, location, ticket price displayed as clear white font on dark semi-transparent backgrounds. The poster features dramatic lighting creating atmospheric mood, frame-filling composition with rich visual elements, no empty negative space, fully utilized canvas presenting cinematic quality"
    },
    "data_viz": {
        "keywords": ["数据图", "图表", "data visualization", "chart", "图形", "数据可视化", "信息图", "infographic", "对比图", "对比"],
        "formats": ["png"],
        "default_size": "2048x1152",
        "has_text": True,
        "text_precision": "high",
        "template": "Professional infographic comparison chart displaying '{title}'. Overall adopts cinematic tech-style background with smooth gradient transitioning from light blue at top-left corner to deep navy blue at bottom-right corner, creating precise professional atmosphere with uniform soft lighting. The layout features clear visual hierarchy dividing canvas into left and right panels separated by a thin glowing cyan line. Left panel title '{left_title}' displayed inside a prominent light blue rounded rectangular header box with soft glowing edges, centered at the top of left panel, using bold white modern font. Right panel title '{right_title}' displayed inside a prominent beige rounded rectangular header box with soft warm glow, centered at the top of right panel, using bold dark slate gray modern font. All items displayed with detailed photographic realism showing metallic textures, glass transparency, liquid properties, and surface materials. All text labels use clear white font. Visual indicators such as green checkmarks and red X marks feature vibrant colors with soft glowing effects for emphasis. Overall style is modern minimalist design with strong color contrast, frame-filling composition with no empty negative space, fully utilized canvas with rich visual content presenting publication-quality technical illustration"
    },
    "social": {
        "keywords": ["社交媒体", "社交", "social media", "小红书", "朋友圈", "Instagram"],
        "formats": ["png", "jpg"],
        "default_size": "2048x2048",
        "has_text": True,
        "text_precision": "medium",
        "template": "Lifestyle flat lay photography for social media featuring inspirational quote '{main_text}'. Overall adopts soft pastel gradient background creating cozy aspirational atmosphere. The central area prominently displays the quote '{main_text}' incorporated artistically—written on coffee cup with latte foam art, spelled out in letterboard tiles, formed by seashells on sand, appearing on book cover, or created by neon lights. Surrounding the central quote, build an aspirational lifestyle scene creating rich visual narrative: morning coffee setup with pastries and journal on wooden table; workspace setup with laptop, indoor plants, and inspiration board; cozy reading nook with book, soft blanket, and steaming tea; dinner table displaying culinary creation; vanity with beauty products and mirror. Soft natural window light creates gentle shadows throughout scene. Color palette uses pastel tones with warm accents—light pink, light blue, beige, warm yellow. The composition features carefully arranged items filling entire frame, no empty negative space, fully utilized canvas presenting relatable yet artfully arranged lifestyle aesthetic"
    },
    "educational": {
        "keywords": ["教学", "演示", "tutorial", "教学", "讲解", "how-to"],
        "formats": ["png", "jpg"],
        "default_size": "2048x1152",
        "has_text": True,
        "text_precision": "high",
        "template": "Educational comic strip or storyboard teaching '{step1}' through '{step2}' to '{step3}'. Overall adopts clean light background for clear content presentation. The canvas is divided horizontally into three equal-width panels, each displaying an independent step. Left panel (Panel 1) showcases '{step1}' as an active scene with a character performing the action in a relatable setting—someone writing at desk, gardener planting seeds, or chef preparing ingredients. Central panel (Panel 2) advances to '{step2}' showing progress and results—document taking shape, plant sprouting, or ingredients combining. Right panel (Panel 3) completes with '{step3}' showing the outcome—finished document, blooming flower, or completed dish. Panels are connected by smooth flowing arrows or motion lines, arrows pointing from left to right indicating process flow. Each panel top displays large colorful number labels (1, 2, 3), numbers using vibrant colors—red, green, blue—for clear identification. Use friendly cartoon or semi-realistic illustration style, characters showing rich emotion through expressions—determination, effort, satisfaction. Overall color scheme is bright and encouraging, clear visual progression from left to right. Educational yet entertaining like children's book illustrations, frame-filling composition with no empty negative space, fully utilized canvas with rich detailed content"
    },
    "character": {
        "keywords": ["角色", "character", "人物", "人设", "角色设计"],
        "formats": ["png", "jpg"],
        "default_size": "1024x1024",
        "has_text": False,
        "text_precision": "none",
        "template": "Dynamic character concept art showcasing '{description}' character in meaningful action environment. Instead of static standing pose, the character is captured in dynamic moment: warrior mid-swing with sword in motion, hair flowing dynamically, battle-worn armor displaying realistic weathered textures, determined facial expression against dramatic backdrop; mage casting spell with glowing hands, floating arcane symbols around, billowing robes flowing, magical atmosphere filled with particle effects; merchant at market stall arranging goods, customers browsing nearby, warm marketplace ambiance, detailed props and environmental storytelling. Character outfit {outfit} features realistic materials—weathered textures, natural fabric folds, battle damage or wear. Character face reveals personality through expressive details—eyes wide with wonder, brow furrowed with concentration, smile conveying confidence. Soft rim lighting creates depth, background is richly detailed but slightly out of focus to emphasize character. Professional concept art quality for games or stories, frame-filling composition with no empty negative space, fully utilized canvas with rich environmental details"
    },
    "academic": {
        "keywords": ["学术", "论文", "academic", "论文插图", "research", "科学"],
        "formats": ["png"],
        "default_size": "2048x1152",
        "has_text": True,
        "text_precision": "critical",
        "template": "Scientific visualization diagram bringing '{subject}' to life through tangible 3D modeling or artistic cross-section. Overall adopts professional deep blue gradient background from top-left to bottom-right, creating calm precise scientific atmosphere. Central area displays the subject structure in detailed form: biological structures shown as layered 3D models with cutaway views revealing internal workings, cells as colorful floating orbs with detailed organelles visible; geological formations presented as dramatic landscape cross-sections with underground layers exposed and labeled with pointer lines; mechanical systems displayed as exploded 3D diagrams with components separated and connected by elegant lines; astronomical phenomena rendered as deep space scenes with accurate celestial bodies. Each structural part is connected to labels through elegant thin pointer lines, labels displayed as clear white font on dark semi-transparent backgrounds for readability. Labels use precise terminology and professional typography. Rendered with photorealistic 3D quality or artistic scientific illustration style, soft natural lighting illuminating key features, professional color palette featuring teal and slate blue accents, richly detailed background filled with scientific elements, no empty negative space, fully utilized canvas presenting publication-quality visualization"
    },
    "illustration": {
        "keywords": ["插图", "配图", "illustration", "文章图", "博客配图"],
        "formats": ["png", "jpg"],
        "default_size": "1920x1080",
        "has_text": False,
        "text_precision": "low",
        "template": "Conceptual illustration using creative visual metaphor '{visual_metaphor}' to represent '{topic}' theme. Overall adopts inviting gradient background supporting warm storytelling atmosphere. The central area displays the metaphor transformed into tangible, story-driven scene. Instead of abstract symbols, create concrete imaginative scenarios: for 'growth', show magical treehouse growing upward with new rooms continuously appearing; for 'innovation', depict lightbulb factory with glowing bulbs being crafted on assembly line; for 'collaboration', illustrate diverse hands building structure together; for 'security', present fortress with warm hearth visible inside. Each metaphor rendered as rich detailed environment containing storytelling elements—characters, objects, atmospheric effects. Scene features distinct foreground, middle ground, and background layers creating depth. Warm storytelling lighting creates inviting mood. Color palette is vibrant and welcoming. Art style ranges from storybook illustration to concept art depending on theme. Editorial presentation quality with narrative depth, frame-filling composition with no empty negative space, fully utilized canvas with rich visual and decorative elements"
    }
}

# 精确提示词示例库（参考结构化提示词写法）
PROMPT_EXAMPLES = {
    "flowchart": """这是一张现代科技感的流程图幻灯片，展示用户认证流程。整体采用深蓝色渐变背景，从左上到右下由淡蓝色渐变为深紫色。中央区域一条水平延伸的发光时间轴，轴线中间写着"认证流程"。时间轴上从左向右排列4个醒目的蓝色圆角矩形节点标签，标签内为清晰白色字体：节点1写着"用户提交注册信息"、节点2写着"系统发送验证邮件"、节点3写着"用户点击验证链接"、节点4写着"认证成功账号激活"。每个节点通过精致的发光箭头连接，箭头从左指向右。节点周围有显著的光晕效果，背景中有淡淡的电路板纹理装饰。整个画面充满元素，无大量留白。""",

    "logo": """这是一张品牌Logo设计图，展示品牌名称"{brand_name}"。整体采用深色渐变背景，从中央向四周由亮青色渐变为深蓝色。品牌名称"{brand_name}"以粗体现代字体居中展示，字体颜色为亮白色，带有精致的渐变叠加效果——从顶部的淡青色渐变到底部的深蓝色。文字周围环绕着科技感的电路板纹理和发光节点装饰。背景左侧有流动的光带从左下向右上延伸，右侧有几何装饰元素平衡构图。整体呈现高端科技感，Logo带有显著的光晕和立体感，画面充满装饰元素无留白。""",

    "poster": """这是一张电影风格的海报，标题"{title}"占据画面上方三分之一区域。标题采用大号艺术字体，颜色为金色，带有发光效果，字体样式现代粗体，从背景中浮现——由戏剧性的风暴云层构成，云层间透出暖黄色光芒。副标题"{subtitle}"位于标题下方，以中号白色字体展示，呈霓虹灯牌样式。画面中央区域展示"{details}"的具体内容：以电影票根、海报或地图形式呈现，周围有人物剪影和生活场景。底部三分之一区域展示活动详情：时间、地点、票价等信息以清晰白色字体排列在深色半透明背景板上。整体采用电影海报式构图，戏剧性照明营造氛围感，画面充满视觉元素无留白。""",

    "data_viz": """这是一张创意数据可视化图表，展示{y_label}与{x_label}的关系。整体采用柔和渐变背景，从上方的淡青色渐变到下方的淡蓝色。图表中央区域展示具体实物隐喻：销售数据以生长树木形式呈现，树叶为金色硬币；流量数据以流动河流形式展示，河流中有小船承载访问者。横轴{x_label}以醒目白色字体标注在底部，纵轴{y_label}以竖排白色字体标注在左侧。数据分类'{categories}'以具体图标表示——建筑、车辆、动物或相关物体。数值通过具体量感展示——金币堆叠高度、水位刻度线、角色等级进度条。所有数据标签以清晰白色字体显示在深色半透明背景板上，便于阅读。采用信息图风格，既有教育意义又富有趣味性，画面充满视觉元素无留白。""",

    "social": """这是一张生活方式风格的社交媒体图文，展示引语"{main_text}"。整体采用平铺摄影视角，模拟精心布置的桌面场景。中央区域展示引语"{main_text}"，以艺术方式融入——写在咖啡杯的奶泡上、拼字板瓷砖中、沙滩上的贝壳排列、书封面上的文字，或霓虹灯构成。周围构建向往的生活场景：早晨咖啡配甜点和日记本；工作台有笔记本电脑、绿植和灵感板；阅读角有书籍、毯子和茶饮；晚餐桌上的烹饪作品；梳妆台的美妆用品和镜子。整体采用柔和自然窗光，营造温暖阴影。色彩采用柔和色调配合暖色点缀——浅粉色、淡蓝色、米白色、暖黄色。画面充满精心布置的物品，呈现生活方式感，无大量留白。""",

    "educational": """这是一张教育风格的漫画条带，展示从'{step1}'到'{step2}'再到'{step3}'的学习过程。整体采用白色背景，便于清晰展示内容。画面横向分为三个等宽面板，每个面板独立展示一个步骤。左侧面板（面板1）展示'{step1}'：角色在相关场景中执行动作——有人在桌前书写、园丁播种种子、厨师准备食材。中央面板（面板2）展示'{step2}'：展示进展和结果——文档初具形态、植物发芽、食材混合。右侧面板（面板3）展示'{step3}'：展示最终成果——完成的文档、盛开的鲜花、完成的菜肴。面板之间用流畅的箭头或动作线连接，箭头从左指向右表示流程。每个面板顶部以大号彩色数字标签（1、2、3）标记，数字颜色鲜艳——红色、绿色、蓝色。采用友好的卡通或半写实插画风格，角色表情丰富，展示情绪和努力。整体色彩明亮鼓励，清晰视觉进展从左到右，既有教育意义又有趣味，画面充满内容无留白。""",

    "character": """这是一张角色概念设计图，展示'{description}'角色的生动形象。角色放置在有意义的环境中揭示其故事背景。不是静态站立，而是展示动态动作：战士挥剑中途，剑在运动中，头发飘逸，姿态充满动感，战损装甲和坚定表情衬托戏剧性背景；法师施法时双手发光，漂浮的奥术符号，飘逸的长袍，魔法氛围伴随粒子特效；商人在市场摊位整理货物，顾客浏览，温暖市场氛围，细致道具和环境叙事。服装{outfit}呈现风化纹理、褶皱和真实材质。角色面部通过表情展示个性——眼睛睁大表示惊奇、眉头皱起表示专注、微笑传递自信。柔和轮廓光营造深度，背景细节丰富略失焦，营造专业游戏或故事概念艺术效果。画面充满角色和环境细节，无大量留白。""",

    "academic": """这是一张科学可视化图表，展示'{subject}'的具体结构。整体采用深蓝色渐变背景，从左上到右下由淡蓝色渐变为深紫色。图表中央展示主体结构：生物结构以分层3D模型形式呈现，带切视图揭示内部运作；细胞以彩色浮动球体形式展示，细胞器细节清晰；地质构造以戏剧性景观剖面形式展示，地下层暴露并标注；机械系统以爆炸3D图解形式展示，组件分离并用线连接。每个结构部分通过优雅的指针线连接到标签，标签以清晰白色字体显示在深蓝色半透明背景板上，便于阅读。标注内容具体详实，使用专业术语。整体采用3D渲染质量或艺术科学插画风格，柔和自然光照，专业配色方案以青色和板岩蓝色为点缀，背景丰富充满元素无留白。""",

    "illustration": """这是一张概念插图，通过创意视觉隐喻'{visual_metaphor}'展示'{topic}'主题。整体采用故事驱动场景，充满具体视觉元素：成长展示为向上生长的魔法树屋，新房间不断出现；创新展示为灯泡工厂，发光灯泡正在制造；协作展示为多样双手共同建设；安全展示为带温暖壁炉的堡垒。每个隐喻渲染为丰富详细环境，包含故事元素——角色、物体、氛围。采用温暖故事照明，邀请性配色方案，艺术风格从故事书插画到概念艺术范围，编辑质量伴随叙事深度。画面前景、中景、背景层次分明，充满视觉细节和装饰元素，无大量留白。"""
}


# 通用修饰词（艺术风格库）
COMMON_MODIFIERS = {
    "style": [
        "modern flat design with depth",
        "glassmorphism with soft shadows",
        "Memphis design style with geometric shapes",
        "art nouveau inspired with flowing lines",
        "minimalist luxury aesthetic",
        "playful and whimsical illustration",
        "vintage retro with modern twist",
        "futuristic tech with gradients",
        "editorial illustration style",
        "lifestyle photography feel"
    ],
    "color_scheme": [
        "teal to purple gradient",
        "coral and sage accents",
        "soft pink to peach gradient",
        "blue to green harmonious",
        "vibrant primary with pop accents",
        "muted earth tones natural",
        "electric coral to teal",
        "pastel soft with depth",
        "monochrome with color accent",
        "warm sunset golden hour"
    ],
    "quality": [
        "4K resolution quality",
        "professional publication ready",
        "high-end advertising quality",
        "editorial magazine quality",
        "clean and sharp with texture",
        "detailed with artistic flair",
        "polished and refined"
    ],
    "lighting": [
        "soft natural window light",
        "dramatic side lighting",
        "golden hour glow",
        "studio lighting with rim highlights",
        "soft diffused lighting from above",
        "atmospheric mood lighting"
    ],
    "composition": [
        "dynamic diagonal flow",
        "asymmetric modern layout",
        "rule of thirds composition",
        "centered with decorative elements",
        "floating elements with depth",
        "frame-filling composition with no empty negative space",
        "fully utilized canvas with rich visual content",
        "tight composition maximizing image area"
    ]
}


# ================================================================
# 核心类
# ================================================================

class ImageGenerator:
    """AI 图像生成器"""

    def __init__(self):
        self.base_url = BASE_URL
        self.api_key = API_KEY
        self.model = MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def detect_scene(self, user_input: str) -> Tuple[str, Dict]:
        """
        检测场景类型

        Args:
            user_input: 用户输入

        Returns:
            (scene_name, scene_config)
        """
        user_input_lower = user_input.lower()

        # 优先级排序（更具体的场景优先）
        scene_priority = [
            "logo", "poster", "flowchart", "data_viz", "social",
            "educational", "character", "academic", "illustration"
        ]

        for scene_name in scene_priority:
            scene = SCENES[scene_name]
            for keyword in scene["keywords"]:
                if keyword.lower() in user_input_lower:
                    return scene_name, scene

        # 默认返回插图场景
        return "illustration", SCENES["illustration"]

    def extract_params(self, user_input: str, scene_config: Dict) -> Dict:
        """
        从用户输入中提取参数

        Args:
            user_input: 用户输入
            scene_config: 场景配置

        Returns:
            提取的参数字典
        """
        params = {}

        # 提取尺寸（带分辨率限制：最短边 >= 1024，最长边 <= 2048）
        size_pattern = r'(\d+)x(\d+)'
        size_match = re.search(size_pattern, user_input)
        if size_match:
            width = int(size_match.group(1))
            height = int(size_match.group(2))

            # 最大分辨率限制：最长边不超过 2048
            max_dim = max(width, height)
            if max_dim > MAX_RESOLUTION:
                scale = MAX_RESOLUTION / max_dim
                width = int(width * scale)
                height = int(height * scale)

            # 最小分辨率限制：最短边不低于 1024
            min_dim = min(width, height)
            if min_dim < 1024:
                scale = 1024 / min_dim
                width = int(width * scale)
                height = int(height * scale)

            # 再次检查最大分辨率（可能因最小分辨率调整而超限）
            max_dim = max(width, height)
            if max_dim > MAX_RESOLUTION:
                scale = MAX_RESOLUTION / max_dim
                width = int(width * scale)
                height = int(height * scale)

            # 确保最小值为 1
            width = max(1, width)
            height = max(1, height)

            params["size"] = f"{width}x{height}"
        else:
            params["size"] = scene_config["default_size"]

        # 提取品牌名称（LOGO 场景）
        brand_patterns = [
            r'(?:名称|叫|named?)[:\s]+"?([^"\']+)"?',
            r'(?:名称|叫|name)[\:：]\s*["\']?([^"\']+)["\']?',
            r'(?:logo|标志)[^\w]*["\']?([^"\']+)["\']?'
        ]
        for pattern in brand_patterns:
            if brand_match := re.search(pattern, user_input, re.IGNORECASE):
                if brand_match.group(1):
                    brand_name = brand_match.group(1).strip()
                    if brand_name and brand_name not in ["logo", "标志"]:
                        params["brand_name"] = brand_name
                        break

        # 提取标题（海报场景）
        title_patterns = [
            r'标题[:]\s*["\']?([^"\']+)["\']?',
            r'title[:]\s*["\']?([^"\']+)["\']?'
        ]
        for pattern in title_patterns:
            if title_match := re.search(pattern, user_input):
                params["title"] = title_match.group(1)
                break

        # 提取颜色
        color_pattern = r'(黑色|白色|红色|蓝色|绿色|黄色|紫色|橙色|粉色|灰色|棕色)系?'
        if color_match := re.search(color_pattern, user_input):
            color_map = {
                "黑色": "black", "白色": "white", "红色": "red",
                "蓝色": "blue", "绿色": "green", "黄色": "yellow",
                "紫色": "purple", "橙色": "orange", "粉色": "pink",
                "灰色": "gray", "棕色": "brown"
            }
            params["color"] = color_map.get(color_match.group(1), "blue")

        # 提取风格
        style_keywords = {
            "极简": "minimalist", "简约": "minimalist",
            "现代": "modern", "复古": "vintage retro",
            "可爱": "playful and fun", "专业": "professional business"
        }
        for keyword, style in style_keywords.items():
            if keyword in user_input:
                params["style"] = style
                break

        return params

    def build_prompt(self, user_input: str, scene_name: str, scene_config: Dict, params: Dict) -> str:
        """
        构建增强的提示词

        Args:
            user_input: 用户输入
            scene_name: 场景名称
            scene_config: 场景配置
            params: 提取的参数

        Returns:
            增强后的提示词
        """
        template = scene_config["template"]

        # 基础填充
        replacements = {
            "text_color": params.get("color", "black"),
            "bg_color": "white",
            "bg_style": "clean solid color",
            "background_style": "clean solid color",
            "title_color": params.get("color", "black"),
            "subtitle_color": "gray",
            "body_color": "dark gray",
            "brand_name": params.get("brand_name", "BRAND"),
            "title": params.get("title", "TITLE"),
            "subtitle": "Subtitle",
            "details": "Details",
            "main_text": "Main Text",
            "steps": "4",
            "step_text": user_input,
            "step_count": "4",
            "step1": "First step",
            "step2": "Second step",
            "step3": "Third step",
            "x_label": "X Axis",
            "y_label": "Y Axis",
            "categories": "Categories",
            "description": user_input,
            "outfit": "modern clothing",
            "topic": user_input,
            "visual_metaphor": "abstract",
            "subject": user_input
        }

        # 根据场景特殊处理
        if scene_name == "flowchart":
            # 尝试提取流程步骤
            if "、" in user_input or "，" in user_input:
                steps = re.split(r'[、,，]', user_input)
                replacements["step_text"] = " | ".join(f'"{s.strip()}"' for s in steps if s.strip())
                replacements["steps"] = str(len([s for s in steps if s.strip()]))
            else:
                replacements["step_text"] = f'"{user_input}"'

        elif scene_name == "poster":
            if not params.get("title"):
                replacements["title"] = "主标题"
            replacements["subtitle"] = "副标题或时间地点"
            replacements["details"] = "详细内容描述"

        elif scene_name == "data_viz":
            replacements["x_label"] = "类别"
            replacements["y_label"] = "数值"
            replacements["categories"] = "数据类别"

        elif scene_name == "character":
            replacements["description"] = user_input

        elif scene_name == "illustration":
            replacements["topic"] = user_input

        # 添加风格修饰
        style = params.get("style", "professional business style")
        template = template + f", {style}"

        # 替换模板变量
        try:
            prompt = template.format(**replacements)
        except KeyError as e:
            # 缺少变量时使用基础模板
            prompt = f"{user_input}, professional design, high quality"

        return prompt

    def get_output_format(self, scene_config: Dict, params: Dict) -> str:
        """
        获取输出格式

        Args:
            scene_config: 场景配置
            params: 参数

        Returns:
            文件格式 (png, jpg, svg)
        """
        formats = scene_config["formats"]
        return formats[0]  # 返回第一个（优先）格式

    def generate(self, user_input: str) -> Dict:
        """
        生成图像

        Args:
            user_input: 用户输入

        Returns:
            生成结果字典
        """
        # 1. 检测场景
        scene_name, scene_config = self.detect_scene(user_input)
        print(f"[Scene] {scene_name}")

        # 2. 提取参数
        params = self.extract_params(user_input, scene_config)
        print(f"[Params] {params}")

        # 3. 构建提示词
        prompt = self.build_prompt(user_input, scene_name, scene_config, params)
        print(f"[Prompt] {prompt[:200]}...")

        # 4. 获取输出格式
        output_format = self.get_output_format(scene_config, params)
        print(f"[Format] {output_format}")

        # 5. 调用 API
        return self._call_api(prompt, scene_name, output_format, params)

    def _call_api(self, prompt: str, scene_name: str, output_format: str, params: Dict) -> Dict:
        """
        调用 ModelScope API

        Args:
            prompt: 提示词
            scene_name: 场景名称
            output_format: 输出格式
            params: 参数

        Returns:
            生成结果
        """
        # 提交任务
        for attempt in range(MAX_RETRIES):
            try:
                print(f"[API] Submitting task... (attempt {attempt + 1}/{MAX_RETRIES})")

                response = requests.post(
                    f"{self.base_url}v1/images/generations",
                    headers={**self.headers, "X-ModelScope-Async-Mode": "true"},
                    data=json.dumps({
                        "model": self.model,
                        "prompt": prompt
                    }, ensure_ascii=False).encode('utf-8'),
                    timeout=30
                )
                response.raise_for_status()

                task_id = response.json()["task_id"]
                print(f"[OK] Task submitted: {task_id}")

                # 轮询结果
                return self._poll_result(task_id, scene_name, output_format, params)

            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_DELAY * (attempt + 1)
                    print(f"[WARN] Request failed, retrying in {wait_time}s... ({e})")
                    time.sleep(wait_time)
                else:
                    return {
                        "success": False,
                        "error": str(e)
                    }

    def _poll_result(self, task_id: str, scene_name: str, output_format: str, params: Dict) -> Dict:
        """
        轮询任务结果

        Args:
            task_id: 任务 ID
            scene_name: 场景名称
            output_format: 输出格式
            params: 参数

        Returns:
            生成结果
        """
        print(f"[POLL] Waiting for generation...")

        while True:
            try:
                result = requests.get(
                    f"{self.base_url}v1/tasks/{task_id}",
                    headers={**self.headers, "X-ModelScope-Task-Type": "image_generation"},
                    timeout=30
                )
                result.raise_for_status()

                data = result.json()
                task_status = data["task_status"]

                if task_status == "SUCCEED":
                    print(f"[OK] Generation completed!")
                    # 下载图片
                    return self._download_image(data["output_images"][0], scene_name, task_id, output_format)

                elif task_status == "FAILED":
                    error_msg = data.get("error", "Unknown error")
                    print(f"[ERROR] Generation failed: {error_msg}")
                    return {
                        "success": False,
                        "error": error_msg
                    }

                else:
                    # PENDING 或 PROCESSING
                    print(f"[POLL] Status: {task_status}, waiting {POLL_INTERVAL}s...")
                    time.sleep(POLL_INTERVAL)

            except requests.exceptions.RequestException as e:
                print(f"[WARN] Query failed: {e}, continuing...")
                time.sleep(POLL_INTERVAL)

    def _download_image(self, image_url: str, scene_name: str, task_id: str, output_format: str) -> Dict:
        """
        下载图片

        Args:
            image_url: 图片 URL
            scene_name: 场景名称
            task_id: 任务 ID
            output_format: 输出格式

        Returns:
            下载结果
        """
        try:
            print(f"[DOWNLOAD] Downloading image...")

            response = requests.get(image_url, timeout=60)
            response.raise_for_status()

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            short_id = task_id[:8]
            filename = f"{scene_name}_{timestamp}_{short_id}.{output_format}"

            # 保存图片
            image = Image.open(BytesIO(response.content))

            # 转换格式（如果需要）
            if output_format == "jpg":
                image = image.convert("RGB")
                filename = filename.replace("jpg", "jpeg")

            image.save(filename)
            file_size = len(response.content) / 1024  # KB

            print(f"[SAVE] Image saved: {filename} ({file_size:.1f} KB)")

            return {
                "success": True,
                "filename": filename,
                "size": file_size,
                "dimensions": image.size,
                "task_id": task_id
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# ================================================================
# CLI 接口
# ================================================================

def main():
    """主函数 - CLI 接口"""
    import sys
    import io

    # 设置 UTF-8 编码输出（Windows 兼容）
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    if len(sys.argv) < 2:
        print("Usage: python image_gen.py 'your description'")
        print("Example: python image_gen.py 'generate a user login flowchart'")
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])

    print("=" * 60)
    print("[Image Gen] AI Image Generation Skill")
    print("=" * 60)
    print(f"[Input] {user_input}")
    print("-" * 60)

    generator = ImageGenerator()
    result = generator.generate(user_input)

    print("-" * 60)

    if result["success"]:
        print("[SUCCESS] Generation completed!")
        print(f"[File] {result['filename']}")
        print(f"[Size] {result['dimensions'][0]} x {result['dimensions'][1]}")
        print(f"[Storage] {result['size']:.1f} KB")
    else:
        print(f"[ERROR] {result['error']}")


if __name__ == "__main__":
    main()

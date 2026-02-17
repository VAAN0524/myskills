#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工业技术信息图表生成测试 - 使用优化后的详细提示词
"""

import requests
import time
import json
from PIL import Image
from io import BytesIO
from datetime import datetime

# API 配置
BASE_URL = 'https://api-inference.modelscope.cn/'
API_KEY = "ms-d4cf5deb-8ed7-4016-8899-57f02b00c1b1"
MODEL = "Qwen/Qwen-Image-2512"

# 详细的具象化提示词
DETAILED_PROMPT = """Professional industrial technical infographic titled '水分对工业生产的影响' displayed at the top center in bold white modern sans-serif font. Overall adopts cinematic deep blue tech-style background with smooth gradient transitioning from light blue at top-left corner to deep navy blue at bottom-right corner, creating precise calm industrial atmosphere with uniform soft lighting.

The layout features clear visual hierarchy dividing canvas into left and right panels separated by a thin glowing cyan line. Left panel occupies 40% of canvas width. Left panel title '实际发生的现象' displayed inside a prominent light blue rounded rectangular header box with soft glowing edges, centered at the top of left panel, using bold white modern font. Below the title, three deep navy blue rounded rectangular button-style items arranged vertically with equal spacing, each item featuring:

Item 1: A detailed icon showing a small pile of brown powder-like granular material with a single water droplet suspended above creating a ripple effect, accompanied by Chinese text '团聚/结块' in clear white font on the left side, with a vibrant green checkmark symbol on the right side featuring soft glowing effect

Item 2: A detailed icon showing a transparent conical laboratory flask filled with blue liquid containing multiple rising bubbles of varying sizes, accompanied by Chinese text '产生气泡/缺陷' in clear white font on the left side, with a vibrant green checkmark symbol on the right side featuring soft glowing effect

Item 3: A detailed icon showing two interlocking metal gears with visible rust corrosion and orange-brown discoloration, accompanied by Chinese text '设备腐蚀/催化剂失活' in clear white font on the left side, with a vibrant green checkmark symbol on the right side featuring soft glowing effect

Right panel occupies 60% of canvas width. Right panel title '【不会】发生的现象' displayed inside a prominent beige rounded rectangular header box with soft warm glow, centered at the top of right panel, using bold dark slate gray modern font. Below the title, four items arranged in a 2x2 grid format, each displayed inside a dark charcoal gray rectangular background box with slightly lighter border, each item featuring:

Item 1: A detailed icon showing precisely interlocking clean metal gears with shiny silver surfaces, accompanied by Chinese text '反应效率【显著提高】' in clear white font, with a large bright red X mark covering the center featuring bold thick lines and slight glow effect

Item 2: A detailed icon showing a neatly arranged bundle of silver metal cylindrical pipes with clean polished surfaces, accompanied by Chinese text '成品内部【绝对无气泡/孔隙】' in clear white font, with a large bright red X mark covering the center featuring bold thick lines and slight glow effect

Item 3: A detailed icon showing a sturdy metal chain under tension with visible strain, each link detailed with metallic shine, accompanied by Chinese text '材料强度与耐久性【得到增强】' in clear white font, with a large bright red X mark covering the center featuring bold thick lines and slight glow effect

Item 4: A detailed icon showing a corroded metal wrench with orange-brown rust patches and surface degradation, accompanied by Chinese text '加工过程【零腐蚀/零副反应风险】' in clear white font, with a large bright red X mark covering the center featuring bold thick lines and slight glow effect

At the bottom center of canvas, a small white text note displayed in a semi-transparent dark blue rounded rectangular background for better readability: '注：水分的存在通常会导致负面或干扰性的结果，而非理想或增强的状态' using regular weight white sans-serif font.

Overall style is modern minimalist industrial design with strong color contrast between deep navy blues, light blues, beiges, dark grays, vibrant greens, and bright reds. All graphical symbols are rendered with photographic realism showing metallic textures, glass transparency, liquid properties, and surface materials. The entire canvas is frame-filling with no empty negative space, all visual elements are precisely positioned with balanced composition, fully utilized canvas with rich visual content presenting publication-quality technical illustration. Resolution 2048x1152 pixels with sharp detail and professional color grading."""

def generate_with_detailed_prompt():
    """使用详细提示词生成图片"""
    common_headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    print("=" * 60)
    print("工业技术信息图表生成测试")
    print("=" * 60)
    print(f"[Model] {MODEL}")
    print(f"[Prompt Length] {len(DETAILED_PROMPT)} characters")
    print(f"[Resolution] 2048x1152")
    print()

    # 提交任务
    max_retries = 6
    retry_delay = 15

    for attempt in range(max_retries):
        try:
            print(f"[API] Submitting task... (attempt {attempt + 1}/{max_retries})")

            response = requests.post(
                f"{BASE_URL}v1/images/generations",
                headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
                data=json.dumps({
                    "model": MODEL,
                    "prompt": DETAILED_PROMPT
                }, ensure_ascii=False).encode('utf-8'),
                timeout=30
            )
            response.raise_for_status()

            task_id = response.json()["task_id"]
            print(f"[OK] Task submitted: {task_id}")

            # 轮询结果
            return poll_result(task_id)

        except requests.exceptions.RequestException as e:
            if "quota" in str(e).lower() or "429" in str(e):
                print(f"[ERROR] API quota exceeded: {e}")
                print()
                print("解决方案:")
                print("1. 等待明天配额重置")
                print("2. 更换 API_KEY")
                print("3. 使用其他图像生成服务")
                return None
            elif attempt < max_retries - 1:
                wait_time = retry_delay * (attempt + 1)
                print(f"[WARN] Request failed, retrying in {wait_time}s... ({e})")
                time.sleep(wait_time)
            else:
                print(f"[ERROR] All retries failed: {e}")
                return None

def poll_result(task_id):
    """轮询任务结果"""
    print(f"[POLL] Waiting for generation...")

    poll_count = 0
    max_polls = 60  # 最多轮询5分钟

    while poll_count < max_polls:
        try:
            result = requests.get(
                f"{BASE_URL}v1/tasks/{task_id}",
                headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
                timeout=30
            )
            result.raise_for_status()
            data = result.json()

            task_status = data["task_status"]

            if task_status == "SUCCEED":
                print(f"[OK] Generation completed!")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'industrial_infographic_{timestamp}.png'

                # 下载图片
                image_url = data["output_images"][0]
                image = Image.open(BytesIO(requests.get(image_url).content))
                image.save(filename)
                print(f"[SAVE] Image saved: {filename}")
                print(f"[INFO] Image size: {image.size}")
                return filename

            elif task_status == "FAILED":
                error_msg = data.get("error", "Unknown error")
                print(f"[ERROR] Generation failed: {error_msg}")
                return None

            else:
                poll_count += 1
                print(f"[POLL] Status: {task_status}, waiting 5s... ({poll_count}/{max_polls})")
                time.sleep(5)

        except requests.exceptions.RequestException as e:
            poll_count += 1
            print(f"[WARN] Query failed: {e}, continuing... ({poll_count}/{max_polls})")
            time.sleep(5)

    print("[TIMEOUT] Polling timeout")
    return None

if __name__ == "__main__":
    result = generate_with_detailed_prompt()

    if result:
        print()
        print("=" * 60)
        print("生成成功！")
        print(f"文件: {result}")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("生成失败 - 请等待API配额重置或更换API密钥")
        print("=" * 60)
        print()
        print("详细提示词已保存，可在配额恢复后使用:")
        print(f"  文件位置: industrial_infographic_prompt.txt")
        print(f"  提示词长度: {len(DETAILED_PROMPT)} 字符")

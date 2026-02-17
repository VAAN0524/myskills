# -*- coding: utf-8 -*-
"""
微信公众号 API 封装
支持通过 wx.limyai.com 或微信官方 API 发布草稿
"""

import os
import json
import requests
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class WeChatConfig:
    """微信配置"""
    # wx.limyai.com API（推荐，更简单）
    limyai_api_key: Optional[str] = None

    # 微信官方 API（需要认证的服务号）
    app_id: Optional[str] = None
    app_secret: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'WeChatConfig':
        """从环境变量加载配置"""
        return cls(
            limyai_api_key=os.getenv('LIMYAI_API_KEY'),
            app_id=os.getenv('WECHAT_APP_ID'),
            app_secret=os.getenv('WECHAT_APP_SECRET')
        )

    @property
    def has_limyai(self) -> bool:
        return bool(self.limyai_api_key)

    @property
    def has_official_api(self) -> bool:
        return bool(self.app_id and self.app_secret)


class WeChatPublisher:
    """微信公众号发布器"""

    LIMYAI_API_URL = "https://wx.limyai.com/api/v1"
    WECHAT_API_URL = "https://api.weixin.qq.com/cgi-bin"

    def __init__(self, config: Optional[WeChatConfig] = None):
        self.config = config or WeChatConfig.from_env()
        self._access_token: Optional[str] = None

    def publish_draft(
        self,
        title: str,
        content: str,
        cover_url: Optional[str] = None,
        author: str = "",
        digest: str = "",
        content_source_url: str = "",
        need_open_comment: int = 0
    ) -> Dict:
        """
        发布文章到草稿箱

        Args:
            title: 文章标题（必填，最长64字）
            content: 文章内容，HTML格式（必填）
            cover_url: 封面图片URL
            author: 作者名称
            digest: 摘要（不填则自动截取正文前54字）
            content_source_url: 原文链接
            need_open_comment: 是否打开评论（0否，1是）

        Returns:
            API 响应结果
        """
        if self.config.has_limyai:
            return self._publish_via_limyai(
                title, content, cover_url, author, digest
            )
        elif self.config.has_official_api:
            return self._publish_via_official(
                title, content, cover_url, author, digest,
                content_source_url, need_open_comment
            )
        else:
            return {
                "success": False,
                "error": "NO_API_CONFIG",
                "message": "请配置 LIMYAI_API_KEY 或 WECHAT_APP_ID + WECHAT_APP_SECRET"
            }

    def _publish_via_limyai(
        self,
        title: str,
        content: str,
        cover_url: Optional[str],
        author: str,
        digest: str
    ) -> Dict:
        """通过 wx.limyai.com API 发布"""
        try:
            response = requests.post(
                f"{self.LIMYAI_API_URL}/draft/add",
                headers={
                    "Authorization": f"Bearer {self.config.limyai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "articles": [{
                        "title": title,
                        "author": author,
                        "digest": digest,
                        "content": content,
                        "thumb_url": cover_url,
                        "need_open_comment": 0
                    }]
                },
                timeout=30
            )
            result = response.json()

            if result.get("errcode", 0) == 0:
                return {
                    "success": True,
                    "media_id": result.get("media_id"),
                    "message": "草稿创建成功"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("errmsg", "Unknown error"),
                    "code": result.get("errcode")
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _publish_via_official(
        self,
        title: str,
        content: str,
        cover_url: Optional[str],
        author: str,
        digest: str,
        content_source_url: str,
        need_open_comment: int
    ) -> Dict:
        """通过微信官方 API 发布"""
        try:
            # 1. 获取 access_token
            token = self._get_access_token()
            if not token:
                return {"success": False, "error": "获取 access_token 失败"}

            # 2. 上传封面图片获取 media_id
            thumb_media_id = None
            if cover_url:
                thumb_media_id = self._upload_image(token, cover_url)

            # 3. 创建草稿
            response = requests.post(
                f"{self.WECHAT_API_URL}/draft/add?access_token={token}",
                json={
                    "articles": [{
                        "title": title,
                        "author": author,
                        "digest": digest,
                        "content": content,
                        "thumb_media_id": thumb_media_id,
                        "content_source_url": content_source_url,
                        "need_open_comment": need_open_comment
                    }]
                },
                timeout=30
            )
            result = response.json()

            if result.get("errcode", 0) == 0:
                return {
                    "success": True,
                    "media_id": result.get("media_id"),
                    "message": "草稿创建成功"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("errmsg", "Unknown error"),
                    "code": result.get("errcode")
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _get_access_token(self) -> Optional[str]:
        """获取微信 access_token"""
        if self._access_token:
            return self._access_token

        try:
            response = requests.get(
                f"{self.WECHAT_API_URL}/token",
                params={
                    "grant_type": "client_credential",
                    "appid": self.config.app_id,
                    "secret": self.config.app_secret
                },
                timeout=10
            )
            result = response.json()
            if "access_token" in result:
                self._access_token = result["access_token"]
                return self._access_token
        except:
            pass
        return None

    def _upload_image(self, token: str, image_url: str) -> Optional[str]:
        """上传图片获取 media_id"""
        try:
            # 下载图片
            img_response = requests.get(image_url, timeout=30)
            img_data = img_response.content

            # 上传到微信
            response = requests.post(
                f"{self.WECHAT_API_URL}/media/upload?access_token={token}&type=thumb",
                files={"media": ("cover.jpg", img_data, "image/jpeg")},
                timeout=30
            )
            result = response.json()
            return result.get("media_id")
        except:
            return None


def format_content_for_wechat(markdown_content: str) -> str:
    """
    将 Markdown 内容转换为微信公众号支持的 HTML 格式

    Args:
        markdown_content: Markdown 格式的内容

    Returns:
        微信公众号支持的 HTML 格式内容
    """
    import re

    html = markdown_content

    # 标题转换
    html = re.sub(r'^### (.+)$', r'<h3 style="margin: 20px 0 10px; font-size: 16px; font-weight: bold;">\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2 style="margin: 25px 0 15px; font-size: 18px; font-weight: bold; border-left: 4px solid #3b82f6; padding-left: 10px;">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1 style="margin: 30px 0 20px; font-size: 22px; font-weight: bold; text-align: center;">\1</h1>', html, flags=re.MULTILINE)

    # 分割线
    html = re.sub(r'^---$', r'<hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">', html, flags=re.MULTILINE)

    # 粗体和斜体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # 链接
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3b82f6;">\1</a>', html)

    # 引用块
    html = re.sub(r'^> (.+)$', r'<blockquote style="border-left: 4px solid #d1d5db; padding: 10px 15px; margin: 15px 0; background: #f9fafb; color: #6b7280;">\1</blockquote>', html, flags=re.MULTILINE)

    # 列表
    html = re.sub(r'^- (.+)$', r'<li style="margin: 8px 0;">\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li.*</li>\n?)+', r'<ul style="padding-left: 20px;">\g<0></ul>', html)

    # 段落
    lines = html.split('\n')
    processed_lines = []
    in_paragraph = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_paragraph:
                processed_lines.append('</p>')
                in_paragraph = False
            continue

        # 检查是否是块级元素
        if stripped.startswith('<h') or stripped.startswith('<hr') or stripped.startswith('<ul') or stripped.startswith('<li') or stripped.startswith('<block') or stripped.startswith('</'):
            if in_paragraph:
                processed_lines.append('</p>')
                in_paragraph = False
            processed_lines.append(stripped)
        else:
            if not in_paragraph:
                processed_lines.append('<p style="margin: 12px 0; line-height: 1.8; color: #374151;">')
                in_paragraph = True
            processed_lines.append(stripped)

    if in_paragraph:
        processed_lines.append('</p>')

    # 包装在容器中
    final_html = f'''
<section style="padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 15px; line-height: 1.8; color: #374151;">
{''.join(processed_lines)}
</section>
'''

    return final_html


# 使用示例
if __name__ == "__main__":
    # 初始化发布器
    publisher = WeChatPublisher()

    # 示例内容
    title = "测试文章标题"
    content = """
# 这是一个测试文章

这是文章的导语部分，用于吸引读者。

## 第一部分

这是正文内容，**重点内容加粗**。

> 这是一段引用

- 要点一
- 要点二

## 第二部分

更多内容...
"""

    # 转换并发布
    html_content = format_content_for_wechat(content)
    result = publisher.publish_draft(
        title=title,
        content=html_content,
        author="作者名",
        digest="这是文章摘要"
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))

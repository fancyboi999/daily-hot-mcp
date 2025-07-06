"""RSS解析模块"""

import feedparser
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin
from .http import http_client


async def parse_rss(url: str) -> List[Dict[str, Any]]:
    """解析RSS源"""
    try:
        # 获取RSS内容
        response = await http_client.get(url)
        response.raise_for_status()
        
        # 解析RSS
        feed = feedparser.parse(response.text)
        
        if not feed.entries:
            return []
        
        results = []
        for entry in feed.entries:
            item = {
                "title": getattr(entry, "title", ""),
                "description": getattr(entry, "summary", ""),
                "link": getattr(entry, "link", ""),
                "author": getattr(entry, "author", ""),
                "publish_time": getattr(entry, "published", ""),
            }
            
            # 处理封面图片
            cover = None
            if hasattr(entry, "media_content") and entry.media_content:
                cover = entry.media_content[0].get("url")
            elif hasattr(entry, "enclosures") and entry.enclosures:
                for enclosure in entry.enclosures:
                    if enclosure.get("type", "").startswith("image/"):
                        cover = enclosure.get("href")
                        break
            
            if cover:
                item["cover"] = cover
            
            results.append(item)
        
        return results
    
    except Exception as e:
        raise Exception(f"解析RSS失败: {str(e)}")


async def get_rss_items(url: str) -> List[Dict[str, Any]]:
    """获取RSS条目（parse_rss的别名）"""
    return await parse_rss(url)


async def get_rss(url: str) -> Dict[str, Any]:
    """获取原始RSS数据"""
    try:
        # 获取RSS内容
        response = await http_client.get(url)
        response.raise_for_status()
        
        # 解析RSS
        feed_data = feedparser.parse(response.text)
        
        # 转换为字典格式
        result = {
            "feed": {
                "title": getattr(feed_data.feed, "title", ""),
                "description": getattr(feed_data.feed, "description", ""),
                "link": getattr(feed_data.feed, "link", ""),
                "entry": []
            }
        }
        
        # 添加条目
        for entry in feed_data.entries:
            entry_dict = {
                "title": getattr(entry, "title", ""),
                "summary": getattr(entry, "summary", ""),
                "link": getattr(entry, "link", ""),
                "id": getattr(entry, "id", ""),
                "published": getattr(entry, "published", ""),
                "author": getattr(entry, "author", ""),
            }
            result["feed"]["entry"].append(entry_dict)
        
        return result
    
    except Exception as e:
        raise Exception(f"获取RSS数据失败: {str(e)}") 
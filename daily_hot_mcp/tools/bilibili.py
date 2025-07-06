"""哔哩哔哩视频排行榜工具"""

import asyncio
import hashlib
import time
from datetime import datetime
from typing import Annotated
from pydantic import Field
from daily_hot_mcp.utils import http_client, cache, logger
from fastmcp.tools import Tool

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

def encode_wbi(params: dict, img_key: str, sub_key: str) -> str:
    """编码WBI签名"""
    params_with_ts = {**params, "wts": str(int(time.time()))}
    sorted_params = sorted(params_with_ts.items())
    query_parts = []
    for key, value in sorted_params:
        clean_value = str(value).replace("!", "").replace("'", "").replace("(", "").replace(")", "").replace("*", "")
        query_parts.append(f"{key}={clean_value}")
    query_string = "&".join(query_parts)
    mixin_key_order = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
        33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61,
        26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36,
        20, 34, 44, 52
    ]
    full_key = img_key + sub_key
    mixin_key = "".join([full_key[i] if i < len(full_key) else "" for i in mixin_key_order])[:32]
    sign_input = query_string + mixin_key
    w_rid = hashlib.md5(sign_input.encode()).hexdigest()
    return f"{query_string}&w_rid={w_rid}"

async def get_wbi_keys():
    """获取WBI密钥"""
    response = await http_client.get(
        "https://api.bilibili.com/x/web-interface/nav",
        headers={
            "Cookie": "SESSDATA=xxxxxx",
            "User-Agent": USER_AGENT,
            "Referer": "https://www.bilibili.com/",
        }
    )
    response.raise_for_status()
    data = response.json()
    wbi_img = data.get("data", {}).get("wbi_img", {})
    img_url = wbi_img.get("img_url", "")
    sub_url = wbi_img.get("sub_url", "")
    def get_filename_from_url(url):
        return url.split("/")[-1].split(".")[0] if url else ""
    return {
        "img_key": get_filename_from_url(img_url),
        "sub_key": get_filename_from_url(sub_url),
    }

async def get_bili_wbi() -> str:
    """获取B站WBI签名"""
    cache_key = "bilibili-wbi"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    try:
        keys = await get_wbi_keys()
        params = {"foo": "114", "bar": "514", "baz": "1919810"}
        query = encode_wbi(params, keys["img_key"], keys["sub_key"])
        cache.set(cache_key, query)
        return query
    except Exception:
        return "foo=114&bar=514&baz=1919810&wts=" + str(int(time.time()))

async def get_bilibili_rank_main(rank_type: int) -> list:
    """主要的B站排行榜获取方法"""
    wbi_data = await get_bili_wbi()
    headers = {
        "Referer": "https://www.bilibili.com/ranking/all",
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    response = await http_client.get(
        f"https://api.bilibili.com/x/web-interface/ranking/v2?rid={rank_type}&type=all&{wbi_data}",
        headers=headers
    )
    response.raise_for_status()
    data = response.json()
    if data.get("code") != 0:
        raise Exception(data.get("message", "获取B站排行榜失败"))
    results = []
    for item in data.get("data", {}).get("list", []):
        publish_time_iso = None
        if item.get("pubdate"):
            try:
                publish_time_iso = datetime.fromtimestamp(item["pubdate"]).isoformat()
            except (ValueError, TypeError):
                pass
        result_item = {
            "title": item.get("title", ""),
            "description": item.get("desc") or "该视频暂无简介",
            "cover": item.get("pic", ""),
            "author": item.get("owner", {}).get("name", ""),
            "view": item.get("stat", {}).get("view", 0),
        }
        if publish_time_iso:
            result_item["publishTime"] = publish_time_iso
        if item.get("short_link_v2"):
            result_item["link"] = item["short_link_v2"]
        elif item.get("bvid"):
            result_item["link"] = f"https://www.bilibili.com/video/{item['bvid']}"
        results.append(result_item)
    return results

async def get_bilibili_rank_backup(rank_type: int) -> list:
    """备用的B站排行榜获取方法"""
    response = await http_client.get(
        f"https://api.bilibili.com/x/web-interface/ranking?jsonp=jsonp?rid={rank_type}&type=all&callback=__jp0",
        headers={
            "Referer": "https://www.bilibili.com/ranking/all",
            "User-Agent": USER_AGENT,
        }
    )
    response.raise_for_status()
    data = response.json()
    if data.get("code") != 0:
        raise Exception(data.get("message", "获取B站排行榜失败"))
    results = []
    for item in data.get("data", {}).get("list", []):
        result_item = {
            "title": item.get("title", ""),
            "description": item.get("desc") or "该视频暂无简介",
            "cover": item.get("pic", ""),
            "author": item.get("author", ""),
            "view": item.get("video_review", 0),
        }
        if item.get("bvid"):
            result_item["link"] = f"https://www.bilibili.com/video/{item['bvid']}"
        results.append(result_item)
    return results

async def get_bilibili_rank_func(
    rank_type: Annotated[int, Field(description="排行榜分区：0(全站), 1(动画), 3(音乐), 4(游戏), 5(娱乐), 188(科技), 119(鬼畜), 129(舞蹈), 155(时尚), 160(生活), 168(国创相关), 181(影视)")] = 0
) -> list:
    """获取哔哩哔哩排行榜数据"""
    valid_types = [0, 1, 3, 4, 5, 188, 119, 129, 155, 160, 168, 181]
    if rank_type not in valid_types:
        raise ValueError(f"不支持的排行榜类型: {rank_type}")
    try:
        return await get_bilibili_rank_main(rank_type)
    except Exception as e:
        logger.error(f"主要方法失败: {str(e)}")
        return await get_bilibili_rank_backup(rank_type)

bilibili_rank_tool = Tool.from_function(
    fn=get_bilibili_rank_func,
    name="get-bilibili-rank",
    description="获取哔哩哔哩视频排行榜，包含全站、动画、音乐、游戏等多个分区的热门视频，反映当下年轻人的内容消费趋势",
)

async def get_bilibili_trending_func() -> list:
    """Get Bilibili trending videos."""
    cache_key = "bilibili_trending"
    try:
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info("从缓存获取哔哩哔哩热榜数据")
            return cached_data
        url = "https://api.bilibili.com/x/web-interface/popular"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
        }
        response = await http_client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(f"API返回错误: {data.get('message', '未知错误')}")
        videos = data.get("data", {}).get("list", [])
        trending_data = []
        for i, video in enumerate(videos[:20], 1):  # Top 20
            item = {
                "rank": i,
                "title": video.get("title", ""),
                "author": video.get("owner", {}).get("name", ""),
                "view_count": video.get("stat", {}).get("view", 0),
                "like_count": video.get("stat", {}).get("like", 0),
                "url": video.get("short_link_v2", ""),
                "duration": video.get("duration", 0),
                "cover": video.get("pic", ""),
                "pubdate": video.get("pubdate", 0)
            }
            trending_data.append(item)
        cache.set(cache_key, trending_data)
        logger.info(f"获取哔哩哔哩热榜数据成功，共{len(trending_data)}条")
        return trending_data
    except Exception as e:
        logger.error(f"获取哔哩哔哩热榜数据失败: {str(e)}")
        raise

bilibili_trending_tool = Tool.from_function(
    fn=get_bilibili_trending_func,
    name="get-bilibili-trending",
    description="获取哔哩哔哩热门视频",
)

bilibili_hot_tools = [
    bilibili_rank_tool,
    bilibili_trending_tool
]

def main():
    result = asyncio.run(get_bilibili_rank_func(rank_type=155))
    # result = asyncio.run(get_bilibili_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

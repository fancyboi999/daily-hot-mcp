"""抖音热搜工具"""

import asyncio
import re
from datetime import datetime
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool

async def get_csrf_token() -> str:
    """获取CSRF Token"""
    try:
        response = await http_client.get(
            "https://www.douyin.com/passport/general/login_guiding_strategy/",
            params={"aid": 6383}
        )
        response.raise_for_status()
        set_cookie = response.headers.get("set-cookie", "")
        pattern = r"passport_csrf_token=([^;]*); Path"
        match = re.search(pattern, set_cookie)
        return match.group(1) if match else ""
    except Exception:
        return ""

async def get_douyin_trending_func() -> list:
    """获取抖音热搜榜数据"""
    csrf_token = await get_csrf_token()
    headers = {}
    if csrf_token:
        headers["Cookie"] = f"passport_csrf_token={csrf_token}"
    response = await http_client.get(
        "https://www.douyin.com/aweme/v1/web/hot/search/list/",
        params={
            "device_platform": "webapp",
            "aid": 6383,
            "channel": "channel_pc_web",
            "detail_list": 1,
        },
        headers=headers
    )
    response.raise_for_status()
    data = response.json()
    if data.get("status_code") != 0 or not isinstance(data.get("data", {}).get("word_list"), list):
        raise Exception("获取抖音热榜失败")
    results = []
    for item in data["data"]["word_list"]:
        event_time_iso = None
        if item.get("event_time"):
            try:
                event_time_iso = datetime.fromtimestamp(item["event_time"]).isoformat()
            except (ValueError, TypeError):
                pass
        result_item = {
            "title": item.get("word", ""),
            "popularity": item.get("hot_value", 0),
        }
        if event_time_iso:
            result_item["eventTime"] = event_time_iso
        word_cover = item.get("word_cover", {})
        url_list = word_cover.get("url_list", [])
        if url_list:
            result_item["cover"] = url_list[0]
        if item.get("sentence_id"):
            result_item["link"] = f"https://www.douyin.com/hot/{item['sentence_id']}"
        results.append(result_item)
    return results

douyin_trending_tool = Tool.from_function(
    fn=get_douyin_trending_func,
    name="get-douyin-trending",
    description="获取抖音热搜榜单，展示当下最热门的社会话题、娱乐事件、网络热点和流行趋势",
)

douyin_hot_tools = [
    douyin_trending_tool
]

def main():
    result = asyncio.run(get_douyin_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

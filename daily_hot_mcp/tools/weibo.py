"""微博热搜工具"""

import asyncio
from urllib.parse import urlencode
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool


async def get_weibo_trending_func() -> list:
    """获取微博热搜榜数据"""
    response = await http_client.get("https://weibo.com/ajax/side/hotSearch")
    response.raise_for_status()
    
    data = response.json()
    if data.get("ok") != 1 or not isinstance(data.get("data", {}).get("realtime"), list):
        raise Exception("获取微博热搜榜失败")
    
    results = []
    for item in data["data"]["realtime"]:
        if item.get("is_ad") == 1:
            continue
            
        key = item.get("word_scheme") or f"#{item.get('word')}"
        
        # 构建搜索URL
        params = {
            "q": key,
            "band_rank": "1",
            "Refer": "top"
        }
        link = f"https://s.weibo.com/weibo?{urlencode(params)}"
        
        results.append({
            "title": item.get("word", ""),
            "description": item.get("note") or key,
            "popularity": item.get("num", ""),
            "link": link,
        })
    
    return results


weibo_tool_config = Tool.from_function(
    fn=get_weibo_trending_func,
    name="get-weibo-trending",
    description="获取微博热搜榜，包含时事热点、社会现象、娱乐新闻、明星动态及网络热议话题的实时热门中文资讯",
)

weibo_hot_tools = [
    weibo_tool_config
]

def main():
    result = asyncio.run(get_weibo_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

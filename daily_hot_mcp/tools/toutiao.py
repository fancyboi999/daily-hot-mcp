"""今日头条热榜工具"""

import asyncio
from urllib.parse import urlparse, urlunparse
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool


async def get_toutiao_trending_func() -> list:
    """获取今日头条热榜数据"""
    response = await http_client.get(
        "https://www.toutiao.com/hot-event/hot-board/",
        params={"origin": "toutiao_pc"}
    )
    response.raise_for_status()
    
    data = response.json()
    if not isinstance(data.get("data"), list):
        raise Exception("获取今日头条热榜失败")
    
    results = []
    for item in data["data"]:
        # 清理URL参数
        parsed_url = urlparse(item["Url"])
        clean_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            "", "", ""
        ))
        
        results.append({
            "title": item["Title"],
            "cover": item["Image"]["url"],
            "popularity": item["HotValue"],
            "link": clean_url,
        })
    
    return results


toutiao_tool_config = Tool.from_function(
    fn=get_toutiao_trending_func,
    name="get-toutiao-trending",
    description="获取今日头条热榜，包含时政要闻、社会事件、国际新闻、科技发展及娱乐八卦等多领域的热门中文资讯",
)

toutiao_hot_tools = [
    toutiao_tool_config
]

def main():
    result = asyncio.run(get_toutiao_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

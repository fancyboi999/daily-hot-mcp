"""网易新闻热点榜工具"""

import asyncio
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool


async def get_netease_news_trending_func() -> list:
    """获取网易新闻热点榜数据"""
    response = await http_client.get("https://m.163.com/fe/api/hot/news/flow")
    response.raise_for_status()
    
    data = response.json()
    if data.get("code") != 200 or not isinstance(data.get("data", {}).get("list"), list):
        raise Exception("获取网易新闻热点榜失败")
    
    results = []
    for item in data["data"]["list"]:
        result_item = {
            "title": item.get("title", ""),
            "cover": item.get("imgsrc", ""),
            "source": item.get("source", ""),
            "publish_time": item.get("ptime", ""),
            "link": item.get("url", ""),
        }
        results.append(result_item)
    
    return results


netease_news_tool_config = Tool.from_function(
    fn=get_netease_news_trending_func,
    name="get-netease-news-trending",
    description="获取网易新闻热点榜，包含时政要闻、社会事件、财经资讯、科技动态及娱乐体育的全方位中文新闻资讯",
)

netease_news_hot_tools = [
    netease_news_tool_config
]

def main():
    result = asyncio.run(get_netease_news_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

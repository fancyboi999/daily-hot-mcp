"""腾讯新闻热点榜工具"""

import asyncio
from pydantic import Field
from typing import Annotated
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool


async def get_tencent_news_trending_func(
    page_size: Annotated[int, Field(description="返回结果数量")] = 20
) -> list:
    """获取腾讯新闻热点榜数据"""
    response = await http_client.get(
        "https://r.inews.qq.com/gw/event/hot_ranking_list",
        params={"page_size": page_size}
    )
    response.raise_for_status()
    
    data = response.json()
    if data.get("ret") != 0 or not isinstance(data.get("idlist", [{}])[0].get("newslist"), list):
        raise Exception("获取腾讯新闻热点榜失败")
    
    newslist = data["idlist"][0]["newslist"]
    # 过滤掉第一个元素（通常是标题）
    filtered_newslist = newslist[1:] if len(newslist) > 1 else newslist
    
    results = []
    for item in filtered_newslist:
        result_item = {
            "title": item.get("title", ""),
            "description": item.get("abstract", ""),
            "source": item.get("source", ""),
            "publish_time": item.get("time", ""),
            "link": item.get("url", ""),
        }
        
        # 获取封面图片
        thumbnails = item.get("thumbnails", [])
        if thumbnails:
            result_item["cover"] = thumbnails[0]
        
        # 获取热度分数
        hot_event = item.get("hotEvent", {})
        if hot_event.get("hotScore"):
            result_item["popularity"] = hot_event["hotScore"]
        
        results.append(result_item)
    
    return results


tencent_news_tool_config = Tool.from_function(
    fn=get_tencent_news_trending_func,
    name="get-tencent-news-trending",
    description="获取腾讯新闻热点榜，包含国内外时事、社会热点、财经资讯、娱乐动态及体育赛事的综合性中文新闻资讯",
)

tencent_news_hot_tools = [
    tencent_news_tool_config
]

def main():
    result = asyncio.run(get_tencent_news_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

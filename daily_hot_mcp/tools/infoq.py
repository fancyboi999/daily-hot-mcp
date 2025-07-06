"""InfoQ技术资讯工具"""

import asyncio
from typing import Annotated
from pydantic import Field
from daily_hot_mcp.utils.rss import parse_rss
from fastmcp.tools import Tool

async def get_infoq_news_func(
    region: Annotated[str, Field(description="地区选择：cn(中文版), global(国际版)")] = "cn"
) -> list:
    """获取InfoQ技术资讯数据"""
    url_map = {
        "cn": "https://www.infoq.cn/feed",
        "global": "https://feed.infoq.com/",
    }
    if region not in url_map:
        raise ValueError(f"不支持的地区: {region}")
    url = url_map[region]
    items = await parse_rss(url)
    if region == "cn":
        for item in items:
            if "description" in item:
                del item["description"]
    return items

infoq_news_tool = Tool.from_function(
    fn=get_infoq_news_func,
    name="get-infoq-news",
    description="获取 InfoQ 技术资讯，包含软件开发、架构设计、云计算、AI等企业级技术内容和前沿开发者动态",
)

infoq_hot_tools = [
    infoq_news_tool
]

def main():
    result = asyncio.run(get_infoq_news_func(region="global"))
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

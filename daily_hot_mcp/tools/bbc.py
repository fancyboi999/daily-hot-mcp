"""BBC新闻工具"""

import asyncio
from typing import Annotated
from pydantic import Field
from daily_hot_mcp.utils.rss import parse_rss
from fastmcp.tools import Tool

def build_bbc_url(category: str = "", edition: str = "") -> str:
    """构建BBC RSS URL"""
    url = "https://feeds.bbci.co.uk/news/"
    if category:
        url += f"{category}/"
    url += "rss.xml"
    if edition:
        url += f"?edition={edition}"
    return url

async def get_bbc_news_func(
    category: Annotated[str, Field(description="新闻分类：''(热门), world(国际), uk(英国), business(商业), politics(政治), health(健康), education(教育), science_and_environment(科学与环境), technology(科技), entertainment_and_arts(娱乐与艺术)")] = "",
    edition: Annotated[str, Field(description="版本：''(默认), uk(英国), us(美国和加拿大), int(世界其他地区)，仅对category为空时有效")] = ""
) -> list:
    """获取BBC新闻数据"""
    valid_categories = [
        "", "world", "uk", "business", "politics", "health", 
        "education", "science_and_environment", "technology", 
        "entertainment_and_arts"
    ]
    if category not in valid_categories:
        raise ValueError(f"不支持的分类: {category}")
    valid_editions = ["", "uk", "us", "int"]
    if edition not in valid_editions:
        raise ValueError(f"不支持的版本: {edition}")
    url = build_bbc_url(category, edition)
    return await parse_rss(url)

bbc_tool = Tool.from_function(
    fn=get_bbc_news_func,
    name="get-bbc-news",
    description="获取 BBC 新闻，提供全球新闻、英国新闻、商业、政治、健康、教育、科技、娱乐等资讯",
)

bbc_hot_tools = [
    bbc_tool
]

def main():
    result = asyncio.run(get_bbc_news_func(category="", edition="uk"))
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

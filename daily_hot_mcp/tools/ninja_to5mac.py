"""9to5Mac新闻工具"""

import asyncio
from daily_hot_mcp.utils import get_rss_items
from fastmcp.tools import Tool


async def get_9to5mac_news_func() -> list:
    """获取9to5Mac新闻数据"""
    return await get_rss_items("https://9to5mac.com/feed/")


get_ninja_to5mac_tool = Tool.from_function(
    name="get-9to5mac-news",
    description="获取 9to5Mac 苹果相关新闻，包含苹果产品发布、iOS 更新、Mac 硬件、应用推荐及苹果公司动态的英文资讯",
    fn=get_9to5mac_news_func,
)

ninja_to5mac_hot_tools = [
    get_ninja_to5mac_tool
] 

def main():
    result = asyncio.run(get_9to5mac_news_func())
    print(f"结果是{result}")

if __name__ == "__main__":
    main()
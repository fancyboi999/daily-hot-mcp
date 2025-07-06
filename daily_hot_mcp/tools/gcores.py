"""机核网新闻工具"""

import asyncio
from daily_hot_mcp.utils.rss import parse_rss
from fastmcp.tools import Tool

async def get_gcores_new_func() -> list:
    """获取机核网新闻数据"""
    return await parse_rss("https://www.gcores.com/rss")

gcores_new_tool = Tool.from_function(
    fn=get_gcores_new_func,
    name="get-gcores-new",
    description="获取机核网游戏相关资讯，包含电子游戏评测、玩家文化、游戏开发和游戏周边产品的深度内容",
)

gcores_hot_tools = [
    gcores_new_tool
]

def main():
    result = asyncio.run(get_gcores_new_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

"""自定义RSS工具"""

import asyncio
import os
from daily_hot_mcp.utils.rss import parse_rss
from fastmcp.tools import Tool

async def get_custom_rss_func() -> list:
    """获取自定义RSS数据"""
    rss_url = os.environ.get("TRENDS_HUB_CUSTOM_RSS_URL")
    if not rss_url:
        raise ValueError("TRENDS_HUB_CUSTOM_RSS_URL 环境变量未设置")
    return await parse_rss(rss_url)

# 尝试获取RSS信息来生成描述
description = "自定义RSS订阅源"
try:
    rss_url = os.environ.get("TRENDS_HUB_CUSTOM_RSS_URL")
    if rss_url:
        description = f"自定义RSS订阅源: {rss_url}"
except Exception:
    pass

custom_rss_tool = Tool.from_function(
    fn=get_custom_rss_func,
    name="custom-rss",
    description=description,
)

custom_rss_hot_tools = [
    custom_rss_tool
]

def main():
    # 需要设置环境变量 TRENDS_HUB_CUSTOM_RSS_URL
    # export TRENDS_HUB_CUSTOM_RSS_URL=https://rsshub.app/...
    result = asyncio.run(get_custom_rss_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

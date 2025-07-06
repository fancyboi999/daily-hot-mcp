"""爱范儿科技快讯工具"""

import asyncio
from typing import Annotated
from pydantic import Field
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool

async def get_ifanr_news_func(
    limit: Annotated[int, Field(description="返回结果数量限制")] = 20,
    offset: Annotated[int, Field(description="偏移量")] = 0
) -> list:
    """获取爱范儿科技快讯数据"""
    response = await http_client.get(
        "https://sso.ifanr.com/api/v5/wp/buzz",
        params={"limit": limit, "offset": offset}
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data.get("objects"), list):
        raise Exception("获取爱范儿快讯失败")
    results = []
    for item in data["objects"]:
        result_item = {
            "title": item.get("post_title", ""),
            "description": item.get("post_content", ""),
        }
        if item.get("buzz_original_url"):
            result_item["link"] = item["buzz_original_url"]
        elif item.get("post_id"):
            result_item["link"] = f"https://www.ifanr.com/{item['post_id']}"
        results.append(result_item)
    return results

ifanr_news_tool = Tool.from_function(
    fn=get_ifanr_news_func,
    name="get-ifanr-news",
    description="获取爱范儿科技快讯，包含最新的科技产品、数码设备、互联网动态等前沿科技资讯",
)

ifanr_hot_tools = [
    ifanr_news_tool
]

def main():
    result = asyncio.run(get_ifanr_news_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

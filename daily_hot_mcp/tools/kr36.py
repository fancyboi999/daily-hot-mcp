"""36氪热榜工具"""

import asyncio
import time
from datetime import datetime
from pydantic import Field
from typing import Annotated
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool

# 定义可选的类型映射
LIST_TYPE_MAP = {
    "hot": "hotRankList",
    "video": "videoList",
    "comment": "remarkList",
    "collect": "collectList",
}

# 主函数
async def get_36kr_trending_func(
    type: Annotated[
        str,
        Field(description="分类: hot(人气榜), video(视频榜), comment(热议榜), collect(收藏榜)")
    ] = "hot"
) -> list:
    """获取36氪热榜数据"""

    if type not in LIST_TYPE_MAP:
        raise ValueError(f"不支持的 type: {type}，请使用: {list(LIST_TYPE_MAP.keys())}")

    list_type = LIST_TYPE_MAP[type]

    payload = {
        "partner_id": "wap",
        "param": {
            "siteId": 1,
            "platformId": 2,
        },
        "timestamp": int(time.time() * 1000),
    }

    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }

    response = await http_client.post(
        f"https://gateway.36kr.com/api/mis/nav/home/nav/rank/{type}",
        json=payload,
        headers=headers
    )
    response.raise_for_status()

    data = response.json()
    if not isinstance(data.get("data"), dict):
        raise Exception("获取36氪热榜失败")

    items = data["data"].get(list_type, [])

    results = []
    for item in items:
        template_material = item.get("templateMaterial", {})

        # 处理发布时间
        publish_time_str = template_material.get("publishTime")
        publish_time_iso = None
        if publish_time_str:
            try:
                if isinstance(publish_time_str, (int, float)):
                    publish_time_iso = datetime.fromtimestamp(publish_time_str / 1000).isoformat()
                elif isinstance(publish_time_str, str):
                    publish_time_iso = publish_time_str
            except (ValueError, TypeError):
                pass

        result_item = {
            "title": template_material.get("widgetTitle", ""),
            "author": template_material.get("authorName", ""),
            "read_count": template_material.get("statRead", 0),
            "collect_count": template_material.get("statCollect", 0),
            "comment_count": template_material.get("statComment", 0),
            "praise_count": template_material.get("statPraise", 0),
        }

        if template_material.get("widgetImage"):
            result_item["cover"] = template_material["widgetImage"]
        if publish_time_iso:
            result_item["publish_time"] = publish_time_iso
        if template_material.get("itemId"):
            result_item["link"] = f"https://www.36kr.com/p/{template_material['itemId']}"

        results.append(result_item)

    return results

# 注册工具
kr36_tool_config = Tool.from_function(
    fn=get_36kr_trending_func,
    name="get-36kr-trending",
    description="获取 36 氪热榜，提供创业、商业、科技领域的热门资讯，包含投融资动态、新兴产业分析和商业模式创新信息",
)

kr36_hot_tools = [
    kr36_tool_config
]

# 测试入口
def main():
    result = asyncio.run(get_36kr_trending_func(type="hot"))
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()
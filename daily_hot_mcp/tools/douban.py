"""豆瓣实时热门榜工具"""

import asyncio
from typing import Annotated
from pydantic import Field
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool

URL_MAP = {
    "subject": "https://m.douban.com/rexxar/api/v2/subject_collection/subject_real_time_hotest/items",
    "movie": "https://m.douban.com/rexxar/api/v2/subject_collection/movie_real_time_hotest/items",
    "tv": "https://m.douban.com/rexxar/api/v2/subject_collection/tv_real_time_hotest/items",
}

async def get_douban_rank_func(
    rank_type: Annotated[str, Field(description="榜单类型：subject(图书、电影、电视剧、综艺等), movie(电影), tv(电视剧)")] = "subject",
    start: Annotated[int, Field(description="起始位置")] = 0,
    count: Annotated[int, Field(description="返回结果数量")] = 10
) -> list:
    """获取豆瓣实时热门榜数据"""
    if rank_type not in URL_MAP:
        raise ValueError(f"不支持的类型: {rank_type}")
    response = await http_client.get(
        URL_MAP[rank_type],
        params={
            "type": rank_type,
            "start": start,
            "count": count,
            "for_mobile": 1,
        },
        headers={
            "Referer": "https://m.douban.com/subject_collection/movie_real_time_hotest",
        }
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data.get("subject_collection_items"), list):
        raise Exception("获取豆瓣实时热门榜失败")
    results = []
    for item in data["subject_collection_items"]:
        rating = item.get("rating", {})
        rating_count = rating.get("count", 0)
        result_item = {
            "type_name": item.get("type_name", ""),
            "title": item.get("title", ""),
            "info": item.get("info", ""),
            "cover": item.get("cover", {}).get("url", ""),
            "year": item.get("year", ""),
            "release_date": item.get("release_date", ""),
            "link": item.get("url", ""),
            "popularity": item.get("score", 0),
            "rating_count": rating_count,
        }
        if rating_count > 0:
            result_item["rating_value"] = rating.get("value")
        related_terms = item.get("related_search_terms", [])
        if related_terms:
            hashtags = " ".join([f"#{term.get('name', '')}" for term in related_terms if term.get('name')])
            if hashtags:
                result_item["hashtags"] = hashtags
        results.append(result_item)
    return results

douban_rank_tool = Tool.from_function(
    fn=get_douban_rank_func,
    name="get-douban-rank",
    description="获取豆瓣实时热门榜单，提供当前热门的图书、电影、电视剧、综艺等作品信息，包含评分和热度数据",
)

douban_hot_tools = [
    douban_rank_tool
]

def main():
    result = asyncio.run(get_douban_rank_func(rank_type="movie", start=0, count=2))
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

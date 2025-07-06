"""The Verge新闻工具"""

import asyncio
from urllib.parse import urlparse, parse_qs
from daily_hot_mcp.utils import get_rss
from fastmcp.tools import Tool


async def get_theverge_news_func() -> list:
    """获取The Verge新闻数据"""
    rss_data = await get_rss("https://www.theverge.com/rss/index.xml")
    
    if not isinstance(rss_data.get("feed", {}).get("entry"), list):
        raise Exception("获取 The Verge 新闻失败")
    
    results = []
    for item in rss_data["feed"]["entry"]:
        link = item.get("link")
        if not link and item.get("id"):
            link = item["id"]
        
        # 处理链接参数
        if link:
            try:
                parsed = urlparse(link)
                query_params = parse_qs(parsed.query)
                if "p" in query_params:
                    # 重构URL
                    link = f"{parsed.scheme}://{parsed.netloc}{query_params['p'][0]}"
            except Exception:
                pass
        
        result_item = {
            "title": item.get("title", ""),
            "description": item.get("summary", ""),
            "publish_time": item.get("published", ""),
            "link": link or "",
        }
        results.append(result_item)
    
    return results


theverge_tool_config = Tool.from_function(
    fn=get_theverge_news_func,
    name="get-theverge-news",
    description="获取 The Verge 新闻，包含科技创新、数码产品评测、互联网趋势及科技公司动态的英文科技资讯",
)

theverge_hot_tools = [
    theverge_tool_config
]

def main():
    result = asyncio.run(get_theverge_news_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

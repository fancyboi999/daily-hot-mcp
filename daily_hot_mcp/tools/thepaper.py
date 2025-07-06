"""澎湃新闻热榜工具"""

import asyncio
from datetime import datetime
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool


async def get_thepaper_trending_func() -> list:
    """获取澎湃新闻热榜数据"""
    response = await http_client.get("https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar")
    response.raise_for_status()
    
    data = response.json()
    if data.get("resultCode") != 1 or not isinstance(data.get("data", {}).get("hotNews"), list):
        raise Exception(data.get("resultMsg", "获取澎湃新闻热榜失败"))
    
    results = []
    for item in data["data"]["hotNews"]:
        # 转换发布时间
        publish_time_iso = None
        if item.get("pubTimeLong"):
            try:
                # 假设pubTimeLong是毫秒时间戳
                publish_time_iso = datetime.fromtimestamp(item["pubTimeLong"] / 1000).isoformat()
            except (ValueError, TypeError):
                pass
        
        result_item = {
            "title": item.get("name", ""),
            "cover": item.get("pic", ""),
            "popularity": item.get("praiseTimes", 0),
        }
        
        if publish_time_iso:
            result_item["publish_time"] = publish_time_iso
        
        # 处理标签
        tag_list = item.get("tagList", [])
        if tag_list:
            hashtags = " ".join([f"#{tag.get('tag', '')}" for tag in tag_list if tag.get('tag')])
            if hashtags:
                result_item["hashtags"] = hashtags
        
        # 构建链接
        if item.get("contId"):
            result_item["link"] = f"https://www.thepaper.cn/newsDetail_forward_{item['contId']}"
        
        results.append(result_item)
    
    return results


thepaper_tool_config = Tool.from_function(
    fn=get_thepaper_trending_func,
    name="get-thepaper-trending",
    description="获取澎湃新闻热榜，包含时政要闻、财经动态、社会事件、文化教育及深度报道的高质量中文新闻资讯",
)

thepaper_hot_tools = [
    thepaper_tool_config
]

def main():
    result = asyncio.run(get_thepaper_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

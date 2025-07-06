"""百度热榜工具"""

import asyncio
from fastmcp.tools import Tool
from daily_hot_mcp.utils import http_client
from bs4 import BeautifulSoup

async def get_baidu_trending_func(args: dict) -> list:
    """获取百度热榜数据"""
    
    response = await http_client.get(
        "https://top.baidu.com/board",
        params={"tab": "realtime"}
    )
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    # 查找热榜条目
    hot_items = soup.find_all('div', class_='category-wrap_iQLoo')
    
    if not hot_items:
        raise Exception("获取百度热榜失败")
    
    for idx, item in enumerate(hot_items, 1):
        # 标题
        title_elem = item.find('div', class_='c-single-text-ellipsis')
        title = title_elem.text.strip() if title_elem else ""
        
        # 热搜指数
        index_elem = item.find('div', class_='hot-index_1Bl1a')
        hot_index = index_elem.text.strip() if index_elem else ""
        
        # 描述
        desc_elem = item.find('div', class_='hot-desc_1m_jR')
        description = desc_elem.text.strip() if desc_elem else ""
        
        # 链接
        link_elem = item.find('a')
        link = link_elem.get('href', '') if link_elem else ""
        if link and not link.startswith('http'):
            link = 'https://www.baidu.com' + link
        
        # 图片
        img_elem = item.find('img')
        cover = img_elem.get('src', '') if img_elem else ""
        
        if title:  # 只有有标题的才添加
            results.append({
                "title": title,
                "description": description,
                "popularity": hot_index,
                "link": link,
                "cover": cover,
                "rank": idx
            })
    
    return results


baidu_tool_config = Tool.from_function(
    fn=get_baidu_trending_func,
    name="get-baidu-trending",
    description="获取百度热榜，包含实时热搜、社会热点、科技新闻、娱乐八卦等多领域的热门中文资讯和搜索趋势",
)

baidu_hot_tools = [
    baidu_tool_config
] 

# 测试函数
async def main():
    result = await get_baidu_trending_func({})
    print(f"结果是{result}")
    

# 测试工具是否可用
if __name__ == "__main__":
    asyncio.run(main())
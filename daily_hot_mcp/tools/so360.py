"""360热搜榜工具"""

import asyncio
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool


async def get_so360_trending_func() -> list:
    """获取360热搜榜数据"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.so.com/',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    
    try:
        # 360搜索热榜API
        response = await http_client.get(
            "https://ranks.hao.360.com/mbsug-api/hotnewsquery",
            headers=headers,
            params={
                "type": "news",
                "realhot_limit": "50"
            }
        )
        
        response.raise_for_status()
        data = response.json()
        
        results = []
        
        if data.get('errno') == 0 and 'data' in data:
            hot_news = data['data'].get('hotnews', [])
            
            for idx, item in enumerate(hot_news[:50], 1):
                # 获取热度信息
                hot_value = item.get('hotValue', 0)
                hot_desc = item.get('hotDesc', '')
                
                results.append({
                    "rank": idx,
                    "title": item.get('title', '').strip(),
                    "desc": item.get('desc', '').strip(),
                    "url": item.get('url', ''),
                    "hot_value": hot_value,
                    "hot_desc": hot_desc,
                    "source": item.get('source', ''),
                    "img": item.get('img', ''),
                    "time": item.get('time', ''),
                    "category": item.get('category', ''),
                    "trend": item.get('trend', ''),  # 上升/下降趋势
                })
                
        if not results:
            # 备用方案：尝试获取360搜索建议
            return await get_so360_trending_backup()
            
        return results[:50]
        
    except Exception as e:
        return await get_so360_trending_backup()


async def get_so360_trending_backup():
    """360热搜榜备用获取方案"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.so.com/'
    }
    
    try:
        # 尝试360搜索热词接口
        response = await http_client.get(
            "https://sug.so.360.cn/suggest",
            headers=headers,
            params={
                "encodein": "utf-8",
                "encodeout": "utf-8", 
                "format": "json",
                "word": "",
                "src": "home"
            }
        )
        
        response.raise_for_status()
        data = response.json()
        
        results = []
        if 'result' in data:
            suggestions = data['result'][:50]
            
            for idx, suggestion in enumerate(suggestions, 1):
                # suggestion通常是个列表，第一个元素是关键词
                keyword = suggestion[0] if isinstance(suggestion, list) else str(suggestion)
                
                results.append({
                    "rank": idx,
                    "title": keyword.strip(),
                    "desc": f"360搜索热词 - {keyword}",
                    "url": f"https://www.so.com/s?q={keyword}",
                    "hot_value": 0,
                    "hot_desc": "",
                    "source": "360搜索",
                    "img": "",
                    "time": "",
                    "category": "热搜词",
                    "trend": ""
                })
        
        if results:
            return results
            
    except Exception:
        pass
    
    # 最终备用方案
    return [
        {
            "rank": 1,
            "title": "360热搜榜数据获取中...",
            "desc": "360搜索热门关键词和热点新闻",
            "url": "https://www.so.com/",
            "hot_value": 0,
            "hot_desc": "",
            "source": "360搜索",
            "img": "",
            "time": "",
            "category": "系统消息",
            "trend": "",
            "note": "接口暂时不可用，请稍后重试"
        }
    ]


so360_tool_config = Tool.from_function(
    fn=get_so360_trending_func,
    name="get-so360-trending",
    description="获取360热搜榜，包含360搜索平台的热门搜索词、实时新闻热点及用户关注度较高的中文资讯",
)

so360_hot_tools = [
    so360_tool_config
]

def main():
    result = asyncio.run(get_so360_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

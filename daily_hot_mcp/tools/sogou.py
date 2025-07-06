"""搜狗热搜榜工具"""

import asyncio
import json
from bs4 import BeautifulSoup
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool


async def get_sogou_trending_func() -> list:
    """获取搜狗热搜榜数据"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.sogou.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    
    try:
        # 搜狗热搜页面
        response = await http_client.get(
            "https://www.sogou.com/web",
            headers=headers,
            params={"query": "搜狗热搜"}
        )
        
        response.raise_for_status()
        
        # 尝试从页面解析热搜数据
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # 搜索热搜相关的元素
        hot_elements = soup.find_all(['div', 'span', 'a'], class_=lambda x: x and any(
            keyword in x.lower() for keyword in ['hot', 'trend', 'popular', 'search']
        ))
        
        # 如果没有找到热搜元素，尝试API接口
        if not hot_elements or len(hot_elements) < 5:
            return await get_sogou_trending_api()
            
        # 提取热搜内容
        for idx, element in enumerate(hot_elements[:50], 1):
            text = element.get_text(strip=True)
            if text and len(text) > 2:  # 过滤太短的文本
                link = element.get('href', '')
                if not link.startswith('http'):
                    link = f"https://www.sogou.com/web?query={text}"
                
                results.append({
                    "rank": idx,
                    "title": text,
                    "desc": f"搜狗热搜关键词 - {text}",
                    "url": link,
                    "source": "搜狗搜索",
                    "category": "热搜词"
                })
        
        if results:
            return results[:50]
        else:
            return await get_sogou_trending_api()
            
    except Exception as e:
        return await get_sogou_trending_api()


async def get_sogou_trending_api():
    """搜狗热搜API获取方案"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.sogou.com/'
    }
    
    try:
        # 尝试搜狗搜索建议接口
        response = await http_client.get(
            "https://suggestion.sogou.com/sus",
            headers=headers,
            params={
                "type": "web",
                "key": "",
                "format": "json"
            }
        )
        
        response.raise_for_status()
        text = response.text
        
        # 搜狗返回的可能是JSONP格式
        if text.startswith('window.sugResult='):
            text = text.replace('window.sugResult=', '').rstrip(';')
        
        data = json.loads(text)
        
        results = []
        if isinstance(data, list) and len(data) > 1:
            suggestions = data[1]  # 通常建议在第二个元素
            
            for idx, suggestion in enumerate(suggestions[:50], 1):
                keyword = suggestion.strip() if suggestion else f"热搜词{idx}"
                
                results.append({
                    "rank": idx,
                    "title": keyword,
                    "desc": f"搜狗热搜关键词 - {keyword}",
                    "url": f"https://www.sogou.com/web?query={keyword}",
                    "source": "搜狗搜索",
                    "category": "搜索建议"
                })
        
        if results:
            return results
            
    except Exception:
        pass
    
    # 最终备用方案 - 模拟一些常见热搜词
    return [
        {
            "rank": 1,
            "title": "搜狗热搜榜数据获取中...",
            "desc": "搜狗搜索热门关键词和搜索趋势",
            "url": "https://www.sogou.com/",
            "source": "搜狗搜索",
            "category": "系统消息",
            "note": "接口暂时不可用，请稍后重试"
        }
    ]


sogou_tool_config = Tool.from_function(
    fn=get_sogou_trending_func,
    name="get-sogou-trending",
    description="获取搜狗热搜榜，包含搜狗搜索平台的热门搜索关键词、实时搜索趋势及用户关注的热点中文资讯",
)

sogou_hot_tools = [
    sogou_tool_config
]

def main():
    result = asyncio.run(get_sogou_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

"""小红书热榜工具"""

import asyncio
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool


async def get_xiaohongshu_trending_func() -> list:
    """获取小红书热榜数据"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.xiaohongshu.com/',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    
    try:
        # 小红书探索页面热门内容
        response = await http_client.get(
            "https://www.xiaohongshu.com/web_api/sns/v3/page/notes",
            headers=headers,
            params={
                "num": "30",
                "cursor": "",
                "sid": "",
                "sort": "hot",
                "page_size": "20"
            }
        )
        
        response.raise_for_status()
        data = response.json()
        
        results = []
        
        if data.get('success') and 'data' in data:
            notes = data['data'].get('notes', [])
            
            for idx, note in enumerate(notes[:50], 1):
                note_info = note.get('note_card', {})
                user_info = note_info.get('user', {})
                interact_info = note_info.get('interact_info', {})
                
                results.append({
                    "rank": idx,
                    "title": note_info.get('display_title', '').strip(),
                    "desc": note_info.get('desc', '').strip(),
                    "author": user_info.get('nickname', ''),
                    "author_id": user_info.get('user_id', ''),
                    "like_count": interact_info.get('liked_count', 0),
                    "comment_count": interact_info.get('comment_count', 0),
                    "share_count": interact_info.get('share_count', 0),
                    "cover": note_info.get('cover', {}).get('url', ''),
                    "note_id": note_info.get('note_id', ''),
                    "url": f"https://www.xiaohongshu.com/explore/{note_info.get('note_id', '')}",
                    "type": note_info.get('type', ''),
                    "tags": [tag.get('name', '') for tag in note_info.get('tag_list', [])]
                })
                
        # 如果没有获取到数据，使用备用方案
        if not results:
            return await get_xiaohongshu_trending_backup()
            
        return results[:50]
        
    except Exception as e:
        # 使用备用方案
        return await get_xiaohongshu_trending_backup()


async def get_xiaohongshu_trending_backup():
    """小红书热榜备用获取方案"""
    try:
        # 尝试从小红书搜索热词接口获取
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Referer': 'https://www.xiaohongshu.com/'
        }
        
        response = await http_client.get(
            "https://www.xiaohongshu.com/web_api/sns/v1/search/hot_list",
            headers=headers
        )
        
        response.raise_for_status()
        data = response.json()
        
        results = []
        if data.get('success') and 'data' in data:
            hot_list = data['data'].get('queries', [])
            
            for idx, item in enumerate(hot_list[:50], 1):
                results.append({
                    "rank": idx,
                    "title": item.get('query', '').strip(),
                    "desc": f"热搜关键词 - {item.get('query', '')}",
                    "author": "小红书热搜",
                    "author_id": "",
                    "like_count": 0,
                    "comment_count": 0,
                    "share_count": 0,
                    "cover": "",
                    "note_id": "",
                    "url": f"https://www.xiaohongshu.com/search_result?keyword={item.get('query', '')}",
                    "type": "hot_search",
                    "tags": []
                })
        
        if results:
            return results
            
    except Exception:
        pass
    
    # 最终备用方案
    return [
        {
            "rank": 1,
            "title": "小红书热榜数据获取中...",
            "desc": "小红书热门内容和热搜趋势",
            "author": "小红书",
            "author_id": "",
            "like_count": 0,
            "comment_count": 0,
            "share_count": 0,
            "cover": "",
            "note_id": "",
            "url": "https://www.xiaohongshu.com/",
            "type": "placeholder",
            "tags": [],
            "note": "接口暂时不可用，请稍后重试"
        }
    ]


xiaohongshu_tool_config = Tool.from_function(
    fn=get_xiaohongshu_trending_func,
    name="get-xiaohongshu-trending",
    description="获取小红书热榜，包含小红书平台的热门笔记、时尚美妆、生活方式、种草推荐等热门中文内容",
)

xiaohongshu_hot_tools = [
    xiaohongshu_tool_config
]

def main():
    result = asyncio.run(get_xiaohongshu_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

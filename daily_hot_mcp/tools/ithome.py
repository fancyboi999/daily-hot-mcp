"""
IT之家热榜采集工具
获取IT之家的科技新闻热榜，包含科技资讯、数码产品、互联网动态等内容
"""

import asyncio
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool
from bs4 import BeautifulSoup

async def get_ithome_trending_func() -> list:
    """获取IT之家热榜"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    try:
        url = "https://www.ithome.com/"
        response = await http_client.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        items = []
        news_items = (
            soup.select('.hot-list li a') + 
            soup.select('.news-list li a') + 
            soup.select('.list-box li a') +
            soup.select('a[href*="/it/"]') +
            soup.select('.post-item a') +
            soup.select('.news-item a')
        )
        rank = 1
        seen_titles = set()
        for item in news_items:
            try:
                title = item.get_text(strip=True)
                if not title or len(title) < 5 or title in seen_titles:
                    continue
                if any(skip in title for skip in ['登录', '注册', '首页', '下载', '更多']):
                    continue
                seen_titles.add(title)
                link = item.get('href', '')
                if link and not link.startswith('http'):
                    if link.startswith('/'):
                        link = 'https://www.ithome.com' + link
                    else:
                        link = 'https://www.ithome.com/' + link
                desc = ""
                parent = item.parent
                if parent:
                    desc_elem = (parent.find('p') or 
                               parent.find('div', class_='summary') or 
                               parent.find('div', class_='content') or
                               parent.find('span', class_='desc'))
                    if desc_elem:
                        desc = desc_elem.get_text(strip=True)[:200]
                if not desc:
                    desc = f"IT之家科技资讯 - {title}"
                publish_time = ""
                if parent:
                    time_elem = (parent.find('time') or 
                               parent.find('span', class_='time') or 
                               parent.find('div', class_='time') or
                               parent.find('.post-time'))
                    if time_elem:
                        publish_time = time_elem.get_text(strip=True)
                hot_count = ""
                if parent:
                    hot_elem = (parent.find('span', class_='hot') or 
                              parent.find('span', class_='comment') or 
                              parent.find('span', class_='view') or
                              parent.find('.comment-count'))
                    if hot_elem:
                        hot_count = hot_elem.get_text(strip=True)
                item_data = {
                    'rank': rank,
                    'title': title,
                    'desc': desc,
                    'url': link or f"https://www.ithome.com/search?q={title}",
                    'source': 'IT之家',
                    'publish_time': publish_time,
                    'hot_count': hot_count,
                    'category': '科技资讯',
                    'tags': ['科技', '数码', 'IT资讯', '互联网']
                }
                items.append(item_data)
                rank += 1
                if rank > 50:
                    break
            except Exception as e:
                continue
        if not items:
            items = [{
                'rank': 1,
                'title': 'IT之家热榜数据获取中...',
                'desc': 'IT之家科技资讯和热门新闻',
                'url': 'https://www.ithome.com/',
                'source': 'IT之家',
                'publish_time': '',
                'hot_count': '',
                'category': '科技资讯',
                'tags': ['科技', '数码', 'IT资讯', '互联网']
            }]
        return items
    except Exception as e:
        return [{
            'rank': 1,
            'title': 'IT之家热榜数据获取中...',
            'desc': f'IT之家科技资讯获取失败: {str(e)}',
            'url': 'https://www.ithome.com/',
            'source': 'IT之家',
            'publish_time': '',
            'hot_count': '',
            'category': '科技资讯',
            'tags': ['科技', '数码', 'IT资讯', '互联网'],
            'error': str(e)
        }]

ithome_trending_tool = Tool.from_function(
    fn=get_ithome_trending_func,
    name="get-ithome-trending",
    description="获取IT之家热榜，包含科技资讯、数码产品、互联网动态、软件应用及前沿科技发展的热门中文科技新闻",
)

ithome_hot_tools = [
    ithome_trending_tool
]

def main():
    result = asyncio.run(get_ithome_trending_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

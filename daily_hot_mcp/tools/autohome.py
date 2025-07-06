"""汽车之家热榜工具"""

import asyncio
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool
from bs4 import BeautifulSoup
import json


async def get_autohome_trending_func(args: dict) -> list:
    """获取汽车之家热榜数据"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.autohome.com.cn/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    
    try:
        # 汽车之家首页热门新闻
        response = await http_client.get(
            "https://www.autohome.com.cn/",
            headers=headers
        )
        
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # 查找热门新闻和汽车资讯
        news_items = (
            soup.select('.list-article li a') +
            soup.select('.hot-news li a') +
            soup.select('.news-list li a') +
            soup.select('a[href*="/news/"]') +
            soup.select('a[href*="/advice/"]') +
            soup.select('a[href*="/drive/"]')
        )
        
        rank = 1
        seen_titles = set()
        
        for item in news_items:
            try:
                title = item.get_text(strip=True)
                if not title or len(title) < 5 or title in seen_titles:
                    continue
                
                # 过滤掉导航链接和无效内容
                if any(skip in title for skip in ['登录', '注册', '首页', '下载', '更多', '论坛', '导航']):
                    continue
                
                seen_titles.add(title)
                
                link = item.get('href', '')
                if link and not link.startswith('http'):
                    if link.startswith('//'):
                        link = 'https:' + link
                    elif link.startswith('/'):
                        link = 'https://www.autohome.com.cn' + link
                    else:
                        link = 'https://www.autohome.com.cn/' + link
                
                # 获取描述信息
                desc = ""
                parent = item.parent
                if parent:
                    desc_elem = (parent.find('p') or 
                               parent.find('div', class_='summary') or 
                               parent.find('span', class_='desc') or
                               parent.find('div', class_='content'))
                    if desc_elem:
                        desc = desc_elem.get_text(strip=True)[:200]
                
                if not desc:
                    desc = f"汽车之家资讯 - {title}"
                
                # 尝试获取时间和评论数
                publish_time = ""
                comment_count = ""
                
                if parent:
                    time_elem = (parent.find('time') or 
                               parent.find('span', class_='time') or 
                               parent.find('.date'))
                    if time_elem:
                        publish_time = time_elem.get_text(strip=True)
                    
                    comment_elem = (parent.find('span', class_='comment') or 
                                  parent.find('.comment-count') or
                                  parent.find('span', string=lambda text: text and '评论' in text))
                    if comment_elem:
                        comment_count = comment_elem.get_text(strip=True)
                
                # 判断文章类型
                category = "汽车资讯"
                if '/news/' in link:
                    category = "汽车新闻"
                elif '/advice/' in link:
                    category = "购车指南"
                elif '/drive/' in link:
                    category = "试驾体验"
                elif '/dealer/' in link:
                    category = "经销商"
                
                item_data = {
                    'rank': rank,
                    'title': title,
                    'desc': desc,
                    'url': link or f"https://www.autohome.com.cn/search?q={title}",
                    'source': '汽车之家',
                    'publish_time': publish_time,
                    'comment_count': comment_count,
                    'category': category,
                    'tags': ['汽车', '汽车资讯', '购车', '试驾']
                }
                
                results.append(item_data)
                rank += 1
                
                if rank > 50:
                    break
                    
            except Exception as e:
                continue
        
        # 如果没有获取到数据，尝试API接口
        if not results:
            try:
                api_response = await http_client.get(
                    "https://www.autohome.com.cn/ashx/AjaxIndexInfo.ashx?type=5",
                    headers=headers
                )
                
                if api_response.status_code == 200:
                    api_data = api_response.json()
                    if 'result' in api_data and api_data['result']:
                        items = api_data['result'][:30]
                        for idx, item in enumerate(items, 1):
                            results.append({
                                'rank': idx,
                                'title': item.get('title', '').strip(),
                                'desc': item.get('summary', f"汽车之家资讯 - {item.get('title', '')}"),
                                'url': item.get('url', ''),
                                'source': '汽车之家',
                                'publish_time': item.get('publishtime', ''),
                                'comment_count': item.get('replycount', ''),
                                'category': '汽车资讯',
                                'tags': ['汽车', '汽车资讯', '购车', '试驾']
                            })
                            
            except Exception:
                pass
        
        # 如果仍然没有数据，返回默认数据
        if not results:
            results = [{
                'rank': 1,
                'title': '汽车之家热榜数据获取中...',
                'desc': '汽车之家汽车资讯和热门新闻',
                'url': 'https://www.autohome.com.cn/',
                'source': '汽车之家',
                'publish_time': '',
                'comment_count': '',
                'category': '汽车资讯',
                'tags': ['汽车', '汽车资讯', '购车', '试驾']
            }]
        
        return results[:50]
        
    except Exception as e:
        # 返回备用数据
        return [{
            'rank': 1,
            'title': '汽车之家热榜数据获取中...',
            'desc': f'汽车之家汽车资讯获取失败: {str(e)}',
            'url': 'https://www.autohome.com.cn/',
            'source': '汽车之家',
            'publish_time': '',
            'comment_count': '',
            'category': '汽车资讯',
            'tags': ['汽车', '汽车资讯', '购车', '试驾'],
            'error': str(e)
        }]


autohome_tool_config = Tool.from_function(
    fn=get_autohome_trending_func,
    name="get-autohome-trending",
    description="获取汽车之家热榜，包含汽车新闻、新车发布、购车指南、试驾体验、汽车评测及汽车行业动态的专业汽车资讯",
)

autohome_hot_tools = [
    autohome_tool_config
] 

# 测试函数
async def main():
    result = await get_autohome_trending_func({})
    print(f"结果是{result}")
    

# 测试工具是否可用
if __name__ == "__main__":
    asyncio.run(main())
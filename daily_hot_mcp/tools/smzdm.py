"""什么值得买热门工具"""

import asyncio
import json
from pydantic import Field
from typing import Annotated
from daily_hot_mcp.utils import http_client
from fastmcp.tools import Tool


def safe_json_parse(text: str):
    """安全解析JSON"""
    try:
        return json.loads(text) if text else None
    except (json.JSONDecodeError, TypeError):
        return None


async def get_smzdm_rank_func(
    unit: Annotated[int, Field(description="时间范围：1(今日热门), 7(周热门), 30(月热门)")] = 1
) -> list:
    """获取什么值得买热门数据"""
    # 验证unit参数
    valid_units = [1, 7, 30]
    if unit not in valid_units:
        raise Exception(f"不支持的时间单位: {unit}")
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://post.smzdm.com/rank/",
        }
        
        response = await http_client.get(
            "https://post.smzdm.com/rank/json_more",
            params={"unit": unit},
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        
        # 检查响应内容类型
        content_type = response.headers.get('content-type', '')
        if 'application/json' not in content_type and 'text/json' not in content_type:
            # 如果不是JSON响应，尝试从HTML中提取数据或返回空列表
            print(f"什么值得买返回非JSON响应，内容类型: {content_type}")
            return []
        
        # 确保正确的编码
        response.encoding = 'utf-8'
        
        # 获取原始文本并检查是否为空
        text = response.text.strip()
        if not text:
            print("什么值得买返回空响应")
            return []
        
        data = response.json()
        if data.get("error_code") != 0 or not isinstance(data.get("data"), list):
            error_msg = data.get("error_msg", "获取什么值得买热门失败")
            print(f"什么值得买API错误: {error_msg}")
            return []
        
        results = []
        for item in data["data"]:
            result_item = {
                "title": item.get("title", ""),
                "description": item.get("content", ""),
                "cover": item.get("pic_url", ""),
                "author": item.get("nickname", ""),
                "publish_time": item.get("publish_time", ""),
                "collection_count": item.get("collection_count", 0),
                "comment_count": item.get("comment_count", 0),
                "up_count": item.get("up_count", 0),
                "link": item.get("article_url", ""),
            }
            
            # 处理标签
            tag_data = safe_json_parse(item.get("tag", ""))
            if tag_data and isinstance(tag_data, list):
                hashtags = " ".join([f"#{tag.get('title', '')}" for tag in tag_data if tag.get('title')])
                if hashtags:
                    result_item["hashtags"] = hashtags
            
            results.append(result_item)
        
        return results
        
    except Exception as e:
        print(f"获取什么值得买数据失败: {e}")
        # 在测试阶段返回空列表而不是抛出异常
        return []


smzdm_tool_config = Tool.from_function(
    fn=get_smzdm_rank_func,
    name="get-smzdm-rank",
    description="获取什么值得买热门，包含商品推荐、优惠信息、购物攻略、产品评测及消费经验分享的实用中文消费类资讯",
)

smzdm_hot_tools = [
    smzdm_tool_config
]

def main():
    result = asyncio.run(get_smzdm_rank_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

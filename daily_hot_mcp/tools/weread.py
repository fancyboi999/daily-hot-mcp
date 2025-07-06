"""微信读书排行榜工具"""

import asyncio
import hashlib
import re
from pydantic import Field
from typing import Annotated
from daily_hot_mcp.utils import http_client, logger
from fastmcp.tools import Tool


def get_weread_id(book_id: str) -> str:
    """生成微信读书ID"""
    try:
        # 使用MD5哈希算法创建哈希对象
        hash_obj = hashlib.md5()
        hash_obj.update(book_id.encode())
        str_hash = hash_obj.hexdigest()
        
        # 取哈希结果的前三个字符作为初始值
        str_sub = str_hash[:3]
        
        # 判断书籍ID的类型并进行转换
        if re.match(r'^\d*$', book_id):
            # 如果书籍ID只包含数字，则将其拆分成长度为9的子字符串，并转换为十六进制表示
            chunks = []
            for i in range(0, len(book_id), 9):
                chunk = book_id[i:i+9]
                chunks.append(hex(int(chunk))[2:])  # 去掉'0x'前缀
            fa = ['3', chunks]
        else:
            # 如果书籍ID包含其他字符，则将每个字符的Unicode编码转换为十六进制表示
            hex_str = ''.join([hex(ord(char))[2:] for char in book_id])
            fa = ['4', [hex_str]]
        
        # 将类型添加到初始值中
        str_sub += fa[0]
        # 将数字2和哈希结果的后两个字符添加到初始值中
        str_sub += f"2{str_hash[-2:]}"
        
        # 处理转换后的子字符串数组
        for i, sub in enumerate(fa[1]):
            sub_length = hex(len(sub))[2:]  # 去掉'0x'前缀
            # 如果长度只有一位数，则在前面添加0
            sub_length_padded = f"0{sub_length}" if len(sub_length) == 1 else sub_length
            # 将长度和子字符串添加到初始值中
            str_sub += sub_length_padded + sub
            # 如果不是最后一个子字符串，则添加分隔符'g'
            if i < len(fa[1]) - 1:
                str_sub += 'g'
        
        # 如果初始值长度不足20，从哈希结果中取足够的字符补齐
        if len(str_sub) < 20:
            str_sub += str_hash[:20 - len(str_sub)]
        
        # 使用MD5哈希算法创建新的哈希对象
        final_hash = hashlib.md5()
        final_hash.update(str_sub.encode())
        final_str = final_hash.hexdigest()
        
        # 取最终哈希结果的前三个字符并添加到初始值的末尾
        str_sub += final_str[:3]
        return str_sub
        
    except Exception as e:
        logger.error(f"处理微信读书ID时出现错误：{e}")
        return ""


async def get_weread_rank_func(
    category: Annotated[str, Field(description="排行榜分区：rising(飙升榜), hot_search(热搜榜), newbook(新书榜), general_novel_rising(小说榜), all(总榜)")] = "rising"
) -> list:
    """获取微信读书排行榜数据"""
    # 验证category参数
    valid_categories = ["rising", "hot_search", "newbook", "general_novel_rising", "all"]
    if category not in valid_categories:
        raise Exception(f"不支持的排行榜分区: {category}")
    
    response = await http_client.get(
        f"https://weread.qq.com/web/bookListInCategory/{category}",
        params={"rank": 1}
    )
    response.raise_for_status()
    
    data = response.json()
    if not isinstance(data.get("books"), list):
        raise Exception("获取微信读书排行榜失败")
    
    results = []
    for item in data["books"]:
        book_info = item.get("bookInfo", {})
        book_id = book_info.get("bookId", "")
        weread_id = get_weread_id(book_id) if book_id else ""
        
        result_item = {
            "title": book_info.get("title", ""),
            "description": book_info.get("intro", ""),
            "author": book_info.get("author", ""),
            "publish_time": book_info.get("publishTime", ""),
            "reading_count": item.get("readingCount", 0),
        }
        
        # 处理封面图片
        cover = book_info.get("cover", "")
        if cover:
            result_item["cover"] = cover.replace("s_", "t9_")
        
        # 构建链接
        if weread_id:
            result_item["link"] = f"https://weread.qq.com/web/bookDetail/{weread_id}"
        
        results.append(result_item)
    
    return results


weread_tool_config = Tool.from_function(
    fn=get_weread_rank_func,
    name="get-weread-rank",
    description="获取微信读书排行榜，包含热门小说、畅销书籍、新书推荐及各类文学作品的阅读数据和排名信息",
)

weread_hot_tools = [
    weread_tool_config
]

def main():
    result = asyncio.run(get_weread_rank_func())
    print(f"结果是：{result}")

if __name__ == "__main__":
    main()

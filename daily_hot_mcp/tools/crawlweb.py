import os
from typing import Annotated
from firecrawl import FirecrawlApp
from fastmcp.tools import Tool
from pydantic import Field

# 环境变量获取api_key
api_key = os.getenv("FIRECRAWL_API_KEY")
app = FirecrawlApp(api_key=api_key)


def crawl_website_func(url: Annotated[str, Field(description="需要爬取的网站URL，多用于用户想要详细了解某网站内容时使用")]) -> str:
    """
    description: 爬取网站内容
    args:
        url: 需要爬取的网站URL
    return:
        markdown_content: 爬取结果
    """
    scrape_result = app.scrape_url(url, formats=["markdown"])
    if scrape_result.metadata["statusCode"] == 200:
        markdown_content = scrape_result.markdown
        return markdown_content
    else:
        erro_message = f"爬取网站内容失败: {scrape_result.metadata['statusCode']}"
        return erro_message
    

crawl_website_tool = Tool.from_function(
    fn=crawl_website_func,
    name="crawl_website",
    description="爬取网站内容，多用于用户想要详细了解某网站内容时使用",
)

crawl_website_hot_tools = [
    crawl_website_tool
]

def main():
    result = crawl_website_func(url="https://www.baidu.com")
    print(result)

if __name__ == "__main__":
    main()
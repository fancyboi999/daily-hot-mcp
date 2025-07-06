"""HTTP客户端模块"""

import httpx
from typing import Any, Dict, Optional


class HttpClient:
    """HTTP客户端封装"""
    
    def __init__(self):
        self._client = httpx.AsyncClient(
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            },
            timeout=30.0,
            follow_redirects=True,
        )
    
    async def get(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> httpx.Response:
        """发送GET请求"""
        return await self._client.get(
            url, 
            params=params, 
            headers=headers,
            **kwargs
        )
    
    async def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> httpx.Response:
        """发送POST请求"""
        return await self._client.post(
            url,
            data=data,
            json=json,
            headers=headers,
            **kwargs
        )
    
    async def close(self):
        """关闭客户端"""
        await self._client.aclose()


# 全局HTTP客户端实例
http_client = HttpClient() 
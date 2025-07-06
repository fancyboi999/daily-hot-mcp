"""
Cache utilities for MCP Daily News.
"""

import json
import tempfile
from pathlib import Path
from typing import Any, Optional
from datetime import datetime, timedelta


class SimpleCache:
    def __init__(self, cache_duration_minutes: int = 30):
        """Initialize the cache with specified duration."""
        self._cache_dir = Path(tempfile.gettempdir()) / "mcp_daily_news" / "cache"
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_duration = timedelta(minutes=cache_duration_minutes)

    def _get_cache_file(self, key: str) -> Path:
        """Get the cache file path for a given key."""
        safe_key = "".join(c for c in key if c.isalnum() or c in '-_.')
        return self._cache_dir / f"{safe_key}.json"

    def get(self, key: str) -> Optional[Any]:
        """Get cached data for a key if it exists and is not expired."""
        cache_file = self._get_cache_file(key)
        
        if not cache_file.exists():
            return None
            
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                
            # Check if cache is expired
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cache_time > self._cache_duration:
                cache_file.unlink()  # Remove expired cache
                return None
                
            return cache_data['data']
        except Exception:
            # If there's any error reading cache, remove it
            if cache_file.exists():
                cache_file.unlink()
            return None

    def set(self, key: str, data: Any) -> None:
        """Cache data for a key."""
        cache_file = self._get_cache_file(key)
        
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception:
            # Ignore cache write errors
            pass

    def clear(self) -> None:
        """Clear all cached data."""
        try:
            for cache_file in self._cache_dir.glob("*.json"):
                cache_file.unlink()
        except Exception:
            pass


# Global cache instance
cache = SimpleCache() 
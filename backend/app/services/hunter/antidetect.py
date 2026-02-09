"""
Anti-Detection Infrastructure for Hunter Engine.
Provides proxy rotation, rate limiting, stealth headers, and browser fingerprint masking.
"""

import random
import time
import asyncio
import os
from typing import Optional, Dict, List
from dataclasses import dataclass, field
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ─── User-Agent Pool ──────────────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

ACCEPT_LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "en-US,en;q=0.9,ar;q=0.8",
    "en,ar;q=0.9",
]


@dataclass
class ProxyConfig:
    """Residential proxy configuration."""
    url: str = ""
    username: str = ""
    password: str = ""
    rotation_type: str = "per_request"  # per_request, sticky

    @property
    def is_configured(self) -> bool:
        return bool(self.url)

    @property
    def proxy_dict(self) -> Optional[Dict[str, str]]:
        if not self.is_configured:
            return None
        if self.username and self.password:
            auth = f"{self.username}:{self.password}@"
        else:
            auth = ""
        proxy_url = f"http://{auth}{self.url}"
        return {"http": proxy_url, "https": proxy_url}


class RateLimiter:
    """Human-like rate limiting with randomized delays."""

    def __init__(self, min_delay: float = 1.0, max_delay: float = 3.0, burst_limit: int = 10, burst_cooldown: float = 15.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.burst_limit = burst_limit
        self.burst_cooldown = burst_cooldown
        self._request_count = 0
        self._last_reset = time.time()

    def wait(self):
        """Block for a random human-like delay. Apply burst cooldown if threshold hit."""
        self._request_count += 1

        if self._request_count >= self.burst_limit:
            elapsed = time.time() - self._last_reset
            if elapsed < 60:
                cooldown = self.burst_cooldown + random.uniform(0, 5)
                print(f"    ⏳ Burst limit reached, cooling down {cooldown:.1f}s...")
                time.sleep(cooldown)
            self._request_count = 0
            self._last_reset = time.time()

        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)

    async def async_wait(self):
        """Async version of wait."""
        self._request_count += 1
        if self._request_count >= self.burst_limit:
            elapsed = time.time() - self._last_reset
            if elapsed < 60:
                cooldown = self.burst_cooldown + random.uniform(0, 5)
                await asyncio.sleep(cooldown)
            self._request_count = 0
            self._last_reset = time.time()
        delay = random.uniform(self.min_delay, self.max_delay)
        await asyncio.sleep(delay)


class StealthSession:
    """
    Creates a requests.Session with:
    - Rotating user agents
    - Rotating proxies (if configured)
    - Retry logic with backoff
    - Human-like headers
    """

    def __init__(self, proxy_config: Optional[ProxyConfig] = None, rate_limiter: Optional[RateLimiter] = None):
        self.proxy_config = proxy_config or ProxyConfig(
            url=os.getenv("PROXY_URL", ""),
            username=os.getenv("PROXY_USER", ""),
            password=os.getenv("PROXY_PASS", ""),
        )
        self.rate_limiter = rate_limiter or RateLimiter(
            min_delay=float(os.getenv("SCRAPER_DELAY_MIN", "1.0")),
            max_delay=float(os.getenv("SCRAPER_DELAY_MAX", "3.0")),
        )
        self._session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        if self.proxy_config.proxy_dict:
            session.proxies.update(self.proxy_config.proxy_dict)
        return session

    def _stealth_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": random.choice(ACCEPT_LANGUAGES),
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }

    def get(self, url: str, **kwargs) -> requests.Response:
        self.rate_limiter.wait()
        headers = self._stealth_headers()
        headers.update(kwargs.pop("headers", {}))
        return self._session.get(url, headers=headers, timeout=kwargs.pop("timeout", 30), **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        self.rate_limiter.wait()
        headers = self._stealth_headers()
        headers.update(kwargs.pop("headers", {}))
        return self._session.post(url, headers=headers, timeout=kwargs.pop("timeout", 30), **kwargs)


def get_stealth_session() -> StealthSession:
    """Factory: returns a configured StealthSession."""
    return StealthSession()

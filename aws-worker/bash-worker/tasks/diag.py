
import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


IP_SOURCES = [
    "ifconfig.me",
    "https://api.ipify.org",
    "https://ipinfo.io/ip"
]

async def fetch_public_ip(session, url, proxy, timeout=10):
    try:
        async with session.get(url, proxy=proxy, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
            if resp.status == 200:
                text = await resp.text()
                return text.strip()
    except Exception:
        return None

async def fetch_json(session, url, timeout=10):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
            if resp.status == 200:
                return await resp.json()
    except Exception:
        return None

async def diag_cloud_proxy(target_server: str, target_ip: str):
    proxy = f"http://{target_ip}:3128"

    async with aiohttp.ClientSession() as session:
        public_ip = None

        # Try public IP services in order
        for url in IP_SOURCES:
            public_ip = await fetch_public_ip(session, url, proxy)
            if public_ip:
                break

        if not public_ip:
            return {
                "success": False,
                "server": target_server,
                "proxy_ip": target_ip,
                "error": "Unable to retrieve public IP via proxy."
            }

        # Geo from ip-api.com
        geo1 = await fetch_json(session, f"http://ip-api.com/json/{public_ip}")
        country1 = geo1.get("country") if geo1 and geo1.get("status") == "success" else "Error"

        # Geo from ipinfo.io
        geo2 = await fetch_json(session, f"https://ipinfo.io/{public_ip}/json")
        country2 = geo2.get("country") if geo2 else "Error"

        logging.info(f"country_ipapi: {country1}")
        logging.info(f"country_ipinfo: {country2}")
        logging.info(f"public_ip: {public_ip}")

        return {
            "success": True,
            "server": target_server,
            "proxy_ip": target_ip,
            "public_ip": public_ip,
            "country_ipapi": country1,
            "country_ipinfo": country2
        }


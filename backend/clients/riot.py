import httpx
import os
from dotenv import load_dotenv
import asyncio
from typing import Optional

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
REGION_GROUP = os.getenv("REGION_GROUP", "americas")

class RiotClient:
    def __init__(self):
        if not RIOT_API_KEY:
            raise ValueError("RIOT_API_KEY not found in environment")
        self.headers = {
            "X-Riot-Token": RIOT_API_KEY
        }
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def _request_with_retry(self, url: str, max_retries: int = 3) -> Optional[dict]:
        for attempt in range(max_retries):
            try:
                response = await self.client.get(url, headers=self.headers)
        
                if response.status_code == 200:
                    return response.json()
                
                if response.status_code == 429 or response.status_code >= 500:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                    continue
                
                if response.status_code == 404:
                    return None
                
                response.raise_for_status()
                
            except httpx.HTTPError as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
        
        return None
    
    async def get_account_by_riot_id(self, game_name: str, tag_line: str) -> Optional[dict]:
        url = f"https://{REGION_GROUP}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        return await self._request_with_retry(url)
    
    async def get_match_ids_by_puuid(self, puuid: str, start: int = 0, count: int = 10) -> Optional[list]:
        url = f"https://{REGION_GROUP}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
        return await self._request_with_retry(url)
    
    async def get_match_detail(self, match_id: str) -> Optional[dict]:
        url = f"https://{REGION_GROUP}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        return await self._request_with_retry(url)
    
    async def close(self):
        await self.client.aclose()

riot_client = RiotClient()


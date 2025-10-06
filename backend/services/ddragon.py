import httpx
from services.cache import get_cached, set_cached

DDRAGON_BASE = "https://ddragon.leagueoflegends.com"

async def get_latest_version() -> str:
    cached = get_cached("ddragon_version")
    if cached:
        return cached
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DDRAGON_BASE}/api/versions.json")
        latest = response.json()[0]
        set_cached("ddragon_version", latest)
        return latest

async def get_champion_data() -> dict:
    cached = get_cached("champion_data")
    if cached:
        return cached
    
    version = await get_latest_version()
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DDRAGON_BASE}/cdn/{version}/data/en_US/champion.json")
        data = response.json()
        
        champion_map = {
            champ_data["key"]: {
                "name": champ_data["name"],
                "icon": f"{DDRAGON_BASE}/cdn/{version}/img/champion/{champ_data['id']}.png"
            }
            for champ_data in data["data"].values()
        }
        
        set_cached("champion_data", champion_map)
        return champion_map

def get_champion_name(champion_id: str, champion_map: dict) -> str:
    return champion_map.get(champion_id, {}).get("name", champion_id)


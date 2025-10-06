from clients.riot import riot_client
from models.schemas import Player
from models.db import Account, get_session, engine
from services.cache import get_cached, set_cached
from sqlmodel import Session, select
from datetime import datetime, timezone

async def get_player_by_riot_id(riot_id: str) -> Player:
    cached = get_cached(f"player:{riot_id}")
    if cached:
        return Player(**cached)
    
    parts = riot_id.split("#")
    if len(parts) != 2:
        raise ValueError("Invalid Riot ID format")
    
    game_name, tag_line = parts
    
    with Session(engine) as session:
        account = session.exec(select(Account).where(Account.riot_id == riot_id)).first()
        if account:
            player_data = {
                "puuid": account.puuid,
                "riotId": account.riot_id,
                "region": account.region
            }
            set_cached(f"player:{riot_id}", player_data)
            return Player(**player_data)
    
    api_result = await riot_client.get_account_by_riot_id(game_name, tag_line)
    if not api_result:
        raise ValueError(f"Account not found: {riot_id}")
    
    player_data = {
        "puuid": api_result["puuid"],
        "riotId": f"{api_result['gameName']}#{api_result['tagLine']}",
        "region": "americas"
    }
    
    with Session(engine) as session:
        session.merge(Account(
            puuid=player_data["puuid"],
            riot_id=player_data["riotId"],
            region=player_data["region"],
            updated_at=datetime.now(timezone.utc)
        ))
        session.commit()
    
    set_cached(f"player:{riot_id}", player_data)
    return Player(**player_data)


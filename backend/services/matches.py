from clients.riot import riot_client
from models.schemas import MatchSummary, MatchDetail, PlayerStats
from models.db import Match, engine
from services.cache import get_cached, set_cached
from services.ddragon import get_champion_data, get_champion_name
from sqlmodel import Session, select
from datetime import datetime, timezone
import json

QUEUE_NAMES = {
    400: "Normal Draft",
    420: "Ranked Solo/Duo",
    430: "Normal Blind",
    440: "Ranked Flex",
    450: "ARAM",
    700: "Clash",
    830: "Co-op vs AI (Intro)",
    840: "Co-op vs AI (Beginner)",
    850: "Co-op vs AI (Intermediate)",
    900: "URF",
    1020: "One For All",
    1700: "Arena"
}

DRAFT_QUEUES = {400, 420, 440, 700, 830, 840, 850}

async def get_match_ids(puuid: str) -> list[str]:
    cached = get_cached(f"match_ids:{puuid}")
    if cached:
        return cached
    
    match_ids = await riot_client.get_match_ids_by_puuid(puuid, start=0, count=10)
    if match_ids:
        set_cached(f"match_ids:{puuid}", match_ids)
    return match_ids or []

async def get_match_payload(match_id: str) -> dict:
    cached = get_cached(f"match:{match_id}")
    if cached:
        return cached
    
    with Session(engine) as session:
        match_record = session.exec(select(Match).where(Match.match_id == match_id)).first()
        if match_record:
            payload = json.loads(match_record.payload_json)
            set_cached(f"match:{match_id}", payload)
            return payload
    
    payload = await riot_client.get_match_detail(match_id)
    if not payload:
        raise ValueError(f"Match not found: {match_id}")
    
    with Session(engine) as session:
        session.merge(Match(
            match_id=match_id,
            puuid="",
            payload_json=json.dumps(payload),
            fetched_at=datetime.now(timezone.utc)
        ))
        session.commit()
    
    set_cached(f"match:{match_id}", payload)
    return payload

def extract_participant_data(payload: dict, puuid: str) -> dict:
    for participant in payload["info"]["participants"]:
        if participant["puuid"] == puuid:
            return participant
    raise ValueError(f"PUUID not found in match")

async def get_match_summaries(puuid: str) -> tuple[list[MatchSummary], PlayerStats]:
    match_ids = await get_match_ids(puuid)
    champion_map = await get_champion_data()
    
    summaries = []
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    wins = 0
    losses = 0
    champion_counts = {}
    
    for match_id in match_ids:
        try:
            payload = await get_match_payload(match_id)
            participant = extract_participant_data(payload, puuid)
            
            champion_name = get_champion_name(str(participant["championId"]), champion_map)
            result = "W" if participant["win"] else "L"
            wins += participant["win"]
            losses += not participant["win"]
            
            k, d, a = participant["kills"], participant["deaths"], participant["assists"]
            total_kills += k
            total_deaths += d
            total_assists += a
            champion_counts[champion_name] = champion_counts.get(champion_name, 0) + 1
            
            duration_mins = payload["info"]["gameDuration"] // 60
            date_iso = datetime.fromtimestamp(payload["info"]["gameCreation"] / 1000).isoformat()
            queue_id = payload["info"]["queueId"]
            role = (participant.get("teamPosition") or participant.get("lane")) if queue_id in DRAFT_QUEUES else None
            
            summary = MatchSummary(
                matchId=match_id,
                date=date_iso,
                champion=champion_name,
                role=role,
                k=k,
                d=d,
                a=a,
                result=result,
                durationMins=duration_mins
            )
            summaries.append(summary)
            
        except Exception as e:
            print(f"Error processing match {match_id}: {e}")
            continue
    
    avg_kda = round((total_kills + total_assists) / max(total_deaths, 1), 2)
    top_champions = [
        {"name": name, "count": count}
        for name, count in sorted(champion_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    ]
    
    stats = PlayerStats(
        overallWL=f"{wins}-{losses}",
        avgKDA=avg_kda,
        topChampions=top_champions
    )
    
    return summaries, stats

async def get_match_detail(match_id: str, puuid: str) -> MatchDetail:
    payload = await get_match_payload(match_id)
    participant = extract_participant_data(payload, puuid)
    champion_map = await get_champion_data()
    queue_id = payload["info"]["queueId"]
    
    return MatchDetail(
        matchId=match_id,
        queueId=queue_id,
        queueName=QUEUE_NAMES.get(queue_id, f"Queue {queue_id}"),
        myChampion=get_champion_name(str(participant["championId"]), champion_map),
        k=participant["kills"],
        d=participant["deaths"],
        a=participant["assists"],
        cs=participant["totalMinionsKilled"] + participant.get("neutralMinionsKilled", 0),
        win=participant["win"],
        team="BLUE" if participant["teamId"] == 100 else "RED"
    )


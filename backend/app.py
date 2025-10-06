from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.db import init_db
from models.schemas import Player, MatchSummary, MatchDetail, PlayerStats
from services.account import get_player_by_riot_id
from services.matches import get_match_summaries, get_match_detail
from services.ddragon import get_champion_data
import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("RIOT_API_KEY"):
    raise ValueError("RIOT_API_KEY is missing. Please set it in your .env file.")

app = FastAPI(title="LoLTrack API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def root():
    return {"message": "LoLTrack API is running"}

@app.get("/api/player/{riot_id}")
async def get_player(riot_id: str) -> Player:
    try:
        player = await get_player_by_riot_id(riot_id)
        return player
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/player/{riot_id}/matches")
async def get_player_matches(riot_id: str) -> dict:
    try:
        player = await get_player_by_riot_id(riot_id)
        summaries, stats = await get_match_summaries(player.puuid)
        return {"matches": summaries, "stats": stats}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/match/{match_id}")
async def get_match(match_id: str, puuid: str) -> MatchDetail:
    try:
        detail = await get_match_detail(match_id, puuid)
        return detail
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/static/champions")
async def get_champions() -> dict:
    try:
        champions = await get_champion_data()
        return champions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


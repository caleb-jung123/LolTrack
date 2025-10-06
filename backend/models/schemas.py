from pydantic import BaseModel
from typing import Literal

class Player(BaseModel):
    puuid: str
    riotId: str
    region: str

class MatchSummary(BaseModel):
    matchId: str
    date: str
    champion: str
    role: str | None
    k: int
    d: int
    a: int
    result: Literal["W", "L"]
    durationMins: int

class MatchDetail(BaseModel):
    matchId: str
    queueId: int
    queueName: str
    myChampion: str
    k: int
    d: int
    a: int
    cs: int
    win: bool
    team: Literal["BLUE", "RED"]

class PlayerStats(BaseModel):
    overallWL: str
    avgKDA: float
    topChampions: list[dict]


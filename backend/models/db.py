from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime, timezone
from typing import Optional

def utc_now():
    return datetime.now(timezone.utc)

class Account(SQLModel, table=True):
    __tablename__ = "accounts"
    
    puuid: str = Field(primary_key=True)
    riot_id: str
    region: str
    updated_at: datetime = Field(default_factory=utc_now)

class Match(SQLModel, table=True):
    __tablename__ = "matches"
    
    match_id: str = Field(primary_key=True)
    puuid: str
    payload_json: str
    fetched_at: datetime = Field(default_factory=utc_now)

class StaticCache(SQLModel, table=True):
    __tablename__ = "static_cache"
    
    kind: str = Field(primary_key=True)
    key: str = Field(primary_key=True)
    payload_json: str
    fetched_at: datetime = Field(default_factory=utc_now)

engine = create_engine("sqlite:///loltrack.db")

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


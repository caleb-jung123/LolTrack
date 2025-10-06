const API_BASE = "http://localhost:8000/api";

export async function fetchPlayer(riotId) {
  const response = await fetch(`${API_BASE}/player/${encodeURIComponent(riotId)}`);
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to fetch player");
  }
  return response.json();
}

export async function fetchPlayerMatches(riotId) {
  const response = await fetch(`${API_BASE}/player/${encodeURIComponent(riotId)}/matches`);
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to fetch matches");
  }
  return response.json();
}

export async function fetchMatchDetail(matchId, puuid) {
  const response = await fetch(`${API_BASE}/match/${matchId}?puuid=${puuid}`);
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to fetch match detail");
  }
  return response.json();
}

export async function fetchChampions() {
  const response = await fetch(`${API_BASE}/static/champions`);
  if (!response.ok) {
    throw new Error("Failed to fetch champion data");
  }
  return response.json();
}


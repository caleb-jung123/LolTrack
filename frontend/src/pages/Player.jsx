import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchPlayer, fetchPlayerMatches, fetchChampions } from "../lib/api";
import MatchCard from "../components/MatchCard";
import SearchBar from "../components/SearchBar";

export default function Player() {
  const { riotId } = useParams();
  const navigate = useNavigate();
  
  const [player, setPlayer] = useState(null);
  const [matches, setMatches] = useState([]);
  const [stats, setStats] = useState(null);
  const [champions, setChampions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, [riotId]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [playerData, matchData, championData] = await Promise.all([
        fetchPlayer(riotId),
        fetchPlayerMatches(riotId),
        fetchChampions()
      ]);
      
      setPlayer(playerData);
      setMatches(matchData.matches);
      setStats(matchData.stats);
      setChampions(championData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (newRiotId) => {
    navigate(`/player/${encodeURIComponent(newRiotId)}`);
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
        <button className="btn btn-primary" onClick={() => navigate("/")}>
          Back to Home
        </button>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="mb-4">
        <SearchBar onSearch={handleSearch} />
      </div>

      <div className="player-header mb-4">
        <h2 className="mb-2">{player.riotId}</h2>
        <p className="mb-3 opacity-75">Region: {player.region.toUpperCase()}</p>
        
        {stats && (
          <div className="mb-3">
            <span className="stat-chip bg-light text-dark">
              <strong>W-L:</strong> {stats.overallWL}
            </span>
            <span className="stat-chip bg-light text-dark">
              <strong>Avg KDA:</strong> {stats.avgKDA}
            </span>
          </div>
        )}

        {stats && stats.topChampions.length > 0 && (
          <div>
            <h6 className="mb-2 opacity-75">Top Champions (Last 10)</h6>
            <div>
              {stats.topChampions.map((champ, idx) => (
                <span key={idx} className="badge bg-white text-dark me-2 mb-2">
                  {champ.name} ({champ.count})
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      <h4 className="mb-3 fw-bold">Recent Matches</h4>
      
      {matches.length === 0 ? (
        <p className="text-muted">No matches found</p>
      ) : (
        <div>
          {matches.map((match) => (
            <MatchCard
              key={match.matchId}
              match={match}
              champions={champions}
              puuid={player.puuid}
            />
          ))}
        </div>
      )}
    </div>
  );
}


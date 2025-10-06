import { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { fetchMatchDetail, fetchChampions } from "../lib/api";
import ChampAvatar from "../components/ChampAvatar";
import { formatKDA, calculateKDA } from "../lib/format";

export default function Match() {
  const { matchId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  
  const [match, setMatch] = useState(null);
  const [champions, setChampions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, [matchId]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const searchParams = new URLSearchParams(location.search);
      let puuid = searchParams.get("puuid");
      
      if (!puuid) {
        const savedPuuid = sessionStorage.getItem("currentPuuid");
        if (savedPuuid) {
          puuid = savedPuuid;
        } else {
          throw new Error("PUUID not found. Please navigate from player page.");
        }
      } else {
        sessionStorage.setItem("currentPuuid", puuid);
      }
      
      const [matchData, championData] = await Promise.all([
        fetchMatchDetail(matchId, puuid),
        fetchChampions()
      ]);
      
      setMatch(matchData);
      setChampions(championData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
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
        <button className="btn btn-primary" onClick={() => navigate(-1)}>
          Go Back
        </button>
      </div>
    );
  }

  const resultClass = match.win ? "success" : "danger";
  const resultText = match.win ? "Victory" : "Defeat";
  const headerClass = match.win ? "win" : "loss";

  return (
    <div className="container mt-4">
      <button className="back-button mb-4" onClick={() => navigate(-1)}>
        ← Back to Matches
      </button>

      <div className={`match-detail-header ${headerClass} mb-4`}>
        <div className="p-4">
          <h3 className={`text-${resultClass} mb-4 fw-bold`}>{resultText}</h3>
          
          <div className="row align-items-center">
            <div className="col-auto">
              <ChampAvatar
                championName={match.myChampion}
                champions={champions}
                size={100}
              />
            </div>
            
            <div className="col">
              <h4 className="mb-3 fw-bold">{match.myChampion}</h4>
              <div className="mb-3">
                <span className="stat-chip bg-primary text-white">
                  <strong>KDA:</strong> {formatKDA(match.k, match.d, match.a)}
                </span>
                <span className="stat-chip bg-info text-white">
                  <strong>Ratio:</strong> {calculateKDA(match.k, match.d, match.a)}
                </span>
                <span className="stat-chip bg-secondary text-white">
                  <strong>CS:</strong> {match.cs}
                </span>
              </div>
              <div>
                <span className={`badge ${match.team === "BLUE" ? "bg-primary" : "bg-danger"} me-2 px-3 py-2`}>
                  {match.team} TEAM
                </span>
                <span className="badge bg-secondary px-3 py-2">
                  {match.queueName}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}


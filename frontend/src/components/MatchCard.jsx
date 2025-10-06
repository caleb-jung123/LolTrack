import { useNavigate } from "react-router-dom";
import ChampAvatar from "./ChampAvatar";
import { formatKDA, formatDuration, formatDate, roleToDisplay } from "../lib/format";

export default function MatchCard({ match, champions, puuid }) {
  const navigate = useNavigate();

  const resultClass = match.result === "W" ? "success" : "danger";

  const handleClick = () => {
    navigate(`/match/${match.matchId}?puuid=${puuid}`);
  };

  const cardClass = match.result === "W" ? "win" : "loss";

  return (
    <div
      className={`card match-card ${cardClass} mb-3`}
      onClick={handleClick}
    >
      <div className="card-body d-flex align-items-center py-3">
        <div className="me-3">
          <ChampAvatar championName={match.champion} champions={champions} size={56} />
        </div>
        
        <div className="flex-grow-1">
          <h6 className="mb-1 fw-bold">{match.champion}</h6>
          <small className="text-muted">
            {match.role ? `${roleToDisplay(match.role)} • ` : ""}{formatDate(match.date)}
          </small>
        </div>

        <div className="text-center me-4">
          <div className="fw-bold fs-5">{formatKDA(match.k, match.d, match.a)}</div>
          <small className="text-muted">KDA</small>
        </div>

        <div className="text-center me-4">
          <span className={`badge bg-${resultClass} fs-6 px-3 py-2`}>
            {match.result}
          </span>
        </div>

        <div className="text-center">
          <div className="text-muted fw-semibold">{formatDuration(match.durationMins)}</div>
        </div>
      </div>
    </div>
  );
}


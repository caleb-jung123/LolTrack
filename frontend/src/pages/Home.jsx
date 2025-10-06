import { useNavigate } from "react-router-dom";
import SearchBar from "../components/SearchBar";

export default function Home() {
  const navigate = useNavigate();

  const handleSearch = (riotId) => {
    navigate(`/player/${encodeURIComponent(riotId)}`);
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-10 col-lg-8">
          <div className="hero-section text-center mb-5">
            <h1>LoLTrack</h1>
          </div>
          
          <div className="search-container">
            <SearchBar onSearch={handleSearch} />
          </div>
        </div>
      </div>
    </div>
  );
}


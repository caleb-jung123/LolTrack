import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Player from "./pages/Player";
import Match from "./pages/Match";

function App() {
  return (
    <Router>
      <div className="min-vh-100">
        <nav className="navbar navbar-dark bg-dark">
          <div className="container">
            <a className="navbar-brand fw-bold fs-4" href="/">
              🎮 LoLTrack
            </a>
          </div>
        </nav>
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/player/:riotId" element={<Player />} />
          <Route path="/match/:matchId" element={<Match />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

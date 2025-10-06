import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSearch(input.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <div className="input-group input-group-lg">
        <input
          type="text"
          className="form-control"
          placeholder="Enter Riot ID (name#tag)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="btn btn-primary" type="submit">
          Search
        </button>
      </div>
      <small className="form-text text-muted d-block mt-3">
        Example: Hide on bush#KR1
      </small>
    </form>
  );
}


export function formatKDA(k, d, a) {
  return `${k} / ${d} / ${a}`;
}

export function calculateKDA(k, d, a) {
  if (d === 0) return ((k + a) / 1).toFixed(2);
  return ((k + a) / d).toFixed(2);
}

export function formatDuration(minutes) {
  return `${minutes}m`;
}

export function formatDate(isoString) {
  const date = new Date(isoString);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  
  if (diffDays > 0) return `${diffDays}d ago`;
  if (diffHours > 0) return `${diffHours}h ago`;
  if (diffMins > 0) return `${diffMins}m ago`;
  return "just now";
}

export function roleToDisplay(role) {
  if (!role) return "";
  const roleMap = {
    "TOP": "Top",
    "JUNGLE": "Jungle",
    "MIDDLE": "Mid",
    "BOTTOM": "ADC",
    "UTILITY": "Support"
  };
  return roleMap[role] || role;
}


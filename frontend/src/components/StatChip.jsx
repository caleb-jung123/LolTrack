export default function StatChip({ label, value, variant = "secondary" }) {
  return (
    <span className={`badge bg-${variant} me-2`}>
      {label}: {value}
    </span>
  );
}


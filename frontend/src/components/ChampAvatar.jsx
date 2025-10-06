import placeholderIcon from '../assets/placeholder.svg';

export default function ChampAvatar({ championName, champions, size = 48 }) {
  let iconUrl = "";
  
  if (champions) {
    for (const champId in champions) {
      if (champions[champId].name === championName) {
        iconUrl = champions[champId].icon;
        break;
      }
    }
  }

  return (
    <img
      src={iconUrl || placeholderIcon}
      alt={championName}
      width={size}
      height={size}
      className="rounded champ-avatar"
      style={{ objectFit: "cover" }}
    />
  );
}


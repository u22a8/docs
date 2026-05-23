export const ScoreAxis = () => {
  // DR 021 tier palette
  const WEAK = "#8a7f68";
  const DEVELOPING = "#c17338";
  const SOLID = "#2e6b42";
  const STRONG = "#1e3a8a";
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 700 130"
      role="img"
      aria-label="The 0 to 100 score axis split into Weak, Developing, Solid, and Strong by three breaks."
      style={{ width: "100%", height: "auto" }}
    >
      <title>Score axis with tiers and breaks</title>

      <rect x="50" y="58" width="210" height="28" fill={WEAK} fillOpacity="0.85" />
      <rect x="260" y="58" width="162" height="28" fill={DEVELOPING} fillOpacity="0.85" />
      <rect x="422" y="58" width="120" height="28" fill={SOLID} fillOpacity="0.85" />
      <rect x="542" y="58" width="108" height="28" fill={STRONG} fillOpacity="0.85" />
      <line x1="50" y1="86" x2="650" y2="86" stroke="currentColor" strokeOpacity="0.25" />

      <line x1="260" y1="50" x2="260" y2="98" stroke="currentColor" strokeOpacity="0.4" strokeDasharray="3 3" />
      <line x1="422" y1="50" x2="422" y2="98" stroke="currentColor" strokeOpacity="0.4" strokeDasharray="3 3" />
      <line x1="542" y1="50" x2="542" y2="98" stroke="currentColor" strokeOpacity="0.4" strokeDasharray="3 3" />
      <text x="260" y="44" fill="currentColor" fillOpacity="0.75" fontSize="11" textAnchor="middle">developing</text>
      <text x="422" y="44" fill="currentColor" fillOpacity="0.75" fontSize="11" textAnchor="middle">solid</text>
      <text x="542" y="44" fill="currentColor" fillOpacity="0.75" fontSize="11" textAnchor="middle">strong</text>

      <text x="155" y="116" fill="currentColor" fontSize="12" textAnchor="middle">Weak</text>
      <text x="341" y="116" fill="currentColor" fontSize="12" textAnchor="middle">Developing</text>
      <text x="482" y="116" fill="currentColor" fontSize="12" textAnchor="middle">Solid</text>
      <text x="596" y="116" fill="currentColor" fontSize="12" textAnchor="middle">Strong</text>
    </svg>
  );
};

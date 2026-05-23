export const HeadroomGap = () => {
  // DR 021 tier palette + cobalt data marker
  const SOLID = "#2e6b42";
  const STRONG = "#1e3a8a";
  const COBALT = "#1e3a8a";
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 700 140"
      role="img"
      aria-label="A Solid score and the gap, its headroom, to the Strong break above it."
      style={{ width: "100%", height: "auto" }}
    >
      <title>Headroom is the gap to the next break</title>
      <rect x="120" y="58" width="300" height="28" fill={SOLID} fillOpacity="0.85" />
      <rect x="420" y="58" width="180" height="28" fill={STRONG} fillOpacity="0.85" />
      <line x1="120" y1="86" x2="600" y2="86" stroke="currentColor" strokeOpacity="0.25" />

      <line x1="420" y1="50" x2="420" y2="96" stroke="currentColor" strokeOpacity="0.4" strokeDasharray="3 3" />
      <text x="420" y="44" fill="currentColor" fillOpacity="0.75" fontSize="11" textAnchor="middle">strong</text>

      <text x="270" y="122" fill="currentColor" fontSize="12" textAnchor="middle">Solid</text>
      <text x="510" y="122" fill="currentColor" fontSize="12" textAnchor="middle">Strong</text>

      <polygon points="354,48 366,48 360,58" fill={COBALT} />
      <text x="360" y="42" fill={COBALT} fontSize="11" fontWeight="600" textAnchor="middle">score</text>

      <line x1="360" y1="104" x2="414" y2="104" stroke={COBALT} strokeWidth="1.5" />
      <polygon points="414,100 420,104 414,108" fill={COBALT} />
      <text x="387" y="100" fill={COBALT} fontSize="11" textAnchor="middle">headroom</text>
    </svg>
  );
};

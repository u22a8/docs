export const ScoreTypeGlyphs = () => {
  const COBALT = "#1e3a8a"; // data / active points (DR 021)
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 700 170"
      role="img"
      aria-label="Four glyphs, one per trait type: topic, spectrum, claim, and outlier, each a distinct geometry."
      style={{ width: "100%", height: "auto" }}
    >
      <title>The four trait-type geometries</title>

      {/* topic */}
      <circle cx="90" cy="75" r="34" fill="none" stroke="currentColor" strokeOpacity="0.35" strokeDasharray="4 4" />
      <circle cx="90" cy="75" r="6" fill={COBALT} />
      <circle cx="112" cy="58" r="4" fill={COBALT} fillOpacity="0.7" />
      <text x="90" y="150" fill="currentColor" fontSize="13" fontWeight="600" textAnchor="middle">topic</text>

      {/* spectrum */}
      <line x1="210" y1="75" x2="320" y2="75" stroke="currentColor" strokeOpacity="0.4" strokeWidth="2" />
      <circle cx="210" cy="75" r="5" fill="currentColor" fillOpacity="0.4" />
      <circle cx="320" cy="75" r="5" fill={COBALT} />
      <polygon points="291,62 301,62 296,70" fill={COBALT} />
      <text x="265" y="150" fill="currentColor" fontSize="13" fontWeight="600" textAnchor="middle">spectrum</text>

      {/* claim */}
      <line x1="405" y1="110" x2="495" y2="110" stroke="currentColor" strokeOpacity="0.4" />
      <line x1="405" y1="110" x2="405" y2="45" stroke="currentColor" strokeOpacity="0.4" />
      <polygon points="495,107 501,110 495,113" fill="currentColor" fillOpacity="0.4" />
      <polygon points="402,45 408,45 405,39" fill="currentColor" fillOpacity="0.4" />
      <circle cx="475" cy="65" r="5" fill={COBALT} />
      <text x="450" y="150" fill="currentColor" fontSize="13" fontWeight="600" textAnchor="middle">claim</text>

      {/* outlier */}
      <ellipse cx="600" cy="80" rx="34" ry="24" fill="none" stroke="currentColor" strokeOpacity="0.35" strokeDasharray="4 4" />
      <circle cx="590" cy="78" r="3" fill="currentColor" fillOpacity="0.4" />
      <circle cx="606" cy="72" r="3" fill="currentColor" fillOpacity="0.4" />
      <circle cx="598" cy="88" r="3" fill="currentColor" fillOpacity="0.4" />
      <circle cx="610" cy="84" r="3" fill="currentColor" fillOpacity="0.4" />
      <line x1="600" y1="80" x2="652" y2="50" stroke={COBALT} strokeOpacity="0.5" strokeDasharray="3 3" />
      <circle cx="652" cy="50" r="5" fill={COBALT} />
      <text x="615" y="150" fill="currentColor" fontSize="13" fontWeight="600" textAnchor="middle">outlier</text>
    </svg>
  );
};

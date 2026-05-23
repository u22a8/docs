export const ScoreCardFigure = () => {
  const COBALT = "#1e3a8a"; // data / composite (DR 021)
  const rows = [
    { key: "intent_clarity", score: 77, w: 293 },
    { key: "scope_precision", score: 85, w: 323 },
    { key: "actionable_summary", score: 84, w: 319 },
    { key: "context_sufficiency", score: 71, w: 270 },
    { key: "signal_density", score: 86, w: 327 },
  ];
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 680 270"
      role="img"
      aria-label="A score card with a composite, a confidence signal, and one bar per trait."
      style={{ width: "100%", height: "auto" }}
    >
      <title>Score card</title>
      <text x="24" y="40" fill="currentColor" fontSize="16" fontWeight="600">
        u22a8.commit-message
      </text>
      <text x="656" y="44" fill={COBALT} fontSize="34" fontWeight="700" textAnchor="end">
        80
      </text>
      <text x="656" y="62" fill="currentColor" fillOpacity="0.7" fontSize="12" textAnchor="end">
        composite · moderate confidence
      </text>
      <line x1="24" y1="80" x2="656" y2="80" stroke="currentColor" strokeOpacity="0.15" />
      {rows.map((r, i) => {
        const y = 110 + i * 32;
        return (
          <g key={r.key}>
            <text x="24" y={y + 4} fill="currentColor" fontSize="13">
              {r.key}
            </text>
            <rect x="210" y={y - 11} width="380" height="14" rx="7" fill="currentColor" fillOpacity="0.08" />
            <rect x="210" y={y - 11} width={r.w} height="14" rx="7" fill={COBALT} fillOpacity="0.85" />
            <text x="602" y={y + 4} fill="currentColor" fontSize="13" fontWeight="600">
              {r.score}
            </text>
          </g>
        );
      })}
    </svg>
  );
};

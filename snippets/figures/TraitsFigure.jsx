export const TraitsFigure = () => {
  const COBALT = "#1e3a8a"; // data / positive pole + marker (DR 021)
  const traits = [
    { name: "intent_clarity", pos: 508 },
    { name: "scope_precision", pos: 522 },
    { name: "context_sufficiency", pos: 509 },
    { name: "signal_density", pos: 523 },
  ];
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 680 210"
      role="img"
      aria-label="A model fans out into several traits; each trait is an axis of judgment with a negative and a positive pole and a position for the scored content."
      style={{ width: "100%", height: "auto" }}
    >
      <title>A model and its traits</title>
      <rect x="30" y="83" width="120" height="44" rx="8" fill="currentColor" fillOpacity="0.06" stroke="currentColor" strokeOpacity="0.3" />
      <text x="90" y="109" fill="currentColor" fontSize="13" fontWeight="600" textAnchor="middle">model</text>
      {traits.map((t, i) => {
        const y = 45 + i * 48;
        return (
          <g key={t.name}>
            <line x1="150" y1="105" x2="300" y2={y} stroke="currentColor" strokeOpacity="0.25" />
            <rect x="300" y={y - 14} width="250" height="28" rx="14" fill="currentColor" fillOpacity="0.04" stroke="currentColor" strokeOpacity="0.15" />
            <text x="314" y={y + 4} fill="currentColor" fontSize="12">{t.name}</text>
            <line x1="445" y1={y} x2="535" y2={y} stroke="currentColor" strokeOpacity="0.35" />
            <circle cx="445" cy={y} r="3" fill="currentColor" fillOpacity="0.4" />
            <circle cx="535" cy={y} r="3" fill={COBALT} />
            <circle cx={t.pos} cy={y} r="4.5" fill={COBALT} />
          </g>
        );
      })}
    </svg>
  );
};

export const SamplesFigure = () => {
  const COBALT = "#1e3a8a";
  const chips = [
    { x: 40, y: 56, pos: false }, { x: 40, y: 106, pos: false }, { x: 40, y: 156, pos: false },
    { x: 400, y: 56, pos: true }, { x: 400, y: 106, pos: true }, { x: 400, y: 156, pos: true },
  ];
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 680 214"
      role="img"
      aria-label="Two columns of labelled content chips, negative on the left and positive on the right, marking a trait's two poles."
      style={{ width: "100%", height: "auto" }}
    >
      <title>A sample is content plus a label; positives and negatives set a trait's poles</title>

      <text x="140" y="36" fill="currentColor" fontSize="12" textAnchor="middle">negative samples</text>
      <text x="500" y="36" fill="currentColor" fontSize="12" textAnchor="middle">positive samples</text>

      {chips.map((c, i) => (
        <g key={i}>
          <rect x={c.x} y={c.y} width="200" height="38" rx="5" fill="none" stroke="currentColor" strokeOpacity="0.35" />
          <line x1={c.x + 14} y1={c.y + 15} x2={c.x + 150} y2={c.y + 15} stroke="currentColor" strokeOpacity="0.45" strokeWidth="2" />
          <line x1={c.x + 14} y1={c.y + 25} x2={c.x + 118} y2={c.y + 25} stroke="currentColor" strokeOpacity="0.22" strokeWidth="2" />
          <circle cx={c.x + 176} cy={c.y + 19} r="11" fill={c.pos ? COBALT : "none"} fillOpacity={c.pos ? "0.9" : "1"} stroke={c.pos ? "none" : "currentColor"} strokeOpacity="0.55" />
          <text x={c.x + 176} y={c.y + 23} fill={c.pos ? "#efe7d6" : "currentColor"} fontSize="13" textAnchor="middle">{c.pos ? "+" : "−"}</text>
        </g>
      ))}
    </svg>
  );
};

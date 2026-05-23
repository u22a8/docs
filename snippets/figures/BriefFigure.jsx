export const BriefFigure = () => {
  const COBALT = "#1e3a8a";
  const rows = [0, 1, 2, 3, 4, 5];
  const dots = [
    { x: 470, y: 72, pos: true }, { x: 520, y: 96, pos: true }, { x: 562, y: 76, pos: true },
    { x: 480, y: 140, pos: false }, { x: 540, y: 150, pos: false }, { x: 592, y: 130, pos: false },
  ];
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 680 228"
      role="img"
      aria-label="A brief document of six lines on the left is synthesized into positive and negative sample dots on the right."
      style={{ width: "100%", height: "auto" }}
    >
      <title>A brief states intent; the build synthesizes samples from it</title>

      <text x="150" y="32" fill="currentColor" fontSize="12" textAnchor="middle">brief</text>
      <rect x="40" y="44" width="220" height="150" rx="6" fill="none" stroke="currentColor" strokeOpacity="0.4" />
      {rows.map((r) => (
        <line key={r} x1="60" y1={68 + r * 21} x2={r % 2 ? 200 : 232} y2={68 + r * 21} stroke="currentColor" strokeOpacity="0.4" strokeWidth="2" />
      ))}

      <line x1="284" y1="118" x2="372" y2="118" stroke="currentColor" strokeOpacity="0.5" strokeWidth="1.5" markerEnd="url(#briefArrow)" />
      <text x="328" y="108" fill="currentColor" fillOpacity="0.7" fontSize="11" textAnchor="middle">synthesize</text>

      <text x="532" y="32" fill="currentColor" fontSize="12" textAnchor="middle">synthesized samples</text>
      {dots.map((d, i) => (
        <circle key={i} cx={d.x} cy={d.y} r="6" fill={d.pos ? COBALT : "none"} fillOpacity={d.pos ? "0.85" : "1"} stroke={d.pos ? "none" : "currentColor"} strokeOpacity="0.55" />
      ))}

      <defs>
        <marker id="briefArrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="currentColor" fillOpacity="0.5" />
        </marker>
      </defs>
    </svg>
  );
};

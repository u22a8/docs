export const VersionsFigure = () => {
  const COBALT = "#1e3a8a";
  const nodes = [
    { x: 110, label: "v1" }, { x: 270, label: "v2" }, { x: 430, label: "v3" }, { x: 590, label: "v4" },
  ];
  const ACTIVE_X = 430; // active = v3, rolled back from v4
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 680 176"
      role="img"
      aria-label="Four version nodes on a timeline; an active pointer marks v3, a tag named stable sits under v2, and a rollback arrow curves from v4 to v3."
      style={{ width: "100%", height: "auto" }}
    >
      <title>Versions are training snapshots; an active pointer selects which one serves scoring</title>

      <line x1="90" y1="96" x2="610" y2="96" stroke="currentColor" strokeOpacity="0.25" />
      {nodes.map((n, i) => (
        <g key={i}>
          <circle cx={n.x} cy="96" r="9" fill="none" stroke="currentColor" strokeOpacity="0.6" />
          <text x={n.x} y="130" fill="currentColor" fontSize="12" textAnchor="middle">{n.label}</text>
        </g>
      ))}

      <circle cx={ACTIVE_X} cy="96" r="9" fill={COBALT} fillOpacity="0.9" />
      <path d={`M${ACTIVE_X - 7},50 L${ACTIVE_X + 7},50 L${ACTIVE_X},64 Z`} fill={COBALT} />
      <text x={ACTIVE_X} y="42" fill={COBALT} fontSize="12" fontWeight="600" textAnchor="middle">active</text>

      <rect x="240" y="140" width="60" height="20" rx="10" fill="none" stroke="currentColor" strokeOpacity="0.4" />
      <text x="270" y="154" fill="currentColor" fillOpacity="0.8" fontSize="11" textAnchor="middle">stable</text>

      <path d="M585,82 Q512,46 442,84" fill="none" stroke="currentColor" strokeOpacity="0.45" strokeDasharray="3 3" markerEnd="url(#rbArrow)" />
      <text x="512" y="50" fill="currentColor" fillOpacity="0.65" fontSize="11" textAnchor="middle">rollback</text>

      <defs>
        <marker id="rbArrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="currentColor" fillOpacity="0.5" />
        </marker>
      </defs>
    </svg>
  );
};

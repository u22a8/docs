export const ModelFigure = () => {
  const COBALT = "#1e3a8a"; // examples + learned axis (DR 021 data/structure)
  const neg = [[70, 150], [98, 126], [60, 120], [102, 156]];
  const pos = [[172, 70], [150, 92], [186, 96], [158, 60]];
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 680 210"
      role="img"
      aria-label="Labelled examples on the left are fit into a learned axis on the right; new content projects onto the axis to a position."
      style={{ width: "100%", height: "auto" }}
    >
      <title>A model is a geometry learned from labelled examples</title>

      <text x="120" y="28" fill="currentColor" fontSize="12" textAnchor="middle">labelled examples</text>
      {neg.map((p, i) => (
        <circle key={`n${i}`} cx={p[0]} cy={p[1]} r="6" fill="none" stroke="currentColor" strokeOpacity="0.55" />
      ))}
      {pos.map((p, i) => (
        <circle key={`p${i}`} cx={p[0]} cy={p[1]} r="6" fill={COBALT} fillOpacity="0.85" />
      ))}

      <line x1="240" y1="105" x2="322" y2="105" stroke="currentColor" strokeOpacity="0.5" strokeWidth="1.5" markerEnd="url(#modelArrow)" />
      <text x="281" y="95" fill="currentColor" fillOpacity="0.7" fontSize="11" textAnchor="middle">train</text>

      <line x1="380" y1="150" x2="620" y2="60" stroke={COBALT} strokeWidth="2" />
      <text x="512" y="140" fill={COBALT} fontSize="12" textAnchor="middle">learned axis</text>

      <circle cx="470" cy="78" r="5" fill="currentColor" />
      <text x="470" y="66" fill="currentColor" fontSize="11" textAnchor="middle">content</text>
      <line x1="470" y1="78" x2="500" y2="105" stroke="currentColor" strokeOpacity="0.4" strokeDasharray="3 3" />
      <circle cx="500" cy="105" r="4" fill="none" stroke={COBALT} />

      <defs>
        <marker id="modelArrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="currentColor" fillOpacity="0.5" />
        </marker>
      </defs>
    </svg>
  );
};

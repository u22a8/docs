export const CompositePull = () => {
  const COBALT = "#1e3a8a"; // data dots + composite marker (DR 021)
  const dots = [
    { v: 85, x: 543 },
    { v: 80, x: 514 },
    { v: 30, x: 224 },
    { v: 78, x: 502 },
  ];
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 680 145"
      role="img"
      aria-label="Four trait scores on a 0 to 100 axis; the composite, a harmonic mean, sits below the simple average, pulled down by the one weak trait."
      style={{ width: "100%", height: "auto" }}
    >
      <title>The composite is pulled down by the weakest trait</title>
      <line x1="50" y1="70" x2="630" y2="70" stroke="currentColor" strokeOpacity="0.2" />
      {dots.map((d) => (
        <g key={d.v}>
          <circle cx={d.x} cy="70" r="5" fill={COBALT} fillOpacity="0.85" />
          <text x={d.x} y="56" fill="currentColor" fillOpacity="0.7" fontSize="10" textAnchor="middle">{d.v}</text>
        </g>
      ))}

      <line x1="446" y1="58" x2="446" y2="104" stroke="currentColor" strokeOpacity="0.5" strokeDasharray="3 3" />
      <text x="446" y="118" fill="currentColor" fillOpacity="0.7" fontSize="11" textAnchor="middle">average 68</text>

      <line x1="380" y1="52" x2="380" y2="110" stroke={COBALT} strokeWidth="2" />
      <text x="380" y="134" fill={COBALT} fontSize="12" fontWeight="600" textAnchor="middle">composite 57</text>
    </svg>
  );
};

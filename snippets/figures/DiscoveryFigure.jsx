export const DiscoveryFigure = () => {
  const COBALT = "#1e3a8a";
  const pts = [
    [250, 152], [292, 136], [332, 120], [372, 108], [412, 96], [452, 84],
    [272, 160], [312, 142], [352, 128], [392, 112], [432, 100],
    [242, 136], [302, 118], [362, 134], [422, 118], [302, 100], [402, 130],
  ];
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 680 226"
      role="img"
      aria-label="A cloud of sample points with two fitted axes through it: a long primary axis labelled trait 1 and a shorter axis labelled trait 2."
      style={{ width: "100%", height: "auto" }}
    >
      <title>Discovery fits intrinsic axes to a model's samples</title>

      {pts.map((p, i) => (
        <circle key={i} cx={p[0]} cy={p[1]} r="5" fill="currentColor" fillOpacity="0.4" />
      ))}

      <line x1="228" y1="166" x2="470" y2="78" stroke={COBALT} strokeWidth="2" markerEnd="url(#discArrow)" />
      <text x="500" y="78" fill={COBALT} fontSize="12">trait 1</text>

      <line x1="372" y1="160" x2="332" y2="84" stroke={COBALT} strokeWidth="1.5" strokeOpacity="0.6" markerEnd="url(#discArrow)" />
      <text x="300" y="78" fill={COBALT} fillOpacity="0.75" fontSize="11" textAnchor="end">trait 2</text>

      <defs>
        <marker id="discArrow" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill={COBALT} />
        </marker>
      </defs>
    </svg>
  );
};

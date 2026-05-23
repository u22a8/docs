export const ConfidenceClusters = () => {
  const COBALT = "#1e3a8a"; // data / positive cluster (DR 021)
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 680 160"
      role="img"
      aria-label="Two training clusters on the score axis: confidence is high inside a cluster and moderate in the gap between them."
      style={{ width: "100%", height: "auto" }}
    >
      <title>Confidence regions over the training clusters</title>
      <line x1="60" y1="120" x2="620" y2="120" stroke="currentColor" strokeOpacity="0.25" />

      <polygon points="100,120 190,55 280,120" fill="currentColor" fillOpacity="0.12" stroke="currentColor" strokeOpacity="0.4" />
      <polygon points="380,120 470,55 560,120" fill={COBALT} fillOpacity="0.18" stroke={COBALT} strokeOpacity="0.6" />

      <text x="190" y="46" fill="currentColor" fillOpacity="0.6" fontSize="10" textAnchor="middle">negative cluster</text>
      <text x="470" y="46" fill="currentColor" fillOpacity="0.6" fontSize="10" textAnchor="middle">positive cluster</text>

      <text x="190" y="142" fill="currentColor" fontSize="12" textAnchor="middle">high</text>
      <text x="335" y="142" fill="currentColor" fontSize="12" textAnchor="middle">moderate</text>
      <text x="470" y="142" fill="currentColor" fontSize="12" textAnchor="middle">high</text>
    </svg>
  );
};

export const BreaksDistribution = () => {
  // DR 021: cobalt = data; break lines carry the tier they open into.
  const COBALT = "#1e3a8a";
  const DEVELOPING = "#c17338";
  const SOLID = "#2e6b42";
  const STRONG = "#1e3a8a";
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 700 160"
      role="img"
      aria-label="Two training distributions on the score axis; each break sits at a quartile of a cluster."
      style={{ width: "100%", height: "auto" }}
    >
      <title>Breaks sit at training-cluster quartiles</title>
      <line x1="50" y1="125" x2="650" y2="125" stroke="currentColor" strokeOpacity="0.25" />

      <polygon points="120,125 235,62 350,125" fill="currentColor" fillOpacity="0.12" stroke="currentColor" strokeOpacity="0.4" />
      <polygon points="360,125 480,56 600,125" fill={COBALT} fillOpacity="0.16" stroke={COBALT} strokeOpacity="0.6" />
      <text x="235" y="54" fill="currentColor" fillOpacity="0.6" fontSize="10" textAnchor="middle">negatives</text>
      <text x="480" y="48" fill="currentColor" fillOpacity="0.6" fontSize="10" textAnchor="middle">positives</text>

      <line x1="305" y1="46" x2="305" y2="132" stroke={DEVELOPING} strokeOpacity="0.85" strokeDasharray="4 3" />
      <line x1="410" y1="46" x2="410" y2="132" stroke={SOLID} strokeOpacity="0.85" strokeDasharray="4 3" />
      <line x1="545" y1="46" x2="545" y2="132" stroke={STRONG} strokeOpacity="0.85" strokeDasharray="4 3" />

      <text x="305" y="40" fill="currentColor" fontSize="11" fontWeight="600" textAnchor="middle">developing</text>
      <text x="410" y="40" fill="currentColor" fontSize="11" fontWeight="600" textAnchor="middle">solid</text>
      <text x="545" y="40" fill="currentColor" fontSize="11" fontWeight="600" textAnchor="middle">strong</text>

      <text x="305" y="147" fill="currentColor" fillOpacity="0.55" fontSize="9" textAnchor="middle">neg p75</text>
      <text x="410" y="147" fill="currentColor" fillOpacity="0.55" fontSize="9" textAnchor="middle">pos p25</text>
      <text x="545" y="147" fill="currentColor" fillOpacity="0.55" fontSize="9" textAnchor="middle">pos p75</text>
    </svg>
  );
};

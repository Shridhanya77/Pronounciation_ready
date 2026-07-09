function ScoreCard({ label, value, darkMode }) {
  return (
    <div className={`rounded-2xl border p-4 shadow-sm ${darkMode ? 'border-slate-800 bg-slate-900/90' : 'border-slate-200 bg-white'}`}>
      <p className="text-sm uppercase tracking-[0.2em] text-slate-400">{label}</p>
      <p className="mt-2 text-3xl font-semibold">{value}</p>
    </div>
  );
}

export default ScoreCard;

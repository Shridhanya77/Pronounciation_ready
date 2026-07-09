function Transcript({ transcript, darkMode }) {
  return (
    <div className={`rounded-3xl border p-5 shadow-lg ${darkMode ? 'border-slate-800 bg-slate-900/90' : 'border-slate-200 bg-white'}`}>
      <h3 className="text-xl font-semibold">Transcript</h3>
      <p className={`mt-3 leading-7 ${darkMode ? 'text-slate-300' : 'text-slate-700'}`}>{transcript || 'No transcript available yet.'}</p>
    </div>
  );
}

export default Transcript;

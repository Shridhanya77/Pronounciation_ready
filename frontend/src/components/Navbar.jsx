function Navbar({ darkMode, onToggle }) {
  return (
    <header className={`border-b ${darkMode ? 'border-slate-800 bg-slate-950/80' : 'border-slate-200 bg-white/80'}`}>
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.35em] text-cyan-400">Livo AI</p>
          <h2 className="text-xl font-semibold">Pronunciation Assessment</h2>
        </div>
        <button
          onClick={onToggle}
          className={`rounded-full border px-4 py-2 text-sm font-medium transition ${darkMode ? 'border-slate-700 bg-slate-900 text-slate-100 hover:bg-slate-800' : 'border-slate-300 bg-slate-100 text-slate-900 hover:bg-slate-200'}`}
        >
          {darkMode ? '☀️ Light' : '🌙 Dark'}
        </button>
      </div>
    </header>
  );
}

export default Navbar;

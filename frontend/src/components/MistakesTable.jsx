function MistakesTable({ mistakes, darkMode }) {
  if (!mistakes?.length) {
    return (
      <div className={`rounded-3xl border p-5 shadow-lg ${darkMode ? 'border-slate-800 bg-slate-900/90' : 'border-slate-200 bg-white'}`}>
        <h3 className="text-xl font-semibold">Pronunciation Mistakes</h3>
        <p className={`mt-3 ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>No specific mistakes detected from this sample.</p>
      </div>
    );
  }

  return (
    <div className={`overflow-hidden rounded-3xl border shadow-lg ${darkMode ? 'border-slate-800 bg-slate-900/90' : 'border-slate-200 bg-white'}`}>
      <div className="border-b border-slate-800 px-5 py-4">
        <h3 className="text-xl font-semibold">Pronunciation Mistakes</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className={darkMode ? 'bg-slate-950/60 text-slate-400' : 'bg-slate-50 text-slate-500'}>
            <tr>
              <th className="px-5 py-3">Word</th>
              <th className="px-5 py-3">Type</th>
              <th className="px-5 py-3">Reason</th>
              <th className="px-5 py-3">Suggestion</th>
            </tr>
          </thead>
          <tbody>
            {mistakes.map((mistake, index) => (
              <tr key={`${mistake.word}-${index}`} className={darkMode ? 'border-t border-slate-800' : 'border-t border-slate-200'}>
                <td className="px-5 py-3 font-semibold">{mistake.word}</td>
                <td className="px-5 py-3">{mistake.type}</td>
                <td className="px-5 py-3">{mistake.reason}</td>
                <td className="px-5 py-3">{mistake.suggestion}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default MistakesTable;

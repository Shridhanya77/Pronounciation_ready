import ScoreCard from './ScoreCard';
import Transcript from './Transcript';
import MistakesTable from './MistakesTable';

function Result({ result, darkMode }) {
  const scores = [
    { label: 'Overall', value: `${result.overall_score ?? 0}` },
    { label: 'Accuracy', value: `${result.accuracy ?? 0}` },
    { label: 'Fluency', value: `${result.fluency ?? 0}` },
    { label: 'Completeness', value: `${result.completeness ?? 0}` },
  ];

  return (
    <section className="space-y-6">
      <div className={`rounded-[2rem] border p-6 shadow-2xl ${darkMode ? 'border-slate-800 bg-slate-900/90' : 'border-slate-200 bg-white'}`}>
        <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Assessment summary</p>
            <h2 className="mt-2 text-3xl font-semibold">Pronunciation score {result.overall_score ?? 0}/100</h2>
            <p className={`mt-4 max-w-2xl leading-7 ${darkMode ? 'text-slate-300' : 'text-slate-700'}`}>
              {result.explanation || 'Your recording was analyzed with learner-friendly feedback to help you improve clarity and fluency.'}
            </p>
          </div>
          <div className="flex h-32 w-32 items-center justify-center rounded-full border-[10px] border-cyan-500 text-4xl font-semibold">
            {result.overall_score ?? 0}
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        {scores.map((score) => (
          <ScoreCard key={score.label} label={score.label} value={`${score.value}/100`} darkMode={darkMode} />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <Transcript transcript={result.transcript} darkMode={darkMode} />
        <div className={`rounded-3xl border p-5 shadow-lg ${darkMode ? 'border-slate-800 bg-slate-900/90' : 'border-slate-200 bg-white'}`}>
          <h3 className="text-xl font-semibold">Improvement Tips</h3>
          <ul className="mt-4 space-y-3">
            {(result.general_suggestions || []).map((suggestion) => (
              <li key={suggestion} className={`rounded-2xl border px-4 py-3 ${darkMode ? 'border-slate-800 bg-slate-950/50' : 'border-slate-200 bg-slate-50'}`}>
                {suggestion}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <MistakesTable mistakes={result.mistakes} darkMode={darkMode} />
    </section>
  );
}

export default Result;

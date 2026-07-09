import { useMemo, useState } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import Upload from './components/Upload';
import Result from './components/Result';
import Footer from './components/Footer';
import Loading from './components/Loading';

const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [fileName, setFileName] = useState('');

  const handleUpload = async (file) => {
    if (!file) {
      setError('Please choose an audio file first.');
      return;
    }

    setIsLoading(true);
    setError('');
    setProgress(10);
    setFileName(file.name);

    const formData = new FormData();
    formData.append('audio', file);

    try {
      const response = await axios.post(`${apiBaseUrl}/api/assess`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (event) => {
          if (event.total) {
            const percent = Math.round((event.loaded * 100) / event.total);
            setProgress(percent);
          }
        },
      });
      setResult(response.data);
      setProgress(100);
    } catch (err) {
      const message = err?.response?.data?.error || 'Upload failed. Please try again.';
      setError(message);
      setResult(null);
      setProgress(0);
    } finally {
      setIsLoading(false);
    }
  };

  const summary = useMemo(() => {
    if (!result) return null;
    return [
      { label: 'Overall', value: `${result.overall_score ?? 0}/100` },
      { label: 'Accuracy', value: `${result.accuracy ?? 0}/100` },
      { label: 'Fluency', value: `${result.fluency ?? 0}/100` },
      { label: 'Completeness', value: `${result.completeness ?? 0}/100` },
    ];
  }, [result]);

  return (
    <div className={`min-h-screen transition-colors ${darkMode ? 'bg-slate-950 text-slate-100' : 'bg-slate-100 text-slate-900'}`}>
      <Navbar darkMode={darkMode} onToggle={() => setDarkMode((value) => !value)} />
      <main className="mx-auto flex max-w-7xl flex-col gap-8 px-4 py-8 sm:px-6 lg:px-8">
        <section className={`rounded-3xl border p-6 shadow-xl ${darkMode ? 'border-slate-800 bg-slate-900/90' : 'border-slate-200 bg-white/90'}`}>
          <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
            <div>
              <p className="mb-3 text-sm font-semibold uppercase tracking-[0.4em] text-cyan-400">Livo AI</p>
              <h1 className="text-4xl font-semibold sm:text-5xl">Get a production-style pronunciation assessment in seconds.</h1>
              <p className="mt-4 max-w-2xl text-lg text-slate-300">
                Upload a 30–45 second English recording and receive a score, transcript, and practical coaching suggestions.
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <span className="rounded-full border border-cyan-400/40 bg-cyan-400/10 px-3 py-1 text-sm">WAV • MP3 • M4A</span>
                <span className="rounded-full border border-emerald-400/40 bg-emerald-400/10 px-3 py-1 text-sm">30–45 seconds</span>
                <span className="rounded-full border border-violet-400/40 bg-violet-400/10 px-3 py-1 text-sm">20 MB max</span>
              </div>
            </div>
            <Upload onUpload={handleUpload} isLoading={isLoading} error={error} progress={progress} fileName={fileName} />
          </div>
        </section>

        {isLoading && <Loading />}

        {summary && result && (
          <section className="grid gap-4 md:grid-cols-4">
            {summary.map((item) => (
              <div key={item.label} className={`rounded-2xl border p-4 shadow-lg ${darkMode ? 'border-slate-800 bg-slate-900/90' : 'border-slate-200 bg-white'}`}>
                <p className="text-sm uppercase tracking-[0.25em] text-slate-400">{item.label}</p>
                <p className="mt-2 text-3xl font-semibold">{item.value}</p>
              </div>
            ))}
          </section>
        )}

        {result && <Result result={result} darkMode={darkMode} />}
      </main>
      <Footer darkMode={darkMode} />
    </div>
  );
}

export default App;

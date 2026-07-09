import { useRef, useState } from 'react';

function Upload({ onUpload, isLoading, error, progress, fileName }) {
  const inputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFiles = (files) => {
    const file = files?.[0];
    if (file) {
      onUpload(file);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <div
        onDragOver={(event) => {
          event.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragActive(false);
          handleFiles(event.dataTransfer.files);
        }}
        className={`rounded-3xl border-2 border-dashed p-6 text-center transition ${dragActive ? 'border-cyan-400 bg-cyan-400/10' : 'border-slate-700 bg-slate-800/70'}`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".wav,.mp3,.m4a,audio/wav,audio/mpeg,audio/mp4,audio/x-m4a"
          onChange={(event) => handleFiles(event.target.files)}
          className="hidden"
        />
        <p className="text-lg font-semibold">Drop your recording here</p>
        <p className="mt-2 text-sm text-slate-400">Supported files: WAV, MP3, and M4A</p>
        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          className="mt-4 rounded-full bg-cyan-500 px-5 py-2 font-semibold text-slate-950 transition hover:bg-cyan-400"
          disabled={isLoading}
        >
          {isLoading ? 'Analyzing…' : 'Choose Audio File'}
        </button>
      </div>

      {fileName && <p className="text-sm text-slate-300">Selected file: {fileName}</p>}

      {isLoading && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
          <div className="mb-2 flex items-center justify-between text-sm text-slate-300">
            <span>Uploading and assessing</span>
            <span>{progress}%</span>
          </div>
          <div className="h-2 rounded-full bg-slate-800">
            <div className="h-2 rounded-full bg-gradient-to-r from-cyan-500 to-violet-500 transition-all" style={{ width: `${progress}%` }} />
          </div>
        </div>
      )}

      {error && <p className="rounded-2xl border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-300">{error}</p>}
    </div>
  );
}

export default Upload;

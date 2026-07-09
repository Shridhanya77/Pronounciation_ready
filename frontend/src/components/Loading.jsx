function Loading() {
  return (
    <div className="flex items-center justify-center py-6">
      <div className="flex items-center gap-3 rounded-full border border-cyan-400/30 bg-cyan-400/10 px-4 py-3 text-sm text-cyan-300">
        <span className="h-3 w-3 animate-spin rounded-full border-2 border-cyan-400 border-t-transparent" />
        Processing speech and generating feedback…
      </div>
    </div>
  );
}

export default Loading;

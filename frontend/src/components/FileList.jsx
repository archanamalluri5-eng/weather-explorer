import Spinner from "./Spinner";

function formatSize(bytes) {
  if (bytes == null) return "—";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  return isNaN(d) ? iso : d.toLocaleString();
}

export default function FileList({ files, loading, activeFile, onSelect, onRefresh }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-100">Stored files</h2>
        <button
          onClick={onRefresh}
          disabled={loading}
          className="rounded-lg border border-slate-700 px-3 py-1.5 text-xs font-medium text-slate-300 transition hover:border-sky-500 hover:text-sky-300 disabled:opacity-50"
        >
          {loading ? <Spinner /> : "Refresh"}
        </button>
      </div>

      {loading && files.length === 0 ? (
        <div className="flex items-center gap-2 py-8 text-sm text-slate-400">
          <Spinner /> Loading files…
        </div>
      ) : files.length === 0 ? (
        <p className="py-8 text-center text-sm text-slate-500">
          No files stored yet. Fetch some weather data to get started.
        </p>
      ) : (
        <ul className="max-h-80 divide-y divide-slate-800 overflow-y-auto rounded-lg">
          {files.map((file) => (
            <li key={file.name}>
              <button
                onClick={() => onSelect(file.name)}
                className={`w-full px-3 py-3 text-left transition ${
                  activeFile === file.name
                    ? "bg-sky-500/10"
                    : "hover:bg-slate-800/60"
                }`}
              >
                <span className="block truncate font-mono text-xs text-slate-200">
                  {file.name}
                </span>
                <span className="mt-1 flex flex-wrap gap-x-3 text-[11px] text-slate-500">
                  <span>{formatSize(file.size)}</span>
                  <span>{formatDate(file.created_at)}</span>
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

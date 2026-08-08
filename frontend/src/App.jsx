import { useCallback, useEffect, useState } from "react";
import { getWeatherFileContent, listWeatherFiles } from "./api";
import { extractDailyRows, summarize } from "./weather";
import InputPanel from "./components/InputPanel";
import FileList from "./components/FileList";
import TemperatureChart from "./components/TemperatureChart";
import WeatherTable from "./components/WeatherTable";
import Spinner from "./components/Spinner";

export default function App() {
  const [files, setFiles] = useState([]);
  const [listLoading, setListLoading] = useState(true);
  const [activeFile, setActiveFile] = useState(null);
  const [contentLoading, setContentLoading] = useState(false);
  const [content, setContent] = useState(null);
  const [error, setError] = useState("");

  const refreshFiles = useCallback(async () => {
    setListLoading(true);
    try {
      const result = await listWeatherFiles();
      setFiles(result.files || []);
    } catch (err) {
      setError(`Failed to load file list: ${err.message}`);
    } finally {
      setListLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshFiles();
  }, [refreshFiles]);

  const selectFile = useCallback(
    async (file) => {
      setActiveFile(file);
      setContent(null);
      setError("");
      setContentLoading(true);
      try {
        const result = await getWeatherFileContent(file);
        setContent(result.data);
      } catch (err) {
        setError(`Failed to load ${file}: ${err.message}`);
      } finally {
        setContentLoading(false);
      }
    },
    [],
  );

  const handleStored = async () => {
    await refreshFiles();
  };

  const rows = extractDailyRows(content);
  const summary = summarize(content);

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-800 bg-slate-900/70">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-5">
          <div>
            <h1 className="text-xl font-bold text-slate-100">
              Weather <span className="text-sky-400">Explorer</span>
            </h1>
            <p className="text-sm text-slate-400">
              Historical daily weather from Open-Meteo, stored in the cloud.
            </p>
          </div>
          <span className="rounded-full border border-slate-700 px-3 py-1 text-xs text-slate-400">
            max 31-day range
          </span>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6">
        {error && (
          <div className="mb-4 flex items-start justify-between gap-3 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-300">
            <span>{error}</span>
            <button
              onClick={() => setError("")}
              className="text-red-400 transition hover:text-red-200"
              aria-label="Dismiss error"
            >
              ✕
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Left column: input + file list */}
          <div className="space-y-6 lg:col-span-1">
            <InputPanel onStored={handleStored} onError={setError} />
            <FileList
              files={files}
              loading={listLoading}
              activeFile={activeFile}
              onSelect={selectFile}
              onRefresh={refreshFiles}
            />
          </div>

          {/* Right column: visualization */}
          <div className="space-y-6 lg:col-span-2">
            {contentLoading ? (
              <div className="flex items-center gap-2 rounded-xl border border-slate-800 bg-slate-900/60 p-8 text-sm text-slate-400">
                <Spinner /> Loading file content…
              </div>
            ) : content === null ? (
              <div className="rounded-xl border border-dashed border-slate-800 p-12 text-center text-sm text-slate-500">
                Select a stored file to visualize its daily temperatures.
              </div>
            ) : (
              <>
                <section className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg">
                  <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
                    <div>
                      <h2 className="text-lg font-semibold text-slate-100">
                        Daily temperature
                      </h2>
                      <p className="mt-0.5 font-mono text-xs text-slate-500">
                        {summary.location} · {summary.tz} · {summary.days} days
                      </p>
                    </div>
                    <dl className="flex gap-4 text-center text-xs">
                      <Stat label="Max" value={summary.stats.tempMax} />
                      <Stat label="Min" value={summary.stats.tempMin} />
                    </dl>
                  </div>
                  <TemperatureChart rows={rows} />
                </section>

                <section className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg">
                  <h2 className="mb-4 text-lg font-semibold text-slate-100">
                    Daily variables
                  </h2>
                  <WeatherTable rows={rows} />
                </section>
              </>
            )}
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-600">
        Weather Explorer · Open-Meteo API · object storage · full-stack case study
      </footer>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 px-3 py-2">
      <dt className="text-slate-500">{label}</dt>
      <dd className="mt-0.5 text-base font-semibold text-slate-100">
        {value == null ? "—" : `${Number(value).toFixed(1)}°`}
      </dd>
    </div>
  );
}

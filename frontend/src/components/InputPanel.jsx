import { useState } from "react";
import { storeWeatherData } from "../api";
import Spinner from "./Spinner";

const MAX_RANGE_DAYS = 31;

function daysBetween(start, end) {
  const ms = new Date(end) - new Date(start);
  return Math.round(ms / (1000 * 60 * 60 * 24)) + 1;
}

export default function InputPanel({ onStored, onError }) {
  const [latitude, setLatitude] = useState("51.5074");
  const [longitude, setLongitude] = useState("-0.1278");
  const [startDate, setStartDate] = useState("2024-01-01");
  const [endDate, setEndDate] = useState("2024-01-31");
  const [loading, setLoading] = useState(false);
  const [fieldError, setFieldError] = useState("");
  const [successFile, setSuccessFile] = useState("");

  function validate() {
    const lat = parseFloat(latitude);
    const lon = parseFloat(longitude);
    if (!Number.isFinite(lat) || lat < -90 || lat > 90) {
      return "Latitude must be a number between -90 and 90.";
    }
    if (!Number.isFinite(lon) || lon < -180 || lon > 180) {
      return "Longitude must be a number between -180 and 180.";
    }
    if (!startDate || !endDate) {
      return "Both start and end dates are required.";
    }
    if (new Date(startDate) > new Date(endDate)) {
      return "Start date must be on or before end date.";
    }
    const days = daysBetween(startDate, endDate);
    if (days > MAX_RANGE_DAYS) {
      return `Date range can be at most ${MAX_RANGE_DAYS} days (got ${days}).`;
    }
    return "";
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const problem = validate();
    if (problem) {
      setFieldError(problem);
      return;
    }
    setFieldError("");
    setSuccessFile("");
    setLoading(true);
    try {
      const result = await storeWeatherData({
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        start_date: startDate,
        end_date: endDate,
      });
      setSuccessFile(result.file);
      onStored(result.file);
    } catch (err) {
      onError(`Failed to store weather data: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  const inputClass =
    "w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm " +
    "text-slate-100 placeholder-slate-500 outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30";

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg"
    >
      <h2 className="mb-4 text-lg font-semibold text-slate-100">Fetch &amp; store weather</h2>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="mb-1 block text-xs font-medium text-slate-400">Latitude</span>
          <input
            type="number"
            step="any"
            value={latitude}
            onChange={(e) => setLatitude(e.target.value)}
            placeholder="e.g. 51.5074"
            className={inputClass}
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-xs font-medium text-slate-400">Longitude</span>
          <input
            type="number"
            step="any"
            value={longitude}
            onChange={(e) => setLongitude(e.target.value)}
            placeholder="e.g. -0.1278"
            className={inputClass}
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-xs font-medium text-slate-400">Start date</span>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className={inputClass}
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-xs font-medium text-slate-400">End date</span>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className={inputClass}
          />
        </label>
      </div>

      {fieldError && (
        <p className="mt-3 rounded-lg border border-red-500/40 bg-red-500/10 px-3 py-2 text-sm text-red-300">
          {fieldError}
        </p>
      )}

      <button
        type="submit"
        disabled={loading}
        className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-sky-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? (
          <>
            <Spinner /> Fetching &amp; storing…
          </>
        ) : (
          "Fetch & Store Data"
        )}
      </button>

      {successFile && (
        <p className="mt-3 flex items-start gap-2 rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-300">
          <span aria-hidden>✓</span>
          <span className="break-all">
            Stored <code className="font-mono">{successFile}</code>
          </span>
        </p>
      )}
    </form>
  );
}

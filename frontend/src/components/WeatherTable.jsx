import { useMemo, useState } from "react";

const PAGE_SIZES = [10, 20, 50];

const COLUMNS = [
  { key: "date", label: "Date" },
  { key: "temperature_2m_max", label: "Max (°C)" },
  { key: "temperature_2m_min", label: "Min (°C)" },
  { key: "apparent_temperature_max", label: "Apparent max (°C)" },
  { key: "apparent_temperature_min", label: "Apparent min (°C)" },
];

function fmt(value) {
  return value == null ? "—" : Number(value).toFixed(1);
}

export default function WeatherTable({ rows }) {
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(PAGE_SIZES[0]);

  const totalPages = Math.max(1, Math.ceil(rows.length / pageSize));
  const safePage = Math.min(page, totalPages - 1);

  const pageRows = useMemo(
    () => rows.slice(safePage * pageSize, safePage * pageSize + pageSize),
    [rows, safePage, pageSize],
  );

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <p className="text-sm text-slate-400">
          {rows.length} day{rows.length === 1 ? "" : "s"}
        </p>
        <label className="flex items-center gap-2 text-sm text-slate-400">
          Rows per page
          <select
            value={pageSize}
            onChange={(e) => {
              setPageSize(Number(e.target.value));
              setPage(0);
            }}
            className="rounded-lg border border-slate-700 bg-slate-900 px-2 py-1 text-sm text-slate-200 outline-none focus:border-sky-500"
          >
            {PAGE_SIZES.map((size) => (
              <option key={size} value={size}>
                {size}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="overflow-x-auto rounded-lg border border-slate-800">
        <table className="w-full min-w-[640px] text-left text-sm">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-900/80">
              {COLUMNS.map((col) => (
                <th
                  key={col.key}
                  className="whitespace-nowrap px-3 py-2.5 text-xs font-semibold uppercase tracking-wide text-slate-400"
                >
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {pageRows.map((row) => (
              <tr
                key={row.date}
                className="border-b border-slate-800/60 transition last:border-0 hover:bg-slate-800/40"
              >
                <td className="whitespace-nowrap px-3 py-2 font-mono text-xs text-sky-300">
                  {row.date}
                </td>
                <td className="px-3 py-2 text-slate-200">{fmt(row.temperature_2m_max)}</td>
                <td className="px-3 py-2 text-slate-200">{fmt(row.temperature_2m_min)}</td>
                <td className="px-3 py-2 text-slate-200">{fmt(row.apparent_temperature_max)}</td>
                <td className="px-3 py-2 text-slate-200">{fmt(row.apparent_temperature_min)}</td>
              </tr>
            ))}
            {pageRows.length === 0 && (
              <tr>
                <td colSpan={COLUMNS.length} className="px-3 py-8 text-center text-slate-500">
                  No rows to display.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="mt-3 flex items-center justify-between">
        <span className="text-xs text-slate-500">
          Page {safePage + 1} of {totalPages}
        </span>
        <div className="flex gap-2">
          <button
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={safePage === 0}
            className="rounded-lg border border-slate-700 px-3 py-1.5 text-xs text-slate-300 transition hover:border-sky-500 hover:text-sky-300 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Previous
          </button>
          <button
            onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
            disabled={safePage >= totalPages - 1}
            className="rounded-lg border border-slate-700 px-3 py-1.5 text-xs text-slate-300 transition hover:border-sky-500 hover:text-sky-300 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}

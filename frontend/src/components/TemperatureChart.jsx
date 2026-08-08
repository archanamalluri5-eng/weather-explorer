import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";

const COLORS = {
  temperature_2m_max: "#38bdf8",
  temperature_2m_min: "#818cf8",
  apparent_temperature_max: "#34d399",
  apparent_temperature_min: "#f472b6",
};

const LABELS = {
  temperature_2m_max: "Max temp (°C)",
  temperature_2m_min: "Min temp (°C)",
  apparent_temperature_max: "Apparent max (°C)",
  apparent_temperature_min: "Apparent min (°C)",
};

const SERIES = [
  { key: "temperature_2m_max", color: COLORS.temperature_2m_max },
  { key: "temperature_2m_min", color: COLORS.temperature_2m_min },
  { key: "apparent_temperature_max", color: COLORS.apparent_temperature_max },
  { key: "apparent_temperature_min", color: COLORS.apparent_temperature_min },
];

export default function TemperatureChart({ rows }) {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={rows} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis
            dataKey="date"
            tick={{ fill: "#94a3b8", fontSize: 11 }}
            tickLine={false}
            axisLine={{ stroke: "#334155" }}
            minTickGap={24}
          />
          <YAxis
            tick={{ fill: "#94a3b8", fontSize: 11 }}
            tickLine={false}
            axisLine={{ stroke: "#334155" }}
            width={44}
            unit="°C"
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "#0f172a",
              border: "1px solid #334155",
              borderRadius: 8,
              fontSize: 12,
            }}
            labelStyle={{ color: "#e2e8f0" }}
          />
          <Legend wrapperStyle={{ fontSize: 12 }} />
          {SERIES.map((s) => (
            <Line
              key={s.key}
              type="monotone"
              dataKey={s.key}
              name={LABELS[s.key]}
              stroke={s.color}
              strokeWidth={2}
              dot={false}
              connectNulls
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

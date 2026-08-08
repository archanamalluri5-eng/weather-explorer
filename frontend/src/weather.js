// Helpers to turn a stored Open-Meteo payload into display-ready rows.

export function extractDailyRows(payload) {
  const daily = payload && payload.daily;
  if (!daily || !Array.isArray(daily.time)) {
    return [];
  }
  return daily.time.map((date, i) => ({
    date,
    temperature_2m_max: daily.temperature_2m_max?.[i] ?? null,
    temperature_2m_min: daily.temperature_2m_min?.[i] ?? null,
    apparent_temperature_max: daily.apparent_temperature_max?.[i] ?? null,
    apparent_temperature_min: daily.apparent_temperature_min?.[i] ?? null,
  }));
}

export function summarize(payload) {
  const rows = extractDailyRows(payload);
  const max = (key) =>
    rows.reduce(
      (acc, r) => (r[key] != null && r[key] > acc ? r[key] : acc),
      -Infinity,
    );
  const min = (key) =>
    rows.reduce(
      (acc, r) => (r[key] != null && r[key] < acc ? r[key] : acc),
      Infinity,
    );
  const has = (key) => rows.some((r) => r[key] != null);

  return {
    days: rows.length,
    location: payload
      ? `${payload.latitude?.toFixed?.(4) ?? payload.latitude}, ${payload.longitude?.toFixed?.(4) ?? payload.longitude}`
      : "—",
    tz: payload?.timezone || "—",
    stats: {
      tempMax: has("temperature_2m_max") ? max("temperature_2m_max") : null,
      tempMin: has("temperature_2m_min") ? min("temperature_2m_min") : null,
      appTempMax: has("apparent_temperature_max")
        ? max("apparent_temperature_max")
        : null,
      appTempMin: has("apparent_temperature_min")
        ? min("apparent_temperature_min")
        : null,
    },
  };
}

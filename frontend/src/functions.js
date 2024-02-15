export function isObject(o) {
  return o && typeof o === "object" && !Array.isArray(o);
}

export function isFunction(f) {
  return (
    f &&
    ["[object Function]", "[object AsyncFunction]"].indexOf(
      {}.toString.call(f)
    ) >= 0
  );
}

export function isArray(a) {
  return Array.isArray(a);
}

export function isDate(d) {
  return d != null && d instanceof Date && !isNaN(d.getTime());
}

export function isInteger(n) {
  return Number.isInteger(n);
}

export function isNumeric(n) {
  return (
    ["string", "object"].indexOf(n) < 0 && !isNaN(parseFloat(n)) && isFinite(n)
  );
}

const FORMAT_TYPES = {
  number: {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  },
  int: {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  },
  percent: {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  },
  date: {
    year: "numeric",
    month: "numeric",
    day: "numeric",
  },
  datetime: {
    year: "numeric",
    month: "numeric",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
  },
  year: {
    year: "numeric",
  },
  month: {
    month: "short",
  },
};

export function autoCapitalize(value) {
  const data =
    typeof value === "string"
      ? value
        .toLowerCase()
        .replace(/\w\S*/g, (w) => w.replace(/^\w/, (c) => c.toUpperCase()))
      : value;

  return data;
}

export function format(value, type = "text", locale = "pt-br") {
  switch (type) {
    case "number":
    case "int":
      return isNumeric(value)
        ? Intl.NumberFormat(locale, FORMAT_TYPES[type]).format(value)
        : "";
    case "percent":
      return isNumeric(value)
        ? Intl.NumberFormat(locale, FORMAT_TYPES[type]).format(value * 100) +
        "%"
        : "-";
    case "date":
    case "datetime":
    case "year":
    case "month":
      let date = new Date(Date.parse(value));
      return isDate(date)
        ? Intl.DateTimeFormat(locale, FORMAT_TYPES[type]).format(date)
        : "-";
    case "year_month":
      return (
        format(value, "month", locale) + "/" + format(value, "year", locale)
      );
    case "currency":
      return Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value)
    default: // 'text' or any other type
      return value ? value.toString() : "";
  }
}

export function toLocalISOString(date) {
  return isDate(date)
    ? new Date(date - date.getTimezoneOffset() * 60 * 1000)
      .toISOString()
      .split(".")[0]
    : null;
}

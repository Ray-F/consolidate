const MILLIS_IN_MONTH = 1000 * 60 * 60 * 24 * 30.5;

function toPrettyMonthYear(date: Date) {
  date = new Date(date);

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
  ];

  const month = months[date.getMonth()];

  const year = date.getFullYear();

  return `${month.substring(0, 3)}-${year}`;
}

function toPrettyDayMonthYear(date: Date) {
  date = new Date(date);
  return `${date.getDate()}-${toPrettyMonthYear(date)}`;
}


export {
  MILLIS_IN_MONTH,
  toPrettyDayMonthYear,
  toPrettyMonthYear,
};

function toSeparatedThousands(amount: number, separator: string, withDecimal: boolean = false) {
  return "$" + amount.toFixed(withDecimal ? 2 : 0).replace(/\B(?=(\d{3})+(?!\d))/g, separator);
}

/**
 * Returns only the rounded cents (between 00 and 99) as a pretty string.
 *
 * @param amount
 */
function getCents(amount: number) {
  return Math.round((amount - Math.floor(amount)) * 100).toString().padEnd(2, '0')
}

export {
  toSeparatedThousands,
  getCents
}

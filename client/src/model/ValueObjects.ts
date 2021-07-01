interface Transaction {
  date_created: Date
  amount: number
}

interface Snapshot {
  timestamp: Date
  amount: number
}


export type {
  Transaction,
  Snapshot,
}

import React from 'react';
import { CircularProgress } from '@material-ui/core';
import AccountCard from './AccountCard';
import { gql, useQuery } from '@apollo/client';


const ACCOUNTS = gql`
query {
  accounts {
    id
    name
    expectedBalance
    netContribution
    latestTimestamp
  }
}
`

const AccountsContainer = () => {
  const { loading, error, data } = useQuery(ACCOUNTS)

  return (
    <div>
      {loading ? (<CircularProgress />) : error ? console.log(error) : (
        data.accounts.map((account, index) => (
          <AccountCard key={index} name={account.name} amount={account.expectedBalance} latestTimestamp={account.latestTimestamp} />
        ))
      )}
    </div>
  );
};

export default AccountsContainer;

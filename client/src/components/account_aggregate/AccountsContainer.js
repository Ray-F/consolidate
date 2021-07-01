import React from 'react';
import { CircularProgress, Grid } from '@material-ui/core';
import AccountCard from './AccountCard';
import { gql, useQuery } from '@apollo/client';


const AccountsContainer = ({ userId }) => {

  const ACCOUNTS = gql`
    query {
      getUserById(id: "${userId}") {
        accounts {
          id
          name
          expectedBalance
          netContribution
          latestTimestamp
          accountType
          logoUrl
        }
      }
    }
  `;

  const { loading, error, data } = useQuery(ACCOUNTS);

  return (
    <Grid container spacing={3}>
      {loading ? (<CircularProgress />) : error ? console.log(error) : (
        data?.getUserById.accounts.map((account, index) => (
          <Grid item xs={12} lg={6}>
            <AccountCard key={index}
                         name={account.name}
                         amount={account.expectedBalance}
                         latestTimestamp={account.latestTimestamp}
              // FIXME: Replace this with URL from server
                         logoUrl={account.logoUrl}
                         target={{ timestamp: new Date(2021, 9, 20), amount: 6000 }}
            />
          </Grid>
        ))
      )}
    </Grid>
  );
};

export default AccountsContainer;

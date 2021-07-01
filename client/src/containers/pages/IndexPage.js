import React from 'react';
import { CircularProgress, Container, Grid, Paper, Typography } from '@material-ui/core';

import styled from 'styled-components';
import AccountsContainer from '../../components/account_aggregate/AccountsContainer';
import BalanceGraph from '../../components/graphs/BalanceGraph';
import BalancePie from '../../components/graphs/BalancePie';
import { gql, useQuery } from '@apollo/client';
import AccountCard from '../../components/account_aggregate/AccountCard';
import Page from './Page';


const SGrid = styled(Grid)`
  padding: 20px;
`;

const SPaper = styled(Paper)`
  padding: 20px;
  margin-bottom: 20px;
`;


const ACCOUNTS = gql`
query {
  getUserById(id: "60d04c24edd16a7f2e814202") {
    expectedBalance
    lastUpdateTime
    accounts {
      expectedBalance
      name
    }
  }
}
`;


export default function IndexPage() {

  const { loading, error, data } = useQuery(ACCOUNTS);

  const pieSlices = data?.getUserById.accounts.map((account) => ({
    amount: account.expectedBalance,
    name: account.name,
  })) || [];

  const pieSlices2 = [
    { name: 'Test 1', amount: 10 },
    { name: 'Test 2', amount: 30 },
    { name: 'Test 3', amount: 40 },
    { name: 'Test 4', amount: 50 },
    { name: 'Test 5', amount: 60 },
  ];


  // TODO: Replace with business domain logic
  const assets = 20304;
  const debt = 23045;
  const debtToAssetSlices = [
    { name: 'Debt', amount: debt },
    { name: 'Assets', amount: assets },
  ];

  return (
    <Page>
      <Container maxWidth={'xl'}>

        <SGrid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <AccountsContainer userId={'60d04c24edd16a7f2e814202'} />
          </Grid>
          <Grid item xs={12} sm={6}>
            {
              loading ? <CircularProgress /> : error ? console.log(error) :
                (
                  <AccountCard name={"Net Balance"}
                               amount={data.getUserById.expectedBalance}
                               target={{ amount: 100_000, timestamp: new Date(2021, 12, 3) }}
                               logoUrl={""}
                               latestTimestamp={data.getUserById.lastUpdateTime} />
                )
            }
          </Grid>
          <Grid item xs={12} sm={6}>
            <SPaper>
              <BalanceGraph userId={'60d04c24edd16a7f2e814202'} title={'Balance History'} />
            </SPaper>

          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <SPaper>
              {loading ? <CircularProgress /> : error ? console.log(error) : (
                <BalancePie title={'Distribution over Accounts'} slices={pieSlices} />)}
            </SPaper>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <SPaper>
              <BalancePie title={'Debt to Asset'} slices={debtToAssetSlices} />
            </SPaper>
          </Grid>

          <Grid item xs={12} sm={6}>
            <SPaper>
              <Typography variant={'h5'}>
                Latest snapshots
              </Typography>
            </SPaper>
          </Grid>

        </SGrid>
      </Container>
    </Page>
  );
}

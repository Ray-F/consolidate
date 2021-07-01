import React from 'react';
import { Container, Grid, Paper, Typography } from '@material-ui/core';
import { gql, useQuery } from '@apollo/client';
import { Snapshot, Transaction } from '../../model/ValueObjects';
import { useParams } from 'react-router-dom';
import Navigation from '../../components/Navigation';
import Page from './Page';

interface AccountData {
  getAccountById: {
    name: string,
    creationTime: string,
    transactions: [Transaction]
    goals: [Snapshot]
  }
}

interface Params {
  accountId: string
}

const AccountPage = () => {

  const { accountId } = useParams<Params>();

  const { loading, error, data } = useQuery<AccountData>(gql`
  query {
    getAccountById(id: "${accountId}") {
      name
      creationTime
      transactions {
        dateCreated
        amount
      }
      snapshots {
        timestamp
        amount
      }
    }
  }
  `);

  return (
    <Page>
      <Container>
        <Paper>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant={'h3'}>{data?.getAccountById.name}</Typography>
            </Grid>
          </Grid>
        </Paper>
      </Container>
    </Page>
  );
}

export default AccountPage;

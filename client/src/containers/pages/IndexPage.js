import React from 'react';
import { Container, Grid, Paper, Typography } from '@material-ui/core';

import styled from 'styled-components';
import Navigation from '../../components/Navigation';
import AccountsContainer from '../../components/account_aggregate/AccountsContainer';
import TransactionsContainer from '../../components/account_aggregate/TransactionsContainer';

const SContainer = styled(Container)`
  margin-top: 100px
`;

const SGrid = styled(Grid)`
  padding: 20px;
`;

const SPaper = styled(Paper)`
  padding: 20px;
`;



export default function IndexPage() {

  return (
    <>
      <Navigation />
      <SContainer maxWidth={'xl'}>

        <SGrid container spacing={3}>
          <Grid item xs={12} sm={6} className={'grid-item'}>
            <SPaper>
              <Typography variant={'h5'}>
                Accounts
              </Typography>

              <AccountsContainer />

            </SPaper>
          </Grid>
          <Grid item xs={12} sm={6} className={'grid-item'}>
            <SPaper>
              <Typography variant={'h5'}>
                Latest transactions
              </Typography>

              <TransactionsContainer userId={"60d05277a7fb635c9969165e"} />
            </SPaper>

          </Grid>

          <Grid item xs={12} sm={6} className={'grid-item'}>
            <SPaper>
              <Typography variant={'h5'}>
                Latest snapshots
              </Typography>
            </SPaper>
          </Grid>

        </SGrid>
      </SContainer>
    </>
  );
}

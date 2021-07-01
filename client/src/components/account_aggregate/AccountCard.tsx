import React from 'react';
import { Grid, Paper, Typography } from '@material-ui/core';
import styled from 'styled-components';
import { getCents, toSeparatedThousands } from '../../util/CurrencyUtils';
import { MILLIS_IN_MONTH, toPrettyMonthYear } from '../../util/DateTimeUtils';

const SPaper = styled(Paper)`
  padding: 20px;
`;

const Img = styled.img`
  width: 70px;
  float: right;
  max-width: 100%;
`;

const CentsSpan = styled.span`
  font-size: 0.5em;
`;

const AmountContainer = styled(Grid)`
  padding-top: 20px;
  padding-bottom: 20px;
`;

const TimestampSpan = styled.span`
  font-size: 0.4em;
  margin-left: 20px;
`;

const GoalHint = styled(Typography)`
  color: #aaa;
  font-size: 0.75em;
`;

interface Target {
  amount: number
  timestamp: Date
}

const AccountCard = ({
                       name,
                       amount,
                       latestTimestamp,
                       logoUrl,
                       target,
                     }: { name: string, amount: number, latestTimestamp: Date, logoUrl: string, target: Target }) => {

  const accountBalAsParts = toSeparatedThousands(amount, ' ', true).split('.');

  return (
    <SPaper>
      <Grid container>
        <Grid item xs={8}>
          <Typography variant={'h6'}>
            {name}
          </Typography>
        </Grid>
        <Grid item xs={4}>
          <Img src={logoUrl} />
        </Grid>
        <AmountContainer item xs={12}>
          <Typography variant={'h4'}>
            {accountBalAsParts[0]}.<CentsSpan>{accountBalAsParts[1]}</CentsSpan>
            <TimestampSpan>as of {toPrettyMonthYear(latestTimestamp)}</TimestampSpan>
          </Typography>
        </AmountContainer>
        <Grid item xs={3}>
          <Typography variant={'body2'}>TARGET</Typography>
        </Grid>
        <Grid item xs={9}>
          <Typography>{toSeparatedThousands(Math.round(target.amount - amount), ' ')} in {Math.round((target.timestamp.valueOf() - new Date().valueOf()) / MILLIS_IN_MONTH)} months</Typography>
          <GoalHint>{toSeparatedThousands(Math.floor(target.amount), ' ')} by {toPrettyMonthYear(target.timestamp)}</GoalHint>
        </Grid>
      </Grid>

    </SPaper>
  );
};

export default AccountCard;

import React from 'react';
import { Box, CircularProgress, Typography } from '@material-ui/core';
import { gql, useQuery } from '@apollo/client';
import { FlexibleWidthXYPlot, VerticalBarSeries, XAxis, YAxis } from 'react-vis';
import styled from 'styled-components';
import { toPrettyDayMonthYear } from '../../util/DateTimeUtils';
import { toSeparatedThousands } from '../../util/CurrencyUtils';

const SBox = styled(Box)`
  font-family: "Roboto", sans-serif;
`;

const Title = styled(Typography)`
  margin-bottom: 20px;
`;


const createCumulativeChartData = (transactions = []) => {
  const xyData = [];

  const sortedTransactionsByDate = transactions.sort((a, b) =>
                                                       new Date(a.dateCreated) > new Date(b.dateCreated) ? 1 : -1);


  xyData.push({ x: new Date(sortedTransactionsByDate[0].dateCreated), y: 0 });

  for (let i = 0; i < sortedTransactionsByDate.length; i++) {
    xyData.push({
                  x: new Date(sortedTransactionsByDate[i].dateCreated),
                  y: sortedTransactionsByDate[i].amount + xyData[i].y,
                });
  }

  return xyData;
};


const BalanceGraph = ({ userId, title }) => {

  const TRANSACTIONS_FOR_ID = gql`
    query {
      getUserById(id: "${userId}") {
        accounts {
          transactions {
            dateCreated
            amount
          }
        }
      }
    }
  `;

  const { loading, error, data } = useQuery(TRANSACTIONS_FOR_ID);

  const transactions = data?.getUserById.accounts.flatMap((account) => account.transactions);

  const xyData = data ? createCumulativeChartData(transactions) : [];

  return (
    <SBox>
      <Title variant={'h5'}>{title}</Title>
      {loading ?
        <CircularProgress /> : error ? console.log(error) : (
          <FlexibleWidthXYPlot margin={{ left: 60 }} height={300} xType={'ordinal'}>
            <VerticalBarSeries data={xyData} barWidth={0.8} />
            <XAxis tickFormat={(d) => (toPrettyDayMonthYear(new Date(d)))} />
            <YAxis left={20} tickFormat={(a) => toSeparatedThousands(a, ' ')} />
          </FlexibleWidthXYPlot>
        )
      }
    </SBox>
  );
};

export default BalanceGraph;

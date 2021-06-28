import React from 'react';
import { Box, CircularProgress } from '@material-ui/core';
import { gql, useQuery } from '@apollo/client';
import { ChartLabel, FlexibleWidthXYPlot, VerticalBarSeries, XAxis, YAxis } from 'react-vis';
import styled from 'styled-components';

const SBox = styled(Box)`
  font-family: "Roboto", sans-serif;
`


const createCumulativeChartData = (transactions = []) => {
  const xyData = []

  const sortedTransactionsByDate = transactions.sort((a, b) =>
                                                       new Date(a.dateCreated) > new Date(b.dateCreated) ? 1 : -1)


  xyData.push({ x: new Date(sortedTransactionsByDate[0].dateCreated), y: 0 })

  for (let i = 0; i < sortedTransactionsByDate.length; i++) {
    xyData.push({
                  x: new Date(sortedTransactionsByDate[i].dateCreated),
                  y: sortedTransactionsByDate[i].amount + xyData[i].y
                });
  }

  return xyData
}


const TransactionsContainer = ({ userId }) => {

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

  const transactions = data?.getUserById.accounts.flatMap((account) => account.transactions)

  const xyData = data ? createCumulativeChartData(transactions) : [];

  return (
    <SBox>
      {loading ?
        <CircularProgress /> : error ? console.log(error) : (
          <FlexibleWidthXYPlot height={300} width={600} xType={"ordinal"}>
            <VerticalBarSeries data={xyData} />
            <XAxis tickFormat={(d) => (`${String(new Date(d).getMonth() + 1).padStart(2, '0')}-${new Date(d).getFullYear()}`)} />
            <YAxis left={20} />
          </FlexibleWidthXYPlot>
        )
      }
    </SBox>
  );
};

export default TransactionsContainer;

import React from 'react';
import { Typography } from '@material-ui/core';

const TransactionCard = ({ date, amount }) => {
  return (
    <Typography variant={'body2'}>
      {date} for {amount}
    </Typography>
  );
};

export default TransactionCard;

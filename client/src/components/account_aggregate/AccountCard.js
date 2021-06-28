import React from 'react';
import { Box, Typography } from '@material-ui/core';

const AccountCard = ({ name, amount, latestTimestamp }) => {
  return (
    <Box>
      <Typography variant={'body1'}>
        Account for: {name}
      </Typography>
      <Typography variant={'h6'}>
        ${amount} as of {latestTimestamp}
      </Typography>
    </Box>
  );
};

export default AccountCard;

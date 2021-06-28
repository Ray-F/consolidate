import React from 'react';
import { AppBar, Button, IconButton, Toolbar, Typography } from '@material-ui/core';
import { Menu } from '@material-ui/icons';
import styled from 'styled-components';


const SButton = styled(Button)`
  color: white;
  position: absolute;
  right: 25px;
`;

const Navigation = () => {
  return (
    <div>
      <AppBar position={'fixed'}>
        <Toolbar>
          <IconButton edge={'start'} color={'inherit'}>
            <Menu />
          </IconButton>
          <Typography variant={'h6'}>
            Consolidate
          </Typography>

          <SButton>
            Login
          </SButton>
        </Toolbar>
      </AppBar>
    </div>
  );
};

export default Navigation;

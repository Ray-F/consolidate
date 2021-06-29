import React from 'react';
import { AppBar, Button, IconButton, Toolbar, Typography } from '@material-ui/core';
import { Menu } from '@material-ui/icons';
import styled from 'styled-components';


const SAppBar = styled(AppBar)`
  background-color: #24AEB6;
`

const SButton = styled(Button)`
  color: white;
  position: absolute;
  right: 25px;
`;

const Navigation = () => {
  return (
    <div>
      <SAppBar position={'fixed'}>
        <Toolbar>
          <IconButton edge={'start'} color={'inherit'}>
            <Menu />
          </IconButton>
          <Typography variant={'h6'}>
            Consolidate
          </Typography>

          <SButton onClick={() => window.location = "/api/login"}>
            Login
          </SButton>
        </Toolbar>
      </SAppBar>
    </div>
  );
};

export default Navigation;

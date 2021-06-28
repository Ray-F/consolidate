import React from 'react';
import MainRouter from './MainRouter';
import { StylesProvider } from '@material-ui/core';

import 'normalize.css';
import '../styling/style.scss';
import { ApolloClient, ApolloProvider, InMemoryCache } from '@apollo/client';

const client = new ApolloClient({ uri: '/api/graphql', cache: new InMemoryCache() });


export default function App() {
  return (
    <ApolloProvider client={client}>
      <StylesProvider injectFirst={true}>
        <MainRouter />
      </StylesProvider>
    </ApolloProvider>
  );
}

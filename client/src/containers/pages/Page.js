import React from 'react';
import Navigation from '../../components/Navigation';
import styled from 'styled-components';

const SpacedDiv = styled.div`
  margin-top: 100px
`;

const Page = ({ children }) => {
  return (
    <>
      <Navigation />
      <SpacedDiv>
        {children}
      </SpacedDiv>
    </>
  );
};

export default Page;

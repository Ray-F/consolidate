import React from 'react';
import { DiscreteColorLegend, makeVisFlexible, RadialChart } from 'react-vis';
import { Box, Typography } from '@material-ui/core';
import styled, { css } from 'styled-components';
import { toSeparatedThousands } from '../../util/CurrencyUtils';

interface Slice {
  name: string,
  amount: number,
}

const SBox = styled(Box)`
`;

const FlexibleRadialChart = styled(makeVisFlexible(RadialChart))`
  text {
    fill: white;
    transform: scale(0.8) translate(25px, 20px);
  }
`;

const SLegend = styled(DiscreteColorLegend)`
  span {
    line-height: 2em;
    font-size: 0.9em;
  }
  
  svg {
    margin-right: 5px;
    transform: scaleY(10) translateY(-25%);
  }
`

const BalancePie = ({ title, slices }: { title: string, slices: Slice[] }) => {
  if (slices.length > 4) {
    slices = slices.sort((a, b) => (a.amount > b.amount) ? 1 : -1)

    let totalAmount = 0;
    for (let i = 0; i < slices.length; i++) {
      if (i > 3) {
        totalAmount += slices[i].amount
      }
    }

    slices = [...slices.slice(0, 3), { amount: totalAmount, name: "Other" }]
  }

  const base = [90, 194, 202]

  const different: string[] = [];

  for (let i = 0; i < 4; i++) {
    different.push(`rgb(${base[0] - i * 20}, ${base[1] - i * 30}, ${base[2] - i * 30})`)
  }
  const total = slices.map((slice) => slice.amount).reduce((a, b) => a + b, 0);
  const data = slices.map((slice, index) => {
    return {
      angle: slice.amount / total * 360,
      label: Math.round(slice.amount / total * 100) + '%',
      color: different[index],
      name: `${slice.name} (${toSeparatedThousands(slice.amount, ' ')})`
    };
  });

  const size = 200;

  return (
    <SBox>
      <Typography variant={'h5'}>{title}</Typography>
      <FlexibleRadialChart
        data={data}
        height={size}
        showLabels={true}
        colorType={'literal'}
      />
      <SLegend
        items={data.map((item, index) => ({ title: item.name, color: different[index] }))}

      />
    </SBox>
  );
};

export default BalancePie;

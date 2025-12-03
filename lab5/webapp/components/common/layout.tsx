import { FC } from 'react';
import styled from 'styled-components';


interface Props {
  children: any
}

export type TabOption = {
  name: string
  value: string
}

const Styled = styled.div`

`;

export const mediaQuery = 500;

export const Layout: FC<Props> = ({ children }) => {
  return (
    <Styled>
      <main>
        {children}
      </main>
    </Styled>
  );
};
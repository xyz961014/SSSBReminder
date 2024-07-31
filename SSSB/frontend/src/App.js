import React, { useEffect, useState } from 'react';
import { fetchApartmentAmount } from './Api';
import {
  Container,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';

const App = () => {
  const [amounts, setAmounts] = useState([]);

  useEffect(() => {
    const getAmounts = async () => {
      try {
        const response = await fetchApartmentAmount();
        setAmounts(response.data);
      } catch (err) {
        console.error("Error fetching amounts:", err);
      }
    };
    getAmounts();
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Items List
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell align="right">Amount</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {amounts.map((amount) => (
              <TableRow key={amount.id}>
                <TableCell component="th" scope="row">
                  {amount.id}
                </TableCell>
                <TableCell align="right">{amount.amount}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default App;

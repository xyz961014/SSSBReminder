import React from 'react';
import { HashRouter as Router, Route, Routes } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import HomePage from './pages/HomePage';
import ApartmentPage from './pages/ApartmentPage';

const theme = createTheme({
});

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route exact path="/" element={<HomePage />} />
          <Route path="/apartment" element={<ApartmentPage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;

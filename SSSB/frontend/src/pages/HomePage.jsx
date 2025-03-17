import * as React from 'react';
import { Helmet } from 'react-helmet';
import { useEffect, useState } from 'react';
import { useCallback } from 'react';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import { useLocation } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import MuiDrawer from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';

import Filter from './components/Filter';
import EditFilter from './components/EditFilter';
import Apartments from './components/Apartments';
import { fetchApartmentAmount } from '../Api';


const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    '& .MuiDrawer-paper': {
      position: 'relative',
      whiteSpace: 'nowrap',
      width: drawerWidth,
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
      boxSizing: 'border-box',
      ...(!open && {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing(7),
        [theme.breakpoints.up('sm')]: {
          width: theme.spacing(9),
        },
      }),
    },
  }),
);

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

const HomePage = () => {
  const [open, setOpen] = useState(true);
  const toggleDrawer = () => {
    setOpen(!open);
  };

  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const [filterId, SetFilterId] = useState(searchParams.get("filter_id"));

  const [filterData, setFilterData] = useState({});

  const handleFilterDataChange = useCallback((data) => {
    setFilterData(data);
  }, []);


  return (
    <ThemeProvider theme={defaultTheme}>
      <Helmet>
        <title>SSSB Reminder</title>
      </Helmet>
      <CssBaseline />

      <Grid container>
        <Grid
          item
          xs={12}
        > 
          <AppBar 
            position="absolute"
          >
            <Toolbar
            >
              <Typography
                component="h1"
                variant="h6"
                color="inherit"
                noWrap
                sx={{ flexGrow: 1 }}
              >
                SSSB Reminder
              </Typography>
            </Toolbar>
          </AppBar>
        </Grid> 
        <Grid
          item
          xs={5}
          sm={4}
          sx={{
            display: { xs: 'none', md: 'flex' },
            flexDirection: 'column',
            backgroundColor: 'background.paper',
            borderRight: { sm: 'none', md: '1px solid' },
            borderColor: { sm: 'none', md: 'divider' },
            alignItems: 'start',
            px: 4,
            gap: 4,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Toolbar />
          {filterId ? (
            <EditFilter filterId={filterId} onFilterChange={handleFilterDataChange} />
          ) : (
            <Filter onFilterChange={handleFilterDataChange} />
          )}
        </Grid>
        <Grid
          item
          xs={7}
          sm={8}
          sx={{
            display: { xs: 'none', md: 'flex' },
            flexDirection: 'column',
            alignItems: 'start',
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
        <Box
          component="main"
          sx={{ width: "100%" }}
        >
          <Toolbar />
          <Container sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                  <Apartments filterData={filterData} />
                </Paper>
              </Grid>
            </Grid>
          </Container>
        </Box>
        </Grid>
      </Grid>
    </ThemeProvider>
  );
}

export default HomePage;

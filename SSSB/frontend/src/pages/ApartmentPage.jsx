import React from 'react';
import { useEffect, useState } from 'react';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import { Helmet } from 'react-helmet';
import { useLocation } from 'react-router-dom';

import ApartmentChart from './components/ApartmentChart';
import ApartmentBid from './components/ApartmentBid';
import ApartmentKeyInfo from './components/ApartmentKeyInfo';
import ApartmentInfo from './components/ApartmentInfo';
import ApartmentMap from './components/ApartmentMap';
import PDFViewer from './components/PDFViewer';

import { fetchApartmentInfo, baseURL } from '../Api'

const getApartmentPdfUrl = (objectNumber, drawingType) => {
    return `${baseURL}get_drawing?object_number=${objectNumber}&drawing_type=${drawingType}`;
}

const ApartmentPage = () => {
  const [apartmentInfo, setApartmentInfo] = useState({});

  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const [objectNumber, setObjectNumber] = useState(searchParams.get('object_number'));
  const [validFrom, setValidFrom] = useState(searchParams.get('valid_from'));

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchApartmentInfo(objectNumber, validFrom);
        if (response.data && response.data.length > 0) {
            setApartmentInfo(response.data[0]);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();

  }, [objectNumber, validFrom]);

  return (
    <div>
      <Helmet>
        <title>{apartmentInfo.name}</title>
      </Helmet>
      <Container maxWidth="lg">
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            overflow: 'auto',
          }}
        >
          <Box sx={{ ml: 2 }}>
            <h1>{apartmentInfo.name}</h1>
          </Box>
          <Divider/>
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={8} lg={9}>
                <Paper
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: 280,
                  }}
                >
                  <ApartmentChart object_number={objectNumber} valid_from={validFrom} />
                </Paper>
              </Grid>
              <Grid item xs={12} md={4} lg={3}>
                <Paper
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: 280,
                  }}
                >
                  <ApartmentBid object_number={objectNumber} valid_from={validFrom} />
                </Paper>
              </Grid>
              <Grid item xs={12} md={4} lg={3}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>
                  <ApartmentKeyInfo object_number={objectNumber} valid_from={validFrom} />
                </Paper>
              </Grid>
              <Grid item xs={12} md={8} lg={9}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>
                  <ApartmentInfo object_number={objectNumber} valid_from={validFrom} />
                </Paper>
              </Grid>
              <Grid item xs={12}>
                <Paper sx={{ p: 0, display: 'flex', flexDirection: 'column' }}>
                  <ApartmentMap object_number={objectNumber} valid_from={validFrom} />
                </Paper>
              </Grid>
              <Grid item md={6} xs={12}>
                <Paper sx={{ p: 0, display: 'flex', flexDirection: 'column' }}>
                  <PDFViewer pdfUrl={getApartmentPdfUrl(objectNumber, "APARTMENT")} title="Apartment Drawing" />
                </Paper>
              </Grid>
              <Grid item md={6} xs={12}>
                <Paper sx={{ pt: 0, display: 'flex', flexDirection: 'column' }}>
                  <PDFViewer pdfUrl={getApartmentPdfUrl(objectNumber, "FLOOR")} title="Floor Drawing" />
                </Paper>
              </Grid>
            </Grid>
          </Container>
        </Box>
      </Container>
    </div>
  );
};

export default ApartmentPage;

import * as React from 'react';
import { useEffect, useState } from 'react';
import { useTheme } from '@mui/material/styles';
import { LineChart, axisClasses } from '@mui/x-charts';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import moment from 'moment';

import Title from './Title';

import LoadingBox from './LoadingBox';
import { fetchApartmentInfo } from '../../Api'

export default function ApartmentKeyInfo({ object_number }) {
  const [loading, setLoading] = useState(true);
  const [apartmentInfo, setApartmentInfo] = useState({});

  const showItemValue = (item) => {
      return apartmentInfo[item.field];
  }

  useEffect(() => {

  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetchApartmentInfo(object_number);
        if (response.data && response.data.length > 0) {
            setApartmentInfo(response.data[0]);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();

  }, [object_number]);

  return (
    <React.Fragment>
      <LoadingBox loading={loading}>
        <Box>
          <Title>Rent</Title>
          <Typography component="p" variant="h4">
            {apartmentInfo.monthly_rent} SEK
          </Typography>
        </Box>
        <Box sx={{ mt: 2 }}>
          <Title>Space</Title>
          <Typography component="p" variant="h4">
            {apartmentInfo.living_space} m²
          </Typography>
        </Box>
        <Box sx={{ mt: 2 }}>
          <Title>Type</Title>
          <Typography component="p" variant="h5">
            {apartmentInfo.accommodation_type} 
          </Typography>
        </Box>
      </LoadingBox>
    </React.Fragment>
  );
}

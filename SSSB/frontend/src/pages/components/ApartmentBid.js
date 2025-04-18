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

export default function ApartmentBid({ object_number, valid_from }) {
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
        const response = await fetchApartmentInfo(object_number, valid_from);
        if (response.data && response.data.length > 0) {
            response.data[0].update_time = moment.utc(response.data[0].update_time).local().format('YYYY-MM-DD HH:mm');
            setApartmentInfo(response.data[0]);
            // console.log(apartmentInfo)
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();

  }, [object_number, valid_from]);

  return (
    <React.Fragment>
      <LoadingBox loading={loading}>
        <Box>
          <Title>Credit Required</Title>
          <Typography component="p" variant="h4">
            {apartmentInfo.bid ? apartmentInfo.bid.most_credit : ''} days
          </Typography>
        </Box>
        <Box sx={{ mt: 2 }}>
          <Title>Queue Length</Title>
          <Typography component="p" variant="h4">
            {apartmentInfo.bid ? apartmentInfo.bid.queue_len : ''} 
          </Typography>
        </Box>
        <Typography color="text.secondary" sx={{ flex: 1, mt: 1 }}>
          Last Update {apartmentInfo.update_time}
        </Typography>
        <Box sx={{ mt: 1 }}>
          <Link color="primary" href={apartmentInfo.url} target="_blank" rel="noopener noreferrer">
            Go to SSSB Page
          </Link>
        </Box>
      </LoadingBox>
    </React.Fragment>
  );
}

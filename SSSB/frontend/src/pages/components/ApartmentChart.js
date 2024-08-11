import * as React from 'react';
import { useEffect, useState } from 'react';
import { useTheme } from '@mui/material/styles';
import { LineChart, axisClasses } from '@mui/x-charts';
import moment from 'moment';

import Title from './Title';

import LoadingBox from './LoadingBox';
import { fetchApartmentStatus } from '../../Api'


export default function ApartmentChart({ object_number }) {
  const theme = useTheme();
  const [loading, setLoading] = useState(true);
  const [apartmentStatus, setApartmentStatus] = useState([]);

  useEffect(() => {

  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetchApartmentStatus(object_number);
        if (response.data && response.data.length > 0) {
            response.data.forEach((s) => {
                if (s.update_time) {
                  s["time"] = moment.utc(s.update_time).local().format('MM-DD HH:mm');
                }
            });
            setApartmentStatus(response.data);
        }
        console.log(apartmentStatus);
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
      <Title>Bid History</Title>
      <div style={{ width: '100%', flexGrow: 1, overflow: 'hidden' }}>
        <LineChart
          dataset={apartmentStatus}
          margin={{
            top: 40,
            right: 30,
            left: 40,
            bottom: 30,
          }}
          xAxis={[
            {
              scaleType: 'point',
              dataKey: 'time',
              tickNumber: 2,
              tickLabelStyle: theme.typography.body2,
            },
          ]}
          yAxis={[
            {
              labelStyle: {
                ...theme.typography.body1,
                fill: theme.palette.text.primary,
              },
              tickLabelStyle: theme.typography.body2,
              tickNumber: 2,
              min: 0,
            },
          ]}
          series={[
            {
              dataKey: 'most_credit',
              showMark: false,
              label: "Credit Days"
            },
            {
              dataKey: 'queue_len',
              showMark: false,
              label: "Queue Length"
            },
          ]}
          sx={{
            [`.${axisClasses.root} line`]: { stroke: theme.palette.text.secondary },
            [`.${axisClasses.root} text`]: { fill: theme.palette.text.secondary },
            [`& .${axisClasses.left} .${axisClasses.label}`]: {
              transform: 'translateX(-25px)',
            },
          }}
        />
      </div>
    </React.Fragment>
  );
}

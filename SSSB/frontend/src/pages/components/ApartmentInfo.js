import * as React from 'react';
import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { DataGrid } from '@mui/x-data-grid';
import { Link } from '@mui/material';
import { Box, Chip } from '@mui/material';
import { List, ListItem, ListItemText, Typography } from '@mui/material';
import Grid from '@mui/material/Grid';
import moment from 'moment';

import Title from './Title';
import LoadingBox from './LoadingBox';
import { fetchApartmentInfo } from '../../Api'

const columns = [
  // {
  //   "field": "accommodation_type",
  //   "name": "Accommodation Type",
  // },
  {
    "field": "housing_area",
    "name": "Housing Area",
  },
  {
    "field": "address",
    "name": "Address",
  },
  {
    "field": "floor",
    "name": "Floor",
  },
  {
    "field": "application_ddl",
    "name": "Application DDL",
  },
  {
    "field": "valid_from",
    "name": "Valid From",
  },
  {
    "field": "end_date",
    "name": "End Date",
  },
  {
    "field": "electricity_include",
    "name": "Electricity Include",
  },
  // {
  //   "field": "living_space",
  //   "name": "Living Space",
  // },
  {
    "field": "max_4_years",
    "name": "Max 4 Years",
  },
  // {
  //   "field": "monthly_rent",
  //   "name": "Monthly Rent",
  // },
  {
    "field": "rent_free_june_and_july",
    "name": "Rent Free June and July",
  },
];


export default function ApartmentInfo({ object_number, valid_from }) {
  const [loading, setLoading] = useState(true);
  const [apartmentInfo, setApartmentInfo] = useState({});

  const showItemValue = (item) => {
    var value = apartmentInfo[item.field];
    if (item.field === "application_ddl") {
      value = moment.utc(value).local().format('YYYY-MM-DD HH:mm');
    }
    if ((item.field === "end_date" || item.field === "valid_from") && value != null) {
      value = moment.utc(value).local().format('YYYY-MM-DD');
    }
    if (item.field === "monthly_rent") {
      value = `${value} SEK`;
    }
    if (item.field === "living_space") {
      value = `${value} m²`;
    }
    switch (typeof value) {
      case 'string':
        return value;
      case 'number':
        return value.toString();
      case 'boolean':
        return value ? "Yes": "No";
      case 'object':
        return value == null ? "N/A": "Unsupported value type";
      default:
        return "Unsupported value type";
    }
  }

  useEffect(() => {

  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetchApartmentInfo(object_number, valid_from);
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

  }, [object_number, valid_from]);

  return (
    <React.Fragment>
      <LoadingBox loading={loading} sx={{ width: '100%' }}>
        <Title>Apartment Info</Title>
        <Grid container spacing={2}>
          {columns.map((item, index) => (
            <Grid
              item
              xs={12} md={6} lg={4}
              key={index}
            >
              <ListItem>
                <ListItemText primary={item.name} secondary={showItemValue(item)} />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </LoadingBox>
    </React.Fragment>
  );
}

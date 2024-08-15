import * as React from 'react';
import { useEffect, useState, useCallback } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { DataGrid } from '@mui/x-data-grid';
import { Link } from '@mui/material';
import { Box, Chip } from '@mui/material';
import moment from 'moment';
import _ from 'lodash';

import Title from './Title';

import LoadingBox from './LoadingBox';
import { fetchFilteredApartments } from '../../Api'

const openURL = (url) => {
  window.open(`${url}`, '_blank', 'noopener,noreferrer');
};

const columns = [
  { 
    field: 'name', 
    headerName: 'Address', 
    width: 250,
    renderCell: (params) => (
      <Box>
      <Link href={`/apartment?object_number=${params.row.object_number}`} target="_blank" rel="noopener">
        {params.value}
      </Link>
      <Chip 
        label="SSSB" 
        variant="outlined" 
        size="small"
        onClick={() => openURL(params.row.url)} 
        sx={{ ml: 1, fontSize: '0.6rem', height: '20px' }}
      />
      </Box>
    ),
  },
  { field: 'housing_area', headerName: 'Area', flex: 1 },
  { field: 'accommodation_type', headerName: 'Type', flex: 1 },
  { 
    field: 'living_space', 
    headerName: 'Space', 
    width: 100, 
    valueGetter: (value, row) => `${value} m²`,
    sortComparator: (v1, v2, param1, param2) => {
        const space1 = parseFloat(v1.replace(' m²', ''));
        const space2 = parseFloat(v2.replace(' m²', ''));
        return space1 - space2;
    },
    flex: 1,
  },
  { 
    field: 'monthly_rent', 
    headerName: 'Rent', 
    width: 100, 
    sortComparator: (v1, v2, param1, param2) => {
        const rent1 = parseFloat(v1.replace(' SEK', ''));
        const rent2 = parseFloat(v2.replace(' SEK', ''));
        return rent1 - rent2;
    },
    valueGetter: (value, row) => `${value} SEK`,
    flex: 1,
  },
  {
    field: 'most_credit',
    headerName: 'Credit',
    width: 100,
    valueGetter: (value, row) => row.bid ? row.bid.most_credit : null,
    flex: 1,
  },
  { 
    field: 'application_ddl', 
    headerName: 'DDL', 
    width: 250, 
    valueGetter: (value, row) => row.application_ddl ? moment.utc(row.application_ddl).local().format('MM-DD HH:mm'): null,
    flex: 1,
  },
  { 
    field: 'valid_from', 
    headerName: 'Valid From', 
    width: 250, 
    valueGetter: (value, row) => row.valid_from ? moment.utc(row.valid_from).local().format('YYYY-MM-DD'): null,
    flex: 1,
  },
];

export default function Apartments({ filterData }) {
  const [loading, setLoading] = useState(true);
  const [rows, setRows] = useState([]);


  useEffect(() => {

  }, []);

  const fetchData = useCallback(
    _.debounce(async (filterData) => {
      try {
        setLoading(true);
        const response = await fetchFilteredApartments(filterData);
        setRows(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    }, 500), // 500ms
    []
  );

  useEffect(() => {
    if (!filterData || Object.keys(filterData).length === 0) {
      return;
    }
    // console.log("RUN", filterData);
    fetchData(filterData);

  }, [filterData, fetchData]);

  return (
    <React.Fragment>
      <LoadingBox loading={loading} sx={{ width: '100%' }}>
        <Title>Apartments</Title>
        <DataGrid
          rows={rows}
          columns={columns}
          getRowId={(row) => row._id}
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 10 },
            },
          }}
          pageSizeOptions={[5, 10, 20]}
          disableColumnMenu
        />
      </LoadingBox>
    </React.Fragment>
  );
}

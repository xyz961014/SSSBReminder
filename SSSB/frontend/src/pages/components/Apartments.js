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
    flex: 1,
  },
  { 
    field: 'monthly_rent', 
    headerName: 'Rent', 
    width: 100, 
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
  { field: 'application_ddl', headerName: 'DDL', width: 250, flex: 1 },
  { field: 'valid_from', headerName: 'Valid From', width: 250, flex: 1 },
];

export default function Apartments({ filterData }) {
  const [loading, setLoading] = useState(true);
  const [rows, setRows] = useState([]);

  useEffect(() => {

  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        console.log(filterData);
        const response = await fetchFilteredApartments(filterData);
        setRows(response.data);
        //console.log(rows);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();

  }, [filterData]);

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

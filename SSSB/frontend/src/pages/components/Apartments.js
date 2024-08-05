import * as React from 'react';
import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { DataGrid } from '@mui/x-data-grid';
import { Link } from '@mui/material';
import Title from './Title';

import LoadingBox from './LoadingBox';
import { fetchFilteredApartments } from '../../Api'

const columns = [
  { 
    field: 'name', 
    headerName: 'Name', 
    width: 220,
    renderCell: (params) => (
      <Link href={params.row.url} target="_blank" rel="noopener">
        {params.value}
      </Link>
    ),
  },
  { field: 'accommodation_type', headerName: 'Type', flex: 1 },
  { 
    field: 'living_space', 
    headerName: 'Space', 
    width: 100,
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
  { field: 'application_ddl', headerName: 'DDL', width: 200, flex: 1 },
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
        const response = await fetchFilteredApartments(filterData);
        setRows(response.data);
        // console.log(rows);
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

import React from 'react';
import { Grid, Typography, Paper } from '@mui/material';

const Descriptions = ({ items, column = 3, title }) => {
  const columnWidth = 12 / column;

  return (
    <Paper elevation={1} style={{ padding: 0, overflow: 'hidden' }}>
      {title && (
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
      )}
      <Grid container spacing={0}>
        {items.map((item, index) => (
          <React.Fragment key={index}>
            <Grid
              item
              xs={columnWidth}
              style={{
                backgroundColor: '#f5f5f5',
                padding: '8px 0',
                border: `1px solid #ddd`,
                borderRight: 'none',
                borderBottom: 'none',
              }}
            >
              <Typography variant="subtitle2" color="textSecondary" sx={{ mx: 1 }}>
                {item.label}
              </Typography>
            </Grid>
            <Grid 
              item 
              xs={columnWidth * (column - 1)} 
              style={{
                padding: '8px 0',
                border: `1px solid #ddd`,
                borderBottom: 'none',
              }}
            >
              <Typography variant="body1" sx={{ mx: 1 }}>
                {item.value}
              </Typography>
            </Grid>
          </React.Fragment>
        ))}
      </Grid>
    </Paper>
  );
};

export default Descriptions;

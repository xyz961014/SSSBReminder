import React from 'react';
import { CircularProgress, Box } from '@mui/material';

const LoadingBox = ({ loading, children }) => {
  return (
    <Box sx={{ position: 'relative', width: '100%', height: '100%' }}>
      {loading && (
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            backgroundColor: 'rgba(255, 255, 255, 0.8)', 
            zIndex: 9999,
          }}
        >
          <CircularProgress size={60} />
        </Box>
      )}
      <Box sx={{ opacity: loading ? 0.5 : 1, transition: 'opacity 0.3s' }}>
        {children}
      </Box>
    </Box>
  );
};

export default LoadingBox;

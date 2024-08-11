import * as React from 'react';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Alert from '@mui/material/Alert';

export default function SuccessSnackbar({
  message = "Default message",
  autoHideDuration = 6000,
  open: externalOpen,
  handleClose: externalHandleClose,
}) {
  const [internalOpen, setInternalOpen] = React.useState(false);

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setInternalOpen(false);
    if (externalHandleClose) {
      externalHandleClose(event, reason);
    }
  };

  return (
    <div>
      <Snackbar
        open={externalOpen !== undefined ? externalOpen : internalOpen}
        autoHideDuration={autoHideDuration}
        onClose={handleClose}
        message={message}
        action={
          <IconButton
            size="small"
            aria-label="close"
            color="inherit"
            onClick={handleClose}
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        }
      >
          <Alert
            onClose={handleClose}
            severity="success"
            variant="filled"
            sx={{ width: '100%' }}
          >
            { message }
          </Alert>
      </Snackbar>
    </div>
  );
}

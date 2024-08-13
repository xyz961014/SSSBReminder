import React from 'react';
import { useEffect, useState } from 'react';
import { Viewer } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import { pdfjs } from 'react-pdf';
import { Box } from '@mui/material';
import { Typography } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

import Title from './Title';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const renderToolbar = (Toolbar: (props: ToolbarProps) => ReactElement) => (
    <Toolbar>
        {(slots: ToolbarSlot) => {
            const {
                CurrentPageInput,
                Download,
                EnterFullScreen,
                GoToNextPage,
                GoToPreviousPage,
                NumberOfPages,
                Print,
                ShowSearchPopover,
                Zoom,
                ZoomIn,
                ZoomOut,
                Rotate,
                SwitchSelectionMode,
            } = slots;
            return (
                <div
                    style={{
                        alignItems: 'center',
                        display: 'flex',
                        width: '100%',
                    }}
                >
                    <div style={{ padding: '0px 2px' }}>
                        <ZoomOut />
                    </div>
                    <div style={{ padding: '0px 2px' }}>
                        <Zoom />
                    </div>
                    <div style={{ padding: '0px 2px' }}>
                        <ZoomIn />
                    </div>
                    <div style={{ padding: '0px 2px' }}>
                        <SwitchSelectionMode />
                    </div>
                    <div style={{ padding: '0px 2px', marginLeft: 'auto' }}>
                        <Rotate />
                    </div>
                    <div style={{ padding: '0px 2px' }}>
                        <Download />
                    </div>
                </div>
            );
        }}
    </Toolbar>
);

const PDFViewer = ({ pdfUrl, title }) => {
    const [error, setError] = useState(false);
    const defaultLayoutPluginInstance = defaultLayoutPlugin({
        sidebarTabs: (defaultTabs) => [],
        renderToolbar,
    });

    useEffect(() => {
        const checkPDF = async () => {
            try {
                const response = await fetch(pdfUrl);
                if (!response.ok) {
                    setError(true);
                }
            } catch (err) {
                setError(true);
            }
        };

        if (pdfUrl) {
            checkPDF();
        } else {
            setError(true);
        }
    }, [pdfUrl]);

    return (
        <Box>
        <Box sx={{ pt: 2, pl: 2}}>
            <Title>{title}</Title>
        </Box>
        {!error ? (

            <Viewer
                fileUrl={pdfUrl}
                plugins={[defaultLayoutPluginInstance]}
            />
        ) : (
            <Box 
                display="flex" 
                flexDirection="column" 
                justifyContent="center" 
                alignItems="center" 
                height="100%"
                textAlign="center"
            >
                <Typography color="info" gutterBottom>
                    No PDF
                </Typography>
            </Box>
        )}
        </Box>
    );
};

export default PDFViewer;

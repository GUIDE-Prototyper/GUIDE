import React, { useState } from 'react';
import { Box, Typography, IconButton, Button } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import './FeaturePreview.css';

interface FeaturePreviewProps {
  featureName: string;
  featureDescription: string;
  featureDrawing: string;
  featureNumber: string;
  onBack: () => void;
}

interface Component {
  id: string;
  name: string;
  imageUrl: string;
}

const FeaturePreview: React.FC<FeaturePreviewProps> = ({ featureName, featureDescription, featureNumber, featureDrawing, onBack }) => {
  
  const [components, setComponents] = useState<Component[]>([]);
  const [loadingPreview, setLoadingPreview] = useState(false);
  const [loadingDraw, setLoadingDraw] = useState(false);

  
  const handlePreview = async () => {
    setLoadingPreview(true);
    parent.postMessage({ pluginMessage: { type: 'create-preview-multiple', data: featureDrawing, draw: false, frame: ['Exercise_1'], id: featureNumber} }, '*');
  }
  
  const handleDraw = async () => {
    setLoadingDraw(true);
    parent.postMessage({ pluginMessage: { type: 'create-preview-multiple', data: featureDrawing, draw: true, frame: ['Exercise_1'], id: featureNumber} }, '*');
  }

  const handleMessage = (event: MessageEvent) => {
    const { type, data } = event.data.pluginMessage;
    if (type === 'COMPONENT_PREVIEW_SELECTED') {
      const component = { id: data.id, name: data.name, imageUrl: data.imageUrl };
      setComponents(() => [component]);
      setLoadingPreview(false);
    } else if (type === 'NO_PREVIEW') {
      console.log("no peview");
      setLoadingDraw(false);
    } 

    if (type === 'COMPONENT_DRAWN') {
      setLoadingDraw(false);

    } else if (type === 'NOTHING_DRAWN') {
      console.log("nothing drawn");
      setLoadingDraw(false);
    } 
  };

  window.addEventListener('message', handleMessage, { once: false });

  return (
    <Box className="preview-container">
      <Box className="preview-header">
        <IconButton className="icon-button" onClick={onBack}>
          <ArrowBackIcon />
        </IconButton>
        <Typography variant="h6" component="div">
          {featureName} 
        </Typography>
      </Box>

      <Box className="preview-area">
        <div className="recommendationSquare">
          {components.length === 0 ? (
            <div className="placeholderText">Click "Generate Preview" to see a preview of this feature, or click "Draw Preview" to see this feature in Figma.</div>
          ) : (
            components.map((component, index) => (
              <img key={index} src={component.imageUrl} alt={component.name} className="recComponentImage" />
            ))
          )}
        </div>
      </Box>

      <Box className="button-container-preview">
        <Button className="preview-button" disabled={loadingPreview} onClick={handlePreview} variant="contained">{loadingPreview ? 'Generating...' : 'Generate Preview' }</Button>
        <Button className="preview-button" disabled={loadingDraw} onClick={handleDraw} variant="contained">{loadingDraw ? 'Drawing...' : 'Draw Preview'}</Button>
      </Box>
    </Box>
  );
};

export default FeaturePreview;

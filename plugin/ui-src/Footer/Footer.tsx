import { useContext, useEffect, useState } from 'react';
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import './Footer.css';
import { Feature } from '../../structure/Feature';

interface FooterProps {
  features: Feature[];
  description: string;
  loading: boolean;
}

function Footer({ features, description, loading }: FooterProps) {

  const [internalLoading, setInternalLoading] = useState(false);
  const [allToDraw, setAllToDraw] = useState(0);
  const [buttonDisabledEmpty, setButtonDisabledEmpty] = useState(true);


  useEffect(() => {
    const filteredFeatures = features.filter(
      (feature) => feature.excercise === 'Exercise_1' && feature.deleted === false
    );

    if (filteredFeatures.length > 0) {
      setButtonDisabledEmpty(false);
    } else {
      setButtonDisabledEmpty(true);
    }
  }, [features, 'Exercise_1']); 



  const handleGenerateComponents = async () => {
    setInternalLoading(true); 

    const filteredFeatures = features.filter(
      (feature) => feature.excercise === 'Exercise_1' && feature.deleted === false
    );

    setAllToDraw(filteredFeatures.length);
    for (let i = 0; i < filteredFeatures.length; i++) {
      parent.postMessage({ pluginMessage: { type: 'create-preview-multiple', data: filteredFeatures[i].drawing, draw: true, frame: ['Exercise_1'], id: filteredFeatures[i].number} }, '*');
    }

  };

  const handleMessage = (event: MessageEvent) => {
    const { type, data } = event.data.pluginMessage;
    if (type === 'COMPONENT_DRAWN') {
      setInternalLoading(false);
    } else if (type === 'NOTHING_DRAWN') {
      setInternalLoading(false);
    } 
  };

  window.addEventListener('message', handleMessage, { once: false });

  return (
    <Box className="footer">
      <Button
        variant="contained"
        className="footer-button"
        onClick={handleGenerateComponents}
        disabled={loading || internalLoading || buttonDisabledEmpty} 
      >
        {internalLoading 
          ? `Drawing ${allToDraw} Features...`
          : loading 
          ? 'Please wait...'
          : 'Draw All Features' 
        }
      </Button>
    </Box>
  );
}

export default Footer;

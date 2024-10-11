import { useState } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import { Tabs, Tab, Snackbar, Alert } from '@mui/material';
import { Feature } from '../../structure/Feature';
import FeatureTab from './Feature/FeatureTab';
import config from '../../Config/config';
import DividerElement from "./DividerElement/DividerElement";

import './Content.css';

interface ContentProps {
  features: Feature[];
  setFeatures: React.Dispatch<React.SetStateAction<Feature[]>>;
  description: string;
  setDescription: React.Dispatch<React.SetStateAction<string>>;
  loading: boolean;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

const Content: React.FC<ContentProps> = ({ features, setFeatures, description, setDescription, loading, setLoading }) => {
  const [activeTab, setActiveTab] = useState(0); 
  const [submitDisabled, setSubmitDisabled] = useState(false); 
  const [snackbarOpen, setSnackbarOpen] = useState(false); 
  const [snackbarMessage, setSnackbarMessage] = useState(''); 

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const encodeBase64 = (data: string) => {
    return btoa(data); 
  };

  const handleEditFeature = async (number: number, updatedName: string, updatedDescription: string) => {
     
    setLoading(true);
  
    try {
      const payload = {
        text: description,
        user_stories:[{
          id: String(number), 
          text: updatedDescription,
        }],
      };
  
      const recommendationResponse = await fetch(`${config.serverUrlV1}/recommendation_no_prototype_text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic ' + encodeBase64(config.username + ":" + config.password),
        },
        body: JSON.stringify(payload),
      });
  
      if (!recommendationResponse.ok) {
        throw new Error('Network response was not ok');
      }
  
      const recommendationJsonResponse = await recommendationResponse.json();

      if (recommendationJsonResponse.length > 0) {
        
        const recommendationMap = recommendationJsonResponse.reduce((acc: any, item: any) => {
          const key = `${'Exercise_1'}_${item.number}`;
          acc[key] = item.recommendation; 
          return acc;
        }, {});
    
        setFeatures(prevFeatures =>
          prevFeatures.map(feature =>
            feature.number === number
              ? { ...feature, name: updatedName, description: updatedDescription, edited: true, drawing: recommendationJsonResponse[0].recommendation }
              : feature
          )
        );
      } else {
        setSnackbarMessage("Failed to add manual component");
        setSnackbarOpen(true); 
    }

    } catch (error) {
      console.error("Error while fetching data:", error);
    } finally {
      setLoading(false); 
    }
  }

  const handleAddFeature = async (name: string, descriptionIn: string, deleted: boolean, edited: boolean) => {
    
    setLoading(true); 
  
    const filteredFeatures = features.filter(
      (feature) => feature.excercise === 'Exercise_1'
    );
    const usedNumbers = filteredFeatures.map((feature) => feature.number);
    let nextAvailableNumber = 1;
    while (usedNumbers.includes(nextAvailableNumber)) {
      nextAvailableNumber++;
    }

    try {
       
      const payload = {
        text: description,
        user_stories:[{
          id: String(nextAvailableNumber),
          text: descriptionIn,
        }],
      };
  
      const recommendationResponse = await fetch(`${config.serverUrlV1}/recommendation_no_prototype_text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic ' + encodeBase64(config.username + ":" + config.password),
        },
        body: JSON.stringify(payload),
      });
  
      if (!recommendationResponse.ok) {
        throw new Error('Network response was not ok');
      }
  
      const recommendationJsonResponse = await recommendationResponse.json();
      if (recommendationJsonResponse.length > 0){
        const recommendationMap = recommendationJsonResponse.reduce((acc: any, item: any) => {
          const key = `${'Exercise_1'}_${item.number}`;
          acc[key] = item.recommendation;
          return acc;
        }, {});

        setFeatures(prevFeatures => [
          ...prevFeatures,
          {
              number: nextAvailableNumber, 
              name: name,
              description: descriptionIn,
              deleted: deleted,
              edited: edited,
              drawing: recommendationJsonResponse[0].recommendation,
              dateAdded: new Date(),
              excercise: 'Exercise_1'
          },
        ]);
      } else {
        setSnackbarMessage("Failed to add manual component");
        setSnackbarOpen(true);
      }
    } catch (error) {
      console.error("Error while fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleOnDelete = async (number: number) => {
    setFeatures(prevFeatures => 
      prevFeatures.map(feature =>
        feature.number === number && feature.excercise === 'Exercise_1'
          ? { ...feature, deleted: true }
          : feature
      )
    );
  };

  const handleSnackbarClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackbarOpen(false);
  };


  const handleSubmit = async () => {
    setLoading(true);
    try {
      const callJSON = {
        text: description,
      };
  
      const response = await fetch(`${config.serverUrlV2}/feature_generation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic ' + encodeBase64(config.username + ":" + config.password),
        },
        body: JSON.stringify(callJSON),
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const jsonResponse = await response.json();
      console.log("Server Response", jsonResponse);
  
      const mappedFeatures: Feature[] = jsonResponse.map((item: any) => ({
        number: Number(item.number), 
        name: item.name,
        description: item.description,
        edited: false,
        deleted: false,
        drawing: '',
        dateAdded: new Date(),
        excercise: 'Exercise_1',
      }));
  
      setFeatures(prevFeatures => [...prevFeatures, ...mappedFeatures]);
  
      const payload = {
        text: description,
        user_stories: mappedFeatures.map(({ number, name, description }) => ({
          number: String(number),
          name,
          description,
        })),
      };
  
      const recommendationResponse = await fetch(`${config.serverUrlV1}/recommendation_using_feature_list`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Basic ' + encodeBase64(config.username + ":" + config.password),
        },
        body: JSON.stringify(payload),
      });
  
      if (!recommendationResponse.ok) {
        throw new Error('Network response was not ok');
      }
  
      const recommendationJsonResponse = await recommendationResponse.json();
      console.log("Recommendations", recommendationJsonResponse);

      const recommendationMap = recommendationJsonResponse.reduce((acc: any, item: any) => {
        const key = `${'Exercise_1'}_${item.number}`; 
        acc[key] = item.recommendation;
        return acc;
      }, {});
  
      setFeatures(prevFeatures =>
        prevFeatures.map(feature => {
          const featureKey = `${feature.excercise}_${feature.number}`;
          return {
            ...feature,
            drawing: recommendationMap[featureKey] || feature.drawing,
          };
        })
      );
  
    } catch (error) {
      console.error("Error while fetching data:", error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <Box className="content">
      <DividerElement stepNumber={1} text="Enter App Description And Click Submit" />

      <Box className="textbox-section">
        <textarea
          className="textbox-input"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter your GUI description here..."
        />
        <Button
            variant="contained"
            color="primary"
            onClick={handleSubmit}
            className="submit-button"
            disabled={loading || submitDisabled} 
          >
            {loading
              ? 'Submitting...'
              : submitDisabled
              ? 'Already Submitted'
              : 'Submit'}
        </Button>
      </Box>

      <DividerElement stepNumber={2} text="Screen, Edit Features and Generate Previews" />

      <Box className="lowerContent">
        <Tabs
          classes={{ indicator: 'custom-tab-indicator' }}
          className="custom-tabs"
          value={activeTab}
          onChange={handleTabChange}
          centered
        >
          <Tab className="custom-tab" label="Features" />
        </Tabs>

        {activeTab === 0 && (
          <FeatureTab
            features={features}
            loading={loading} 
            onAdd={(newName, newDescription, b1, b2) => handleAddFeature(newName, newDescription, false, false)}
            onEdit={(number, updatedName, updatedDescription) => handleEditFeature(number, updatedName, updatedDescription)}
            onDelete={(number) => handleOnDelete(number)}
          />
        )}
        
      </Box>

      <Snackbar
            open={snackbarOpen}
            autoHideDuration={4000}
            onClose={handleSnackbarClose}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          >
            <Alert onClose={handleSnackbarClose} severity="error" sx={{ width: '100%' }}>
              {snackbarMessage}
            </Alert>
      </Snackbar>
    </Box>
  );
};

export default Content;
import { useState } from 'react';
import { Box, List, Typography, Dialog, DialogTitle, DialogContent, TextField, DialogActions, Button } from '@mui/material';
import { Feature } from '../../../structure/Feature';
import FeatureObject from './FeatureObject';
import FeaturePreview from './FeaturePreview';

interface FeatureTabProps {
  features: Feature[];
  loading: boolean; 
  onAdd: (name: string, description: string, deleted: boolean, edited: boolean) => void;
  onEdit: (number: number, updatedName: string, updatedDescription: string) => void;
  onDelete: (number: number) => void;
}

const FeatureTab: React.FC<FeatureTabProps> = ({ features, loading, onAdd, onEdit, onDelete }) => {
  
  const [openDialog, setOpenDialog] = useState(false);
  const [newName, setNewName] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [openPreview, setOpenPreview] = useState<Feature | null>(null);

  const handlePreview = (feature: Feature) => {
    setOpenPreview(feature);
  };

  const handleBackFromPreview = () => {
    setOpenPreview(null);
  };

  const handleOpenDialog = () => {
    if (!loading){
      setOpenDialog(true);
    }
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setNewName('');
    setNewDescription('');
  };

  const handleAddFeature = () => {
    if (newName.trim() && newDescription.trim()) {
      onAdd(newName, newDescription, false, false);
      handleCloseDialog();
    } else {
      console.error("Feature name and description cannot be empty");
    }
  };

  return (
    <>
      {openPreview ? (
        <FeaturePreview
          featureName={openPreview.name}
          featureDescription={openPreview.description}
          featureDrawing={openPreview.drawing}
          featureNumber={"" + openPreview.number}
          onBack={handleBackFromPreview}
        />
      ) : (
        <>
          <Box className="middle-section" sx={{ overflowY: 'auto', position: 'relative' }}>
            <List sx={{ width: '100%' }}>
              {features.length > 0 ? (
                features
                  .filter(
                    feature =>
                      !feature.deleted && 
                      feature.excercise === 'Exercise_1' 
                  )
                  .map((feature, index) => (
                    <FeatureObject
                      key={feature.number}
                      feature={feature}
                      index={index}
                      loading={loading}
                      onDelete={onDelete}
                      onEdit={onEdit}
                      onPreview={handlePreview}
                    />
                  ))
              ) : (
                <p>No features available. Please submit a description.</p>
              )}
            </List>
          </Box>

          <Typography
            variant="body2"
            sx={{ textAlign: 'right', marginTop: 0, cursor: 'pointer', color: '#919191', paddingRight: '7px' }}
            onClick={handleOpenDialog}
          >
            Add Feature Manually
          </Typography>

          <Dialog open={openDialog} onClose={handleCloseDialog}>
            <DialogTitle>Add New Feature</DialogTitle>
            <DialogContent>
              <TextField
                autoFocus
                margin="dense"
                label="Feature Name"
                type="text"
                fullWidth
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                error={!newName.trim()}
                helperText={!newName.trim() ? "Feature name cannot be empty" : ""}
              />
              <TextField
                margin="dense"
                label="Feature Description"
                type="text"
                fullWidth
                multiline 
                rows={4}
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
                error={!newDescription.trim()}
                helperText={!newDescription.trim() ? "Feature description cannot be empty" : ""}
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Cancel</Button>
              <Button onClick={handleAddFeature} variant="contained" color="primary">Add Feature</Button>
            </DialogActions>
          </Dialog>
        </>
      )}
    </>
  );
};

export default FeatureTab;

import React, { useState } from 'react';
import { ListItem, ListItemText, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import PreviewIcon from '@mui/icons-material/Preview';
import { Feature } from '../../../structure/Feature';
import '../FeatureDesign.css';

interface FeatureObjectProps {
  feature: Feature;
  onDelete: (number: number) => void;
  onEdit: (number: number, updatedName: string, updatedDescription: string) => void;
  onPreview: (feature: Feature) => void; 
  index: number; 
  loading: boolean;
}

const FeatureObject: React.FC<FeatureObjectProps> = ({ feature, onDelete, onEdit, onPreview, index, loading }) => {
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [editedName, setEditedName] = useState(feature.name);
  const [editedDescription, setEditedDescription] = useState(feature.description);

  const handleEditClick = () => {
    setOpenEditDialog(true);
  };

  const handleCloseEditDialog = () => {
    setOpenEditDialog(false);
  };

  const handleSaveEdit = () => {
    if (editedName.trim() && editedDescription.trim()) {
      onEdit(feature.number, editedName, editedDescription);
      setOpenEditDialog(false);
    } else {
      console.error("Name and Description cannot be empty");
    }
  };

  const handlePreviewClick = () => {
    onPreview(feature);
  };

  return (
    <>
      <ListItem className={`list-item ${index % 2 === 0 ? 'even' : 'odd'}`}>
        <ListItemText 
          primary={feature.name} 
          secondary={feature.description} 
        />
        <IconButton
          className="icon-button"
          edge="end"
          aria-label="preview"
          onClick={handlePreviewClick}
          disabled={loading}
        >
          <PreviewIcon />
        </IconButton>
        <IconButton
          className="icon-button"
          edge="end"
          aria-label="edit"
          onClick={handleEditClick}
          disabled={loading}
        >
          <EditIcon />
        </IconButton>
        <IconButton
          className="icon-button"
          edge="end"
          aria-label="delete"
          onClick={() => onDelete(feature.number)}
          disabled={loading}
        >
          <DeleteIcon />
        </IconButton>
      </ListItem>

      <Dialog open={openEditDialog} onClose={handleCloseEditDialog}>
        <DialogTitle className="dialog-title">Edit Feature</DialogTitle>
        <DialogContent className="dialog-content">
          <TextField
            autoFocus
            margin="dense"
            label="Name"
            type="text"
            fullWidth
            value={editedName}
            onChange={(e) => setEditedName(e.target.value)}
            className="dialog-text-field"
            error={!editedName.trim()}
            helperText={!editedName.trim() ? "Name cannot be empty" : ""}
          />
          <TextField
            margin="dense"
            label="Description"
            type="text"
            fullWidth
            multiline
            rows={5}
            value={editedDescription}
            onChange={(e) => setEditedDescription(e.target.value)}
            className="dialog-text-field"
            error={!editedDescription.trim()}
            helperText={!editedDescription.trim() ? "Description cannot be empty" : ""}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseEditDialog} className="dialog-button">Cancel</Button>
          <Button onClick={handleSaveEdit} variant="contained" color="primary" className="dialog-button">Save</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default FeatureObject;

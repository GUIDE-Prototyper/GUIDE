import AppBar from "@mui/material/AppBar";
import Typography from "@mui/material/Typography";
import './DividerElement.css'; 

interface DividerElementProps {
  stepNumber: number;
  text: string;
}

function DividerElement({ stepNumber, text }: DividerElementProps) {
  return (
    <AppBar position="static" className="divider-base">
      <Typography variant="h6" component="div" className="divider-title">
        {stepNumber}. {text}
      </Typography>
    </AppBar>
  );
}

export default DividerElement;

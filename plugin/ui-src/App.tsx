import { useState } from 'react';
import { Feature } from "../structure/Feature";
import './App.css';
import { Container, CssBaseline, Divider } from '@mui/material';
import Content from './Content/Content';
import Footer from './Footer/Footer';

function App() {

  const [features, setFeatures] = useState<Feature[]>([]);
  const [description, setDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="app-container">
      <CssBaseline />
      <Container maxWidth="sm" className="content-container">
        <Content
          features={features}
          setFeatures={setFeatures}
          description={description}
          setDescription={setDescription}
          loading={isLoading}          
          setLoading={setIsLoading} 
        />
      </Container>
      <Divider/>
      <Footer
        features={features}
        description={description}
        loading={isLoading}
      />
    </div>
  );
}

export default App;

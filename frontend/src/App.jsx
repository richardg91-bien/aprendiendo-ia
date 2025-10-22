import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Typography,
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Fade,
} from '@mui/material';
import {
  Psychology,
  Brightness4,
  Brightness7,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

// Componentes
import ChatInterface from './components/ChatInterface.jsx';
import WebSearchPanel from './components/WebSearchPanel.jsx';
import NeuralTrainingPanel from './components/NeuralTrainingPanel.jsx';
import LearningPanel from './components/LearningPanel.jsx';
import StatusIndicator from './components/StatusIndicator.jsx';

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [serverStatus, setServerStatus] = useState('connecting');

  // Verificar estado del servidor
  useEffect(() => {
    const checkServerStatus = async () => {
      try {
        const response = await fetch('/api/status');
        if (response.ok) {
          setServerStatus('connected');
        } else {
          setServerStatus('error');
        }
      } catch (error) {
        setServerStatus('error');
      }
    };

    checkServerStatus();
    const interval = setInterval(checkServerStatus, 30000); // Verificar cada 30s

    return () => clearInterval(interval);
  }, []);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  return (
    <Box
      component={motion.div}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      sx={{
        minHeight: '100vh',
        background: darkMode
          ? 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)'
          : 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
      }}
    >
      {/* Header */}
      <AppBar 
        position="static" 
        elevation={0}
        sx={{
          backgroundColor: 'rgba(26, 26, 26, 0.8)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        }}
      >
        <Toolbar>
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <Psychology 
              sx={{ 
                mr: 2, 
                fontSize: 32,
                color: '#1976d2',
                filter: 'drop-shadow(0 0 10px #1976d2)',
              }} 
            />
            <Typography 
              variant="h4" 
              component="h1"
              sx={{
                fontWeight: 700,
                background: 'linear-gradient(45deg, #1976d2, #42a5f5)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                textShadow: '0 0 20px rgba(25, 118, 210, 0.3)',
              }}
            >
              ARIA
            </Typography>
            <Typography 
              variant="subtitle1" 
              sx={{ 
                ml: 1, 
                color: 'text.secondary',
                fontWeight: 300,
              }}
            >
              Asistente IA Avanzado
            </Typography>
          </Box>

          <StatusIndicator status={serverStatus} />
          
          <IconButton 
            onClick={toggleTheme} 
            color="inherit"
            sx={{ ml: 1 }}
          >
            {darkMode ? <Brightness7 /> : <Brightness4 />}
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* Contenido Principal */}
      <Container maxWidth="xl" sx={{ py: 3 }}>
        <Grid container spacing={3}>
          {/* Panel de Chat Principal */}
          <Grid item xs={12} md={8}>
            <Fade in={true} timeout={1000}>
              <Box>
                <ChatInterface 
                  serverStatus={serverStatus}
                />
              </Box>
            </Fade>
          </Grid>

          {/* Paneles Laterales */}
          <Grid item xs={12} md={4}>
            <Grid container spacing={2}>
              {/* Búsqueda Web */}
              <Grid item xs={12}>
                <Fade in={true} timeout={1200}>
                  <Box>
                    <WebSearchPanel />
                  </Box>
                </Fade>
              </Grid>

              {/* Entrenamiento Neural */}
              <Grid item xs={12}>
                <Fade in={true} timeout={1400}>
                  <Box>
                    <NeuralTrainingPanel />
                  </Box>
                </Fade>
              </Grid>

              {/* Sistema de Aprendizaje Avanzado */}
              <Grid item xs={12}>
                <Fade in={true} timeout={1600}>
                  <Box>
                    <LearningPanel />
                  </Box>
                </Fade>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;
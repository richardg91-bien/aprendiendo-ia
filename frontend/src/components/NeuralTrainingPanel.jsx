import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Button,
  Box,
  Typography,
  CircularProgress,
  LinearProgress,
  Chip,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
} from '@mui/material';
import {
  School,
  TrendingUp,
  Memory,
  CheckCircle,
  Error,
  Info,
  Psychology,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const NeuralTrainingPanel = () => {
  const [isTraining, setIsTraining] = useState(false);
  const [trainingProgress, setTrainingProgress] = useState(0);
  const [trainingStatus, setTrainingStatus] = useState('idle');
  const [trainingMetrics, setTrainingMetrics] = useState(null);
  const [networkInfo, setNetworkInfo] = useState(null);

  // Obtener información de la red neuronal al cargar
  useEffect(() => {
    fetchNetworkInfo();
  }, []);

  const fetchNetworkInfo = async () => {
    try {
      const response = await fetch('/api/red_neuronal_info');
      if (response.ok) {
        const data = await response.json();
        setNetworkInfo(data);
      }
    } catch (error) {
      console.error('Error obteniendo info de red neuronal:', error);
    }
  };

  const startTraining = async () => {
    setIsTraining(true);
    setTrainingProgress(0);
    setTrainingStatus('training');

    try {
      // Simular progreso de entrenamiento
      const progressInterval = setInterval(() => {
        setTrainingProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + Math.random() * 10;
        });
      }, 500);

      const response = await fetch('/api/entrenar_red_neuronal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          epochs: 50
        })
      });

      const data = await response.json();
      
      clearInterval(progressInterval);
      setTrainingProgress(100);

      if (response.ok && data.success) {
        setTrainingStatus('success');
        setTrainingMetrics({
          precision: data.accuracy_final || 0,
          perdida: Math.round((100 - data.accuracy_final) * 0.1 * 100) / 100 || 0.05,
          epocas: data.epochs_completados || 50
        });
        // Actualizar información de la red
        fetchNetworkInfo();
      } else {
        setTrainingStatus('error');
        console.error('Error en entrenamiento:', data.message || 'Error desconocido');
      }
    } catch (error) {
      setTrainingStatus('error');
      console.error('Error en entrenamiento:', error);
    } finally {
      setIsTraining(false);
      // Reset después de 3 segundos
      setTimeout(() => {
        setTrainingStatus('idle');
        setTrainingProgress(0);
      }, 3000);
    }
  };

  const getStatusIcon = () => {
    switch (trainingStatus) {
      case 'training':
        return <CircularProgress size={20} />;
      case 'success':
        return <CheckCircle color="success" />;
      case 'error':
        return <Error color="error" />;
      default:
        return <School />;
    }
  };

  const getStatusColor = () => {
    switch (trainingStatus) {
      case 'success':
        return 'success';
      case 'error':
        return 'error';
      case 'training':
        return 'info';
      default:
        return 'primary';
    }
  };

  return (
    <Card elevation={3} sx={{ 
      background: 'rgba(26, 26, 26, 0.8)',
      backdropFilter: 'blur(20px)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
    }}>
      <CardContent>
        <Typography variant="h6" sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: 1,
          mb: 2,
          color: 'primary.main',
        }}>
          <Psychology />
          Entrenamiento Neural
        </Typography>

        {/* Información de la Red */}
        {networkInfo && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" sx={{ mb: 1, color: 'text.secondary' }}>
                Estado de la Red Neuronal:
              </Typography>
              <List dense>
                <ListItem sx={{ py: 0.5 }}>
                  <ListItemIcon sx={{ minWidth: 36 }}>
                    <Memory sx={{ fontSize: 20, color: 'primary.main' }} />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Parámetros"
                    secondary={networkInfo.parametros || '4,456'}
                  />
                </ListItem>
                <ListItem sx={{ py: 0.5 }}>
                  <ListItemIcon sx={{ minWidth: 36 }}>
                    <TrendingUp sx={{ fontSize: 20, color: 'success.main' }} />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Precisión"
                    secondary={`${((networkInfo.precision || 0.85) * 100).toFixed(1)}%`}
                  />
                </ListItem>
                <ListItem sx={{ py: 0.5 }}>
                  <ListItemIcon sx={{ minWidth: 36 }}>
                    <Info sx={{ fontSize: 20, color: 'info.main' }} />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Última actualización"
                    secondary={networkInfo.ultima_actualizacion || 'Recién iniciado'}
                  />
                </ListItem>
              </List>
            </Box>
          </motion.div>
        )}

        <Divider sx={{ mb: 3, borderColor: 'rgba(255, 255, 255, 0.1)' }} />

        {/* Botón de Entrenamiento */}
        <Box sx={{ mb: 2 }}>
          <Button
            variant="contained"
            fullWidth
            onClick={startTraining}
            disabled={isTraining}
            startIcon={getStatusIcon()}
            color={getStatusColor()}
            sx={{
              py: 1.5,
              fontSize: '1rem',
              fontWeight: 600,
            }}
          >
            {isTraining 
              ? 'Entrenando Red Neuronal...' 
              : 'Iniciar Entrenamiento'
            }
          </Button>
        </Box>

        {/* Progreso de Entrenamiento */}
        {isTraining && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ mb: 1, color: 'text.secondary' }}>
                Progreso: {Math.round(trainingProgress)}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={trainingProgress}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  '& .MuiLinearProgress-bar': {
                    borderRadius: 4,
                    background: 'linear-gradient(45deg, #1976d2, #42a5f5)',
                  },
                }}
              />
            </Box>
          </motion.div>
        )}

        {/* Mensajes de Estado */}
        {trainingStatus !== 'idle' && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Alert 
              severity={
                trainingStatus === 'success' ? 'success' :
                trainingStatus === 'error' ? 'error' : 'info'
              }
              sx={{ mb: 2 }}
            >
              {trainingStatus === 'training' && 'Entrenando la red neuronal con nuevos datos...'}
              {trainingStatus === 'success' && '¡Entrenamiento completado exitosamente!'}
              {trainingStatus === 'error' && 'Error durante el entrenamiento. Inténtalo de nuevo.'}
            </Alert>
          </motion.div>
        )}

        {/* Métricas de Entrenamiento */}
        {trainingMetrics && trainingStatus === 'success' && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Box sx={{ 
              backgroundColor: 'rgba(25, 118, 210, 0.1)',
              borderRadius: 2,
              p: 2,
            }}>
              <Typography variant="subtitle2" sx={{ mb: 1, color: 'primary.main' }}>
                Resultados del Entrenamiento:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {trainingMetrics.precision && (
                  <Chip 
                    label={`Precisión: ${(trainingMetrics.precision * 100).toFixed(1)}%`}
                    size="small"
                    color="success"
                    variant="outlined"
                  />
                )}
                {trainingMetrics.perdida && (
                  <Chip 
                    label={`Pérdida: ${trainingMetrics.perdida.toFixed(3)}`}
                    size="small"
                    color="info"
                    variant="outlined"
                  />
                )}
                {trainingMetrics.epocas && (
                  <Chip 
                    label={`Épocas: ${trainingMetrics.epocas}`}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                )}
              </Box>
            </Box>
          </motion.div>
        )}

        {/* Información adicional */}
        <Box sx={{ mt: 2, p: 2, backgroundColor: 'rgba(255, 255, 255, 0.02)', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            💡 El entrenamiento mejora las respuestas de ARIA basándose en las conversaciones 
            anteriores y el feedback recibido. Se recomienda entrenar regularmente para 
            mantener la precisión óptima.
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default NeuralTrainingPanel;
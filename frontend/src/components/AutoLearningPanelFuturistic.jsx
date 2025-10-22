import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  LinearProgress,
  Grid,
  Chip,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Avatar,
  Tooltip,
  IconButton,
  Paper
} from '@mui/material';
import {
  Psychology,
  PlayArrow,
  Stop,
  AutoAwesome,
  TrendingUp,
  School,
  Analytics,
  Visibility,
  SmartToy,
  Memory,
  Speed,
  Timeline,
  Refresh
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { styled } from '@mui/material/styles';

// Componentes estilizados futuristas
const FuturisticCard = styled(Card)(({ theme, glowing }) => ({
  background: `linear-gradient(135deg, 
    ${theme.palette.mode === 'dark' ? '#1a1a2e 0%' : '#f8f9fa 0%'}, 
    ${theme.palette.mode === 'dark' ? '#16213e 50%' : '#e9ecef 50%'}, 
    ${theme.palette.mode === 'dark' ? '#0f3460 100%' : '#dee2e6 100%'}
  )`,
  border: `1px solid ${glowing ? '#00ff88' : 'rgba(255,255,255,0.1)'}`,
  boxShadow: glowing 
    ? `0 0 20px rgba(0,255,136,0.3), 0 0 40px rgba(0,255,136,0.1)`
    : `0 8px 32px rgba(0,0,0,0.3)`,
  borderRadius: '16px',
  backdropFilter: 'blur(10px)',
  transition: 'all 0.3s ease',
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '2px',
    background: glowing 
      ? 'linear-gradient(90deg, #00ff88, #00d4ff, #ff00ff, #00ff88)'
      : 'transparent',
    backgroundSize: '200% 100%',
    animation: glowing ? 'aurora 3s linear infinite' : 'none',
  },
  '@keyframes aurora': {
    '0%': { backgroundPosition: '200% 0' },
    '100%': { backgroundPosition: '-200% 0' }
  }
}));

const NeuralButton = styled(Button)(({ theme, variant }) => ({
  background: variant === 'start' 
    ? 'linear-gradient(45deg, #00ff88, #00d4ff)'
    : variant === 'stop'
    ? 'linear-gradient(45deg, #ff4444, #ff8800)'
    : 'linear-gradient(45deg, #6c5ce7, #a29bfe)',
  border: 'none',
  borderRadius: '50px',
  color: 'white',
  fontWeight: 'bold',
  textTransform: 'none',
  padding: '12px 24px',
  fontSize: '14px',
  boxShadow: '0 4px 16px rgba(0,0,0,0.3)',
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: '0 8px 24px rgba(0,0,0,0.4)',
  },
  '&:active': {
    transform: 'translateY(0px)',
  }
}));

const StatusIndicator = styled(Box)(({ status }) => ({
  width: '12px',
  height: '12px',
  borderRadius: '50%',
  background: status === 'running' 
    ? 'linear-gradient(45deg, #00ff88, #00d4ff)'
    : status === 'error'
    ? 'linear-gradient(45deg, #ff4444, #ff8800)'
    : '#666',
  boxShadow: status === 'running' 
    ? '0 0 10px rgba(0,255,136,0.6)' 
    : 'none',
  animation: status === 'running' ? 'pulse 2s infinite' : 'none',
  '@keyframes pulse': {
    '0%': { opacity: 1 },
    '50%': { opacity: 0.5 },
    '100%': { opacity: 1 }
  }
}));

const AutoLearningPanel = () => {
  const [learningStatus, setLearningStatus] = useState({
    is_running: false,
    knowledge_stats: {
      total_knowledge: 0,
      unique_topics: 0,
      avg_confidence: 0
    },
    active_topics: 0,
    last_session: {},
    current_session_active: false
  });
  
  const [loading, setLoading] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [sessionRunning, setSessionRunning] = useState(false);
  const [error, setError] = useState('');
  const [lastUpdate, setLastUpdate] = useState(new Date());

  const fetchLearningStatus = async () => {
    try {
      const response = await fetch('/api/auto_learning/status');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      setLearningStatus(data.status || data); // Extraer el status del objeto respuesta
      setLastUpdate(new Date());
      setError('');
    } catch (error) {
      console.error('Error fetching learning status:', error);
      setError(error.message || 'Error de conexión');
    }
  };

  useEffect(() => {
    fetchLearningStatus();
    const interval = setInterval(fetchLearningStatus, 10000); // Actualizar cada 10 segundos
    return () => clearInterval(interval);
  }, []);

  const handleStartLearning = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/auto_learning/start', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Error al iniciar aprendizaje');
      }
      await fetchLearningStatus();
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStopLearning = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/auto_learning/stop', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Error al detener aprendizaje');
      }
      await fetchLearningStatus();
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickSession = async () => {
    setSessionRunning(true);
    try {
      const response = await fetch('/api/auto_learning/quick_session', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Error en sesión rápida');
      }
      await fetchLearningStatus();
    } catch (error) {
      setError(error.message);
    } finally {
      setSessionRunning(false);
    }
  };

  const handleDeepSession = async () => {
    setSessionRunning(true);
    try {
      const response = await fetch('/api/auto_learning/deep_session', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Error en sesión profunda');
      }
      await fetchLearningStatus();
    } catch (error) {
      setError(error.message);
    } finally {
      setSessionRunning(false);
    }
  };

  return (
    <Box sx={{ padding: 3 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Header Futurista */}
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          mb: 3,
          background: 'linear-gradient(90deg, rgba(108,92,231,0.1), rgba(162,155,254,0.1))',
          borderRadius: '16px',
          padding: 2,
          border: '1px solid rgba(108,92,231,0.2)'
        }}>
          <Avatar sx={{ 
            background: 'linear-gradient(45deg, #6c5ce7, #a29bfe)',
            marginRight: 2,
            width: 48,
            height: 48
          }}>
            <SmartToy />
          </Avatar>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h5" sx={{ 
              fontWeight: 'bold',
              background: 'linear-gradient(45deg, #6c5ce7, #a29bfe)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              color: 'transparent'
            }}>
              🤖 Sistema de Aprendizaje Autónomo ARIA
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <StatusIndicator 
                status={learningStatus.is_running ? 'running' : 'stopped'} 
              />
              <Typography variant="body2" sx={{ ml: 1, color: 'text.secondary' }}>
                {learningStatus.is_running ? '🟢 Activo' : '🔴 Detenido'}
              </Typography>
              <Typography variant="caption" sx={{ ml: 2, color: 'text.secondary' }}>
                Última actualización: {lastUpdate.toLocaleTimeString()}
              </Typography>
            </Box>
          </Box>
          <Tooltip title="Actualizar estado">
            <IconButton onClick={fetchLearningStatus} disabled={loading}>
              <Refresh />
            </IconButton>
          </Tooltip>
        </Box>

        {/* Error Alert */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
            >
              <Alert 
                severity="error" 
                onClose={() => setError('')}
                sx={{ mb: 2 }}
              >
                {error}
              </Alert>
            </motion.div>
          )}
        </AnimatePresence>

        <Grid container spacing={3}>
          {/* Panel de Control Principal */}
          <Grid item xs={12} md={6}>
            <FuturisticCard glowing={learningStatus.is_running}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Psychology sx={{ mr: 1, color: '#6c5ce7' }} />
                  <Typography variant="h6" fontWeight="bold">
                    Control Neuronal
                  </Typography>
                </Box>

                <Box sx={{ mb: 3 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Estado del Sistema Autónomo
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    {!learningStatus.is_running ? (
                      <NeuralButton
                        variant="start"
                        onClick={handleStartLearning}
                        disabled={loading}
                        startIcon={<PlayArrow />}
                      >
                        Activar Aprendizaje
                      </NeuralButton>
                    ) : (
                      <NeuralButton
                        variant="stop"
                        onClick={handleStopLearning}
                        disabled={loading}
                        startIcon={<Stop />}
                      >
                        Detener Sistema
                      </NeuralButton>
                    )}
                  </Box>
                </Box>

                {loading && (
                  <Box sx={{ mt: 2 }}>
                    <LinearProgress 
                      sx={{
                        backgroundColor: 'rgba(108,92,231,0.1)',
                        '& .MuiLinearProgress-bar': {
                          background: 'linear-gradient(90deg, #6c5ce7, #a29bfe)'
                        }
                      }}
                    />
                    <Typography variant="caption" color="text.secondary">
                      Procesando comandos neurales...
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </FuturisticCard>
          </Grid>

          {/* Estadísticas en Tiempo Real */}
          <Grid item xs={12} md={6}>
            <FuturisticCard>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Analytics sx={{ mr: 1, color: '#00ff88' }} />
                  <Typography variant="h6" fontWeight="bold">
                    Métricas Neuronales
                  </Typography>
                </Box>

                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Paper sx={{ 
                      p: 2, 
                      textAlign: 'center',
                      background: 'linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,212,255,0.1))',
                      border: '1px solid rgba(0,255,136,0.2)'
                    }}>
                      <Memory sx={{ color: '#00ff88', mb: 1 }} />
                      <Typography variant="h4" fontWeight="bold" color="#00ff88">
                        {learningStatus.knowledge_stats?.total_knowledge || 0}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Datos Aprendidos
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={6}>
                    <Paper sx={{ 
                      p: 2, 
                      textAlign: 'center',
                      background: 'linear-gradient(135deg, rgba(0,212,255,0.1), rgba(255,0,255,0.1))',
                      border: '1px solid rgba(0,212,255,0.2)'
                    }}>
                      <School sx={{ color: '#00d4ff', mb: 1 }} />
                      <Typography variant="h4" fontWeight="bold" color="#00d4ff">
                        {learningStatus.knowledge_stats?.unique_topics || 0}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Áreas de Conocimiento
                      </Typography>
                    </Paper>
                  </Grid>
                </Grid>

                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Confianza Promedio
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={(learningStatus.knowledge_stats?.avg_confidence || 0) * 100}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: 'rgba(255,255,255,0.1)',
                      '& .MuiLinearProgress-bar': {
                        background: 'linear-gradient(90deg, #ff00ff, #00ff88)'
                      }
                    }}
                  />
                  <Typography variant="caption" color="text.secondary">
                    {((learningStatus.knowledge_stats?.avg_confidence || 0) * 100).toFixed(1)}%
                  </Typography>
                </Box>
              </CardContent>
            </FuturisticCard>
          </Grid>

          {/* Sesiones de Entrenamiento */}
          <Grid item xs={12}>
            <FuturisticCard>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Speed sx={{ mr: 1, color: '#ff00ff' }} />
                  <Typography variant="h6" fontWeight="bold">
                    Sesiones de Entrenamiento Neural
                  </Typography>
                </Box>

                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <NeuralButton
                      fullWidth
                      onClick={handleQuickSession}
                      disabled={sessionRunning || loading}
                      startIcon={<AutoAwesome />}
                    >
                      {sessionRunning ? 'Procesando...' : 'Sesión Rápida (30 min)'}
                    </NeuralButton>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <NeuralButton
                      fullWidth
                      onClick={handleDeepSession}
                      disabled={sessionRunning || loading}
                      startIcon={<Timeline />}
                    >
                      {sessionRunning ? 'Procesando...' : 'Análisis Profundo (2 hrs)'}
                    </NeuralButton>
                  </Grid>
                </Grid>

                {sessionRunning && (
                  <Box sx={{ mt: 2 }}>
                    <LinearProgress 
                      sx={{
                        backgroundColor: 'rgba(255,0,255,0.1)',
                        '& .MuiLinearProgress-bar': {
                          background: 'linear-gradient(90deg, #ff00ff, #00ff88)'
                        }
                      }}
                    />
                    <Typography variant="caption" color="text.secondary">
                      Ejecutando sesión de entrenamiento neuronal...
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </FuturisticCard>
          </Grid>

          {/* Información de la Última Sesión */}
          {learningStatus.last_session && Object.keys(learningStatus.last_session).length > 0 && (
            <Grid item xs={12}>
              <FuturisticCard>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <TrendingUp sx={{ mr: 1, color: '#00d4ff' }} />
                    <Typography variant="h6" fontWeight="bold">
                      Última Sesión Neural
                    </Typography>
                  </Box>

                  <Grid container spacing={2}>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body2" color="text.secondary">
                        Fecha/Hora:
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {learningStatus.last_session.last_session ? 
                          new Date(learningStatus.last_session.last_session).toLocaleString() : 
                          'No disponible'
                        }
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body2" color="text.secondary">
                        Temas Procesados:
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {learningStatus.last_session.topics_learned || 0}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body2" color="text.secondary">
                        Calidad:
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {((learningStatus.last_session.quality || 0) * 100).toFixed(1)}%
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body2" color="text.secondary">
                        Tipo:
                      </Typography>
                      <Chip 
                        label={learningStatus.last_session.type || 'unknown'}
                        size="small"
                        sx={{
                          background: 'linear-gradient(45deg, #6c5ce7, #a29bfe)',
                          color: 'white'
                        }}
                      />
                    </Grid>
                  </Grid>
                </CardContent>
              </FuturisticCard>
            </Grid>
          )}
        </Grid>

        {/* Botón para ver detalles */}
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Button
            onClick={() => setShowDetails(true)}
            startIcon={<Visibility />}
            sx={{
              background: 'linear-gradient(45deg, rgba(108,92,231,0.1), rgba(162,155,254,0.1))',
              border: '1px solid rgba(108,92,231,0.3)',
              borderRadius: '25px'
            }}
          >
            Ver Análisis Detallado
          </Button>
        </Box>
      </motion.div>

      {/* Dialog de detalles */}
      <Dialog
        open={showDetails}
        onClose={() => setShowDetails(false)}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: {
            background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: '16px'
          }
        }}
      >
        <DialogTitle sx={{ 
          background: 'linear-gradient(45deg, #6c5ce7, #a29bfe)',
          color: 'white'
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <SmartToy sx={{ mr: 1 }} />
            Análisis Neural Detallado
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
            Estado del Sistema
          </Typography>
          <Typography>
            • Sistema de aprendizaje: {learningStatus.is_running ? '🟢 Activo' : '🔴 Detenido'}
          </Typography>
          <Typography>
            • Sesión actual: {learningStatus.current_session_active ? '🟡 En progreso' : '⚪ Inactiva'}
          </Typography>
          <Typography>
            • Temas activos: {learningStatus.active_topics}
          </Typography>
          
          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
            Estadísticas de Conocimiento
          </Typography>
          <Typography>
            • Total de datos aprendidos: {learningStatus.knowledge_stats?.total_knowledge || 0}
          </Typography>
          <Typography>
            • Áreas de conocimiento: {learningStatus.knowledge_stats?.unique_topics || 0}
          </Typography>
          <Typography>
            • Confianza promedio: {((learningStatus.knowledge_stats?.avg_confidence || 0) * 100).toFixed(2)}%
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDetails(false)}>
            Cerrar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AutoLearningPanel;
import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Switch,
  FormControlLabel,
  LinearProgress,
  Grid,
  Chip,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import {
  Psychology,
  PlayArrow,
  Stop,
  AutoAwesome,
  TrendingUp,
  School,
  CloudSync,
  Analytics
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const AutoLearningPanel = () => {
  const [learningStatus, setLearningStatus] = useState({
    is_running: false,
    knowledge_stats: {},
    active_topics: 0,
    last_session: {}
  });
  const [loading, setLoading] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [sessionRunning, setSessionRunning] = useState(false);

  const fetchLearningStatus = async () => {
    try {
      const response = await fetch('/api/auto_learning/status');
      const data = await response.json();
      
      if (data.success) {
        setLearningStatus(data.status);
      }
    } catch (error) {
      console.error('Error fetching learning status:', error);
    }
  };

  useEffect(() => {
    fetchLearningStatus();
    const interval = setInterval(fetchLearningStatus, 30000); // Actualizar cada 30 segundos
    return () => clearInterval(interval);
  }, []);

  const toggleAutoLearning = async () => {
    setLoading(true);
    try {
      const endpoint = learningStatus.is_running ? 'stop' : 'start';
      const response = await fetch(`/api/auto_learning/${endpoint}`, {
        method: 'POST',
      });
      
      const data = await response.json();
      
      if (data.success) {
        await fetchLearningStatus();
      } else {
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      console.error('Error toggling auto learning:', error);
      alert('Error al cambiar estado del aprendizaje autónomo');
    } finally {
      setLoading(false);
    }
  };

  const triggerLearningSession = async (type = 'quick') => {
    setSessionRunning(true);
    try {
      const response = await fetch('/api/auto_learning/trigger_session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        alert(`✅ Sesión de aprendizaje ${type} completada`);
        await fetchLearningStatus();
      } else {
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      console.error('Error triggering session:', error);
      alert('Error al ejecutar sesión de aprendizaje');
    } finally {
      setSessionRunning(false);
    }
  };

  const getStatusColor = () => {
    if (learningStatus.is_running) return 'success';
    return 'warning';
  };

  const getKnowledgeProgress = () => {
    const total = learningStatus.knowledge_stats?.total_knowledge || 0;
    const confidence = learningStatus.knowledge_stats?.avg_confidence || 0;
    return (total / 1000) * 100; // Normalizar para mostrar progreso
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card 
        sx={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          mb: 2 
        }}
      >
        <CardContent>
          {/* Header */}
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Psychology sx={{ mr: 1, fontSize: 28 }} />
            <Typography variant="h6">
              🤖 Aprendizaje Autónomo ARIA
            </Typography>
          </Box>

          {/* Estado Actual */}
          <Box sx={{ mb: 3 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={learningStatus.is_running}
                  onChange={toggleAutoLearning}
                  disabled={loading}
                  color="default"
                />
              }
              label={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Typography variant="body1">
                    {learningStatus.is_running ? '🟢 Aprendiendo Activamente' : '🔴 Detenido'}
                  </Typography>
                  {loading && <LinearProgress sx={{ ml: 2, width: 50 }} />}
                </Box>
              }
            />
          </Box>

          {/* Estadísticas Rápidas */}
          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={6} sm={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                  {learningStatus.knowledge_stats?.total_knowledge || 0}
                </Typography>
                <Typography variant="caption">
                  Conocimientos
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                  {learningStatus.knowledge_stats?.unique_topics || 0}
                </Typography>
                <Typography variant="caption">
                  Temas Únicos
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                  {Math.round((learningStatus.knowledge_stats?.avg_confidence || 0) * 100)}%
                </Typography>
                <Typography variant="caption">
                  Confianza
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                  {learningStatus.active_topics || 0}
                </Typography>
                <Typography variant="caption">
                  Temas Activos
                </Typography>
              </Box>
            </Grid>
          </Grid>

          {/* Progreso de Conocimiento */}
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ mb: 1 }}>
              Progreso de Conocimiento
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={Math.min(100, getKnowledgeProgress())}
              sx={{ 
                height: 8, 
                borderRadius: 5,
                bgcolor: 'rgba(255,255,255,0.3)',
                '& .MuiLinearProgress-bar': {
                  bgcolor: '#4caf50'
                }
              }}
            />
            <Typography variant="caption" sx={{ mt: 0.5, display: 'block' }}>
              {learningStatus.knowledge_stats?.total_knowledge || 0} elementos de conocimiento
            </Typography>
          </Box>

          {/* Estado de la Última Sesión */}
          {learningStatus.last_session && Object.keys(learningStatus.last_session).length > 0 && (
            <Alert 
              severity="info" 
              sx={{ 
                mb: 2, 
                bgcolor: 'rgba(255,255,255,0.1)', 
                color: 'white',
                '& .MuiAlert-icon': { color: 'white' }
              }}
            >
              <Typography variant="body2">
                📅 Última sesión: {new Date(learningStatus.last_session.last_session).toLocaleString()}
                <br />
                📚 {learningStatus.last_session.topics_learned} temas aprendidos
                <br />
                ⭐ Calidad: {Math.round((learningStatus.last_session.quality || 0) * 100)}%
              </Typography>
            </Alert>
          )}

          {/* Controles Manuales */}
          <Grid container spacing={1}>
            <Grid item xs={12} sm={4}>
              <Button
                variant="outlined"
                size="small"
                onClick={() => triggerLearningSession('quick')}
                disabled={sessionRunning}
                startIcon={<PlayArrow />}
                sx={{ 
                  color: 'white', 
                  borderColor: 'white',
                  '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
                }}
                fullWidth
              >
                {sessionRunning ? 'Ejecutando...' : 'Sesión Rápida'}
              </Button>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Button
                variant="outlined"
                size="small"
                onClick={() => triggerLearningSession('deep')}
                disabled={sessionRunning}
                startIcon={<School />}
                sx={{ 
                  color: 'white', 
                  borderColor: 'white',
                  '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
                }}
                fullWidth
              >
                {sessionRunning ? 'Ejecutando...' : 'Sesión Profunda'}
              </Button>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Button
                variant="outlined"
                size="small"
                onClick={() => setShowDetails(true)}
                startIcon={<Analytics />}
                sx={{ 
                  color: 'white', 
                  borderColor: 'white',
                  '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
                }}
                fullWidth
              >
                Ver Detalles
              </Button>
            </Grid>
          </Grid>

          {/* Indicadores de Estado */}
          <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Chip
              icon={<CloudSync />}
              label={learningStatus.is_running ? "Conexión Web Activa" : "Web Inactiva"}
              color={learningStatus.is_running ? "success" : "default"}
              size="small"
              variant="outlined"
              sx={{ color: 'white', borderColor: 'white' }}
            />
            <Chip
              icon={<AutoAwesome />}
              label="IA Adaptativa"
              color="primary"
              size="small"
              variant="outlined"
              sx={{ color: 'white', borderColor: 'white' }}
            />
            <Chip
              icon={<TrendingUp />}
              label="Aprendizaje Continuo"
              color="secondary"
              size="small"
              variant="outlined"
              sx={{ color: 'white', borderColor: 'white' }}
            />
          </Box>
        </CardContent>
      </Card>

      {/* Dialog de Detalles */}
      <Dialog open={showDetails} onClose={() => setShowDetails(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Psychology sx={{ mr: 1 }} />
            Detalles del Aprendizaje Autónomo
          </Box>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                📊 Estadísticas de Conocimiento
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemText
                    primary="Total de Conocimientos"
                    secondary={learningStatus.knowledge_stats?.total_knowledge || 0}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Temas Únicos"
                    secondary={learningStatus.knowledge_stats?.unique_topics || 0}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Confianza Promedio"
                    secondary={`${Math.round((learningStatus.knowledge_stats?.avg_confidence || 0) * 100)}%`}
                  />
                </ListItem>
              </List>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                🎯 Configuración Actual
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemText
                    primary="Estado del Sistema"
                    secondary={learningStatus.is_running ? "🟢 Activo" : "🔴 Inactivo"}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Temas Activos"
                    secondary={learningStatus.active_topics || 0}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Modo de Operación"
                    secondary="Aprendizaje Autónomo Programado"
                  />
                </ListItem>
              </List>
            </Grid>
          </Grid>
          
          <Divider sx={{ my: 2 }} />
          
          <Typography variant="body2" color="text.secondary">
            💡 <strong>Funcionamiento:</strong> El sistema de aprendizaje autónomo ejecuta sesiones 
            programadas cada 30 minutos (sesiones rápidas) y cada 2 horas (sesiones profundas). 
            Durante estas sesiones, ARIA busca información actualizada en internet sobre temas 
            relevantes y la incorpora a su base de conocimientos.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDetails(false)}>Cerrar</Button>
        </DialogActions>
      </Dialog>
    </motion.div>
  );
};

export default AutoLearningPanel;
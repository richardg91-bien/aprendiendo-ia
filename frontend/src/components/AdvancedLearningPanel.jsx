import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Switch,
  FormControlLabel,
  Chip,
  Grid,
  Alert,
  AlertTitle,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Paper,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Psychology as BrainIcon,
  CloudDownload as CloudIcon,
  Science as ScienceIcon,
  Public as WebIcon,
  Search as SearchIcon,
  TrendingUp as TrendingIcon,
  VerifiedUser as VerifiedIcon,
  AutoAwesome as AdvancedIcon,
  ExpandMore as ExpandIcon,
  Computer as BasicIcon,
  CompareArrows as CompareIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

const AdvancedLearningPanel = () => {
  const [learningStatus, setLearningStatus] = useState(null);
  const [capabilities, setCapabilities] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [isAdvancedActive, setIsAdvancedActive] = useState(false);
  const [searchDialog, setSearchDialog] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    fetchLearningStatus();
    fetchCapabilities();
    fetchComparison();
    
    const interval = setInterval(fetchLearningStatus, 5000);
    return () => clearInterval(interval);
  }, []);
  
  const fetchLearningStatus = async () => {
    try {
      const response = await fetch('/api/auto_learning/status');
      const data = await response.json();
      
      if (data.success) {
        setLearningStatus(data.status);
        setIsAdvancedActive(data.status.system_type === 'advanced');
      }
    } catch (error) {
      console.error('Error fetching learning status:', error);
    }
  };
  
  const fetchCapabilities = async () => {
    try {
      const response = await fetch('/api/advanced_learning/capabilities');
      const data = await response.json();
      setCapabilities(data);
    } catch (error) {
      console.error('Error fetching capabilities:', error);
    }
  };
  
  const fetchComparison = async () => {
    try {
      const response = await fetch('/api/learning/compare_systems');
      const data = await response.json();
      setComparison(data);
    } catch (error) {
      console.error('Error fetching comparison:', error);
    }
  };
  
  const handleStartLearning = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/auto_learning/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      
      if (data.success) {
        setIsAdvancedActive(data.system === 'advanced');
        fetchLearningStatus();
      }
    } catch (error) {
      console.error('Error starting learning:', error);
    }
    setLoading(false);
  };
  
  const handleStopLearning = async () => {
    setLoading(true);
    try {
      await fetch('/api/auto_learning/stop', { method: 'POST' });
      setIsAdvancedActive(false);
      fetchLearningStatus();
    } catch (error) {
      console.error('Error stopping learning:', error);
    }
    setLoading(false);
  };
  
  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/advanced_learning/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery, limit: 10 })
      });
      const data = await response.json();
      
      if (data.success) {
        setSearchResults(data.results);
      }
    } catch (error) {
      console.error('Error searching knowledge:', error);
    }
    setLoading(false);
  };
  
  const getSystemStatusColor = () => {
    if (!learningStatus) return 'default';
    if (learningStatus.system_type === 'advanced') return 'success';
    return 'warning';
  };
  
  const getSystemStatusText = () => {
    if (!learningStatus) return 'No Disponible';
    if (learningStatus.system_type === 'advanced') return 'Sistema Avanzado Activo';
    return 'Sistema Básico Activo';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <Card
        sx={{
          background: 'linear-gradient(145deg, rgba(16, 20, 31, 0.95), rgba(30, 41, 59, 0.9))',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(100, 255, 218, 0.3)',
          borderRadius: 3,
          boxShadow: '0 8px 32px rgba(0, 255, 127, 0.15)',
          mb: 3
        }}
      >
        <CardContent>
          <Typography
            variant="h5"
            sx={{
              background: 'linear-gradient(45deg, #00FF7F, #00BFFF)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 2,
              display: 'flex',
              alignItems: 'center',
              gap: 1
            }}
          >
            <AdvancedIcon />
            Sistema de Aprendizaje Mejorado
          </Typography>
          
          {/* Estado Actual */}
          <Alert 
            severity={getSystemStatusColor()} 
            sx={{ mb: 2 }}
            icon={isAdvancedActive ? <AdvancedIcon /> : <BasicIcon />}
          >
            <AlertTitle>{getSystemStatusText()}</AlertTitle>
            {learningStatus && (
              <>
                <Typography variant="body2">
                  Conocimiento Total: {learningStatus.total_knowledge || 0} elementos
                </Typography>
                {learningStatus.avg_confidence && (
                  <Typography variant="body2">
                    Confianza Promedio: {(learningStatus.avg_confidence * 100).toFixed(1)}%
                  </Typography>
                )}
              </>
            )}
          </Alert>
          
          {/* Controles */}
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} md={6}>
              <Button
                variant="contained"
                onClick={isAdvancedActive ? handleStopLearning : handleStartLearning}
                disabled={loading}
                fullWidth
                sx={{
                  background: isAdvancedActive 
                    ? 'linear-gradient(45deg, #FF6B6B, #FF8E8E)'
                    : 'linear-gradient(45deg, #00FF7F, #00BFFF)',
                  color: 'white',
                  '&:hover': {
                    background: isAdvancedActive 
                      ? 'linear-gradient(45deg, #FF5252, #FF7979)'
                      : 'linear-gradient(45deg, #00E676, #2196F3)',
                  }
                }}
              >
                {loading ? (
                  <LinearProgress sx={{ width: '100%' }} />
                ) : isAdvancedActive ? (
                  '🛑 Detener Aprendizaje'
                ) : (
                  '🚀 Iniciar Aprendizaje Avanzado'
                )}
              </Button>
            </Grid>
            <Grid item xs={12} md={6}>
              <Button
                variant="outlined"
                onClick={() => setSearchDialog(true)}
                fullWidth
                startIcon={<SearchIcon />}
                sx={{
                  borderColor: '#00FF7F',
                  color: '#00FF7F',
                  '&:hover': {
                    borderColor: '#00BFFF',
                    backgroundColor: 'rgba(0, 255, 127, 0.1)'
                  }
                }}
              >
                Buscar Conocimiento
              </Button>
            </Grid>
          </Grid>
          
          {/* Capacidades del Sistema Avanzado */}
          {capabilities && capabilities.available && (
            <Accordion sx={{ mb: 2, backgroundColor: 'rgba(0, 255, 127, 0.05)' }}>
              <AccordionSummary expandIcon={<ExpandIcon sx={{ color: '#00FF7F' }} />}>
                <Typography sx={{ color: '#00FF7F', fontWeight: 'bold' }}>
                  ✨ Capacidades Avanzadas Disponibles
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  {Object.entries(capabilities.features).map(([key, available]) => (
                    <Grid item xs={12} sm={6} key={key}>
                      <Chip
                        label={key.replace(/_/g, ' ').toUpperCase()}
                        color={available ? 'success' : 'default'}
                        icon={available ? <VerifiedIcon /> : undefined}
                        variant={available ? 'filled' : 'outlined'}
                      />
                    </Grid>
                  ))}
                </Grid>
                
                <Typography variant="h6" sx={{ mt: 2, mb: 1, color: '#00BFFF' }}>
                  Fuentes de Conocimiento:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {capabilities.sources.map((source, index) => (
                    <Chip
                      key={index}
                      label={source}
                      size="small"
                      sx={{ 
                        backgroundColor: 'rgba(0, 191, 255, 0.2)',
                        color: '#00BFFF'
                      }}
                    />
                  ))}
                </Box>
              </AccordionDetails>
            </Accordion>
          )}
          
          {/* Comparación de Sistemas */}
          {comparison && (
            <Accordion sx={{ backgroundColor: 'rgba(0, 191, 255, 0.05)' }}>
              <AccordionSummary expandIcon={<ExpandIcon sx={{ color: '#00BFFF' }} />}>
                <Typography sx={{ color: '#00BFFF', fontWeight: 'bold' }}>
                  <CompareIcon sx={{ mr: 1 }} />
                  Comparación: Sistema Básico vs Avanzado
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, backgroundColor: 'rgba(255, 193, 7, 0.1)' }}>
                      <Typography variant="h6" sx={{ color: '#FFC107', mb: 1 }}>
                        🔧 Sistema Básico
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        Disponible: {comparison.basic_system.available ? '✅' : '❌'}
                      </Typography>
                      <Typography variant="subtitle2" sx={{ color: '#FFC107' }}>
                        Características:
                      </Typography>
                      <List dense>
                        {Object.entries(comparison.basic_system.features).map(([key, value]) => (
                          <ListItem key={key} sx={{ py: 0 }}>
                            <ListItemText
                              primary={key.replace(/_/g, ' ')}
                              secondary={value ? '✅ Sí' : '❌ No'}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Paper>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, backgroundColor: 'rgba(0, 255, 127, 0.1)' }}>
                      <Typography variant="h6" sx={{ color: '#00FF7F', mb: 1 }}>
                        🚀 Sistema Avanzado
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        Disponible: {comparison.advanced_system.available ? '✅' : '❌'}
                      </Typography>
                      <Typography variant="subtitle2" sx={{ color: '#00FF7F' }}>
                        Características:
                      </Typography>
                      <List dense>
                        {Object.entries(comparison.advanced_system.features).map(([key, value]) => (
                          <ListItem key={key} sx={{ py: 0 }}>
                            <ListItemText
                              primary={key.replace(/_/g, ' ')}
                              secondary={value ? '✅ Sí' : '❌ No'}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Paper>
                  </Grid>
                </Grid>
                
                <Alert severity="info" sx={{ mt: 2 }}>
                  <AlertTitle>Sistema Recomendado</AlertTitle>
                  Se recomienda usar el sistema <strong>{comparison.recommendation}</strong> 
                  {comparison.recommendation === 'advanced' 
                    ? ' por sus capacidades superiores de acceso a información en tiempo real.'
                    : ' como alternativa estable sin dependencias externas.'
                  }
                </Alert>
              </AccordionDetails>
            </Accordion>
          )}
          
          {/* Estadísticas en Tiempo Real */}
          {learningStatus && learningStatus.system_type === 'advanced' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <Typography variant="h6" sx={{ mt: 2, mb: 1, color: '#00FF7F' }}>
                📊 Estadísticas en Tiempo Real
              </Typography>
              <Grid container spacing={2}>
                {learningStatus.statistics && (
                  <>
                    <Grid item xs={6} sm={3}>
                      <Paper sx={{ p: 1, textAlign: 'center', backgroundColor: 'rgba(0, 255, 127, 0.1)' }}>
                        <Typography variant="h6" sx={{ color: '#00FF7F' }}>
                          {learningStatus.statistics.sources_accessed || 0}
                        </Typography>
                        <Typography variant="caption">Fuentes Accedidas</Typography>
                      </Paper>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                      <Paper sx={{ p: 1, textAlign: 'center', backgroundColor: 'rgba(0, 191, 255, 0.1)' }}>
                        <Typography variant="h6" sx={{ color: '#00BFFF' }}>
                          {learningStatus.statistics.articles_processed || 0}
                        </Typography>
                        <Typography variant="caption">Artículos Procesados</Typography>
                      </Paper>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                      <Paper sx={{ p: 1, textAlign: 'center', backgroundColor: 'rgba(255, 193, 7, 0.1)' }}>
                        <Typography variant="h6" sx={{ color: '#FFC107' }}>
                          {learningStatus.statistics.successful_extractions || 0}
                        </Typography>
                        <Typography variant="caption">Extracciones Exitosas</Typography>
                      </Paper>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                      <Paper sx={{ p: 1, textAlign: 'center', backgroundColor: 'rgba(255, 87, 34, 0.1)' }}>
                        <Typography variant="h6" sx={{ color: '#FF5722' }}>
                          {learningStatus.statistics.failed_extractions || 0}
                        </Typography>
                        <Typography variant="caption">Extracciones Fallidas</Typography>
                      </Paper>
                    </Grid>
                  </>
                )}
              </Grid>
            </motion.div>
          )}
        </CardContent>
      </Card>
      
      {/* Dialog de Búsqueda */}
      <Dialog
        open={searchDialog}
        onClose={() => setSearchDialog(false)}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: {
            background: 'linear-gradient(145deg, rgba(16, 20, 31, 0.95), rgba(30, 41, 59, 0.9))',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(100, 255, 218, 0.3)'
          }
        }}
      >
        <DialogTitle sx={{ color: '#00FF7F' }}>
          🔍 Buscar en Base de Conocimiento Avanzada
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Consulta de búsqueda"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            margin="normal"
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            sx={{
              '& .MuiOutlinedInput-root': {
                '& fieldset': { borderColor: '#00FF7F' },
                '&:hover fieldset': { borderColor: '#00BFFF' },
                '&.Mui-focused fieldset': { borderColor: '#00BFFF' }
              },
              '& .MuiInputLabel-root': { color: '#00FF7F' }
            }}
          />
          
          {searchResults.length > 0 && (
            <List sx={{ mt: 2 }}>
              {searchResults.map((result, index) => (
                <ListItem key={index} divider>
                  <ListItemText
                    primary={
                      <Typography sx={{ color: '#00BFFF', fontWeight: 'bold' }}>
                        {result.title}
                      </Typography>
                    }
                    secondary={
                      <>
                        <Typography variant="body2" sx={{ color: '#E0E0E0', mb: 1 }}>
                          {result.content}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                          <Chip size="small" label={result.source_name} color="primary" />
                          <Chip size="small" label={`${(result.confidence_score * 100).toFixed(0)}% confianza`} />
                          <Chip size="small" label={result.topic} variant="outlined" />
                        </Box>
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSearchDialog(false)} sx={{ color: '#FF5722' }}>
            Cerrar
          </Button>
          <Button onClick={handleSearch} disabled={loading} sx={{ color: '#00FF7F' }}>
            {loading ? 'Buscando...' : 'Buscar'}
          </Button>
        </DialogActions>
      </Dialog>
    </motion.div>
  );
};

export default AdvancedLearningPanel;
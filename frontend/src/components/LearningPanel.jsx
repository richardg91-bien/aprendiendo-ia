import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Grid,
  Chip,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  Divider,
  IconButton,
  Alert
} from '@mui/material';
import {
  Psychology,
  School,
  Feedback,
  Download,
  AutoStories,
  TrendingUp,
  Memory,
  Analytics
} from '@mui/icons-material';

function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export default function LearningPanel() {
  const [tabValue, setTabValue] = useState(0);
  const [learningStats, setLearningStats] = useState({});
  const [teachingDialog, setTeachingDialog] = useState(false);
  const [exportDialog, setExportDialog] = useState(false);
  const [teachData, setTeachData] = useState({ concept: '', definition: '' });
  const [exportedKnowledge, setExportedKnowledge] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchLearningStats();
    const interval = setInterval(fetchLearningStats, 10000); // Actualizar cada 10 segundos
    return () => clearInterval(interval);
  }, []);

  const fetchLearningStats = async () => {
    try {
      const response = await fetch('/api/learning/stats');
      const data = await response.json();
      if (data.success) {
        setLearningStats(data.stats);
      }
    } catch (error) {
      console.error('Error fetching learning stats:', error);
    }
  };

  const handleTeach = async () => {
    if (!teachData.concept.trim() || !teachData.definition.trim()) {
      setMessage('Se requieren concepto y definición');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/learning/teach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(teachData)
      });
      
      const data = await response.json();
      setMessage(data.message);
      
      if (data.success) {
        setTeachData({ concept: '', definition: '' });
        setTeachingDialog(false);
        fetchLearningStats();
      }
    } catch (error) {
      setMessage('Error enseñando conocimiento');
    }
    setLoading(false);
  };

  const handleExport = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/learning/export');
      const data = await response.json();
      
      if (data.success) {
        setExportedKnowledge(data.knowledge);
        setExportDialog(true);
      } else {
        setMessage(data.message);
      }
    } catch (error) {
      setMessage('Error exportando conocimiento');
    }
    setLoading(false);
  };

  const downloadKnowledge = () => {
    if (!exportedKnowledge) return;
    
    const blob = new Blob([JSON.stringify(exportedKnowledge, null, 2)], 
                         { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `aria-knowledge-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Box>
      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Psychology color="primary" sx={{ mr: 1 }} />
            <Typography variant="h5" component="h2">
              Sistema de Aprendizaje Avanzado
            </Typography>
          </Box>

          {message && (
            <Alert severity="info" sx={{ mb: 2 }} onClose={() => setMessage('')}>
              {message}
            </Alert>
          )}

          <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
            <Tab label="Estadísticas" icon={<Analytics />} />
            <Tab label="Enseñar" icon={<School />} />
            <Tab label="Conocimiento" icon={<AutoStories />} />
          </Tabs>

          {/* Panel de Estadísticas */}
          <TabPanel value={tabValue} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Box display="flex" alignItems="center" mb={1}>
                      <Memory color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h6">Memoria</Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      Conversaciones: {learningStats.total_conversations || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Memoria corto plazo: {learningStats.short_term_memory || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Patrones a largo plazo: {learningStats.long_term_patterns || 0}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Box display="flex" alignItems="center" mb={1}>
                      <TrendingUp color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h6">Aprendizaje</Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      Entradas de conocimiento: {learningStats.knowledge_entries || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Patrones aprendidos: {learningStats.learned_patterns || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Tamaño vocabulario: {learningStats.vocabulary_size || 0}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" mb={2}>
                      Feedback Promedio
                    </Typography>
                    <Box display="flex" alignItems="center">
                      <Box width="100%" mr={1}>
                        <LinearProgress 
                          variant="determinate" 
                          value={((learningStats.average_feedback || 0) + 1) * 50}
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        {((learningStats.average_feedback || 0) * 100).toFixed(1)}%
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>

          {/* Panel de Enseñanza */}
          <TabPanel value={tabValue} index={1}>
            <Box>
              <Typography variant="h6" mb={2}>
                Enseñar Nuevo Conocimiento
              </Typography>
              <Typography variant="body2" color="text.secondary" mb={3}>
                Enséñale directamente a ARIA nuevos conceptos y definiciones.
              </Typography>
              
              <Button
                variant="contained"
                startIcon={<School />}
                onClick={() => setTeachingDialog(true)}
                sx={{ mb: 2 }}
              >
                Enseñar Concepto
              </Button>

              <Typography variant="body1" mb={1}>
                💡 <strong>Cómo funciona el aprendizaje:</strong>
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemText primary="• ARIA aprende de cada conversación automáticamente" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="• Extrae patrones y conocimiento de las respuestas" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="• Crea embeddings semánticos para entender contexto" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="• Mejora las respuestas basándose en feedback" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="• Consolida memoria a corto plazo en conocimiento permanente" />
                </ListItem>
              </List>
            </Box>
          </TabPanel>

          {/* Panel de Conocimiento */}
          <TabPanel value={tabValue} index={2}>
            <Box>
              <Typography variant="h6" mb={2}>
                Exportar Conocimiento
              </Typography>
              <Typography variant="body2" color="text.secondary" mb={3}>
                Descarga todo el conocimiento que ARIA ha aprendido.
              </Typography>
              
              <Button
                variant="contained"
                startIcon={<Download />}
                onClick={handleExport}
                disabled={loading}
                sx={{ mb: 2 }}
              >
                Exportar Conocimiento
              </Button>

              <Typography variant="body1" mb={1}>
                📚 <strong>Base de Conocimiento:</strong>
              </Typography>
              <Box display="flex" gap={1} flexWrap="wrap">
                <Chip label={`${learningStats.knowledge_entries || 0} conceptos`} />
                <Chip label={`${learningStats.learned_patterns || 0} patrones`} />
                <Chip label={`${learningStats.vocabulary_size || 0} palabras`} />
              </Box>
            </Box>
          </TabPanel>
        </CardContent>
      </Card>

      {/* Dialog de Enseñanza */}
      <Dialog open={teachingDialog} onClose={() => setTeachingDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Box display="flex" alignItems="center">
            <School sx={{ mr: 1 }} />
            Enseñar Nuevo Concepto
          </Box>
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Concepto"
            value={teachData.concept}
            onChange={(e) => setTeachData(prev => ({ ...prev, concept: e.target.value }))}
            placeholder="Ej: Inteligencia Artificial"
            sx={{ mb: 2, mt: 1 }}
          />
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Definición"
            value={teachData.definition}
            onChange={(e) => setTeachData(prev => ({ ...prev, definition: e.target.value }))}
            placeholder="Ej: La inteligencia artificial es una rama de la informática que busca crear sistemas capaces de realizar tareas que requieren inteligencia humana..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTeachingDialog(false)}>Cancelar</Button>
          <Button onClick={handleTeach} variant="contained" disabled={loading}>
            Enseñar
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog de Exportación */}
      <Dialog open={exportDialog} onClose={() => setExportDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Conocimiento Exportado</DialogTitle>
        <DialogContent>
          {exportedKnowledge && (
            <Box>
              <Typography variant="h6" mb={1}>Conceptos Aprendidos:</Typography>
              <Typography variant="body2" mb={2}>
                {exportedKnowledge.concepts?.length || 0} conceptos encontrados
              </Typography>
              
              <Typography variant="h6" mb={1}>Patrones Exitosos:</Typography>
              <Typography variant="body2" mb={2}>
                {exportedKnowledge.successful_patterns?.length || 0} patrones de respuesta
              </Typography>

              <Button
                variant="contained"
                startIcon={<Download />}
                onClick={downloadKnowledge}
                sx={{ mt: 2 }}
              >
                Descargar JSON
              </Button>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setExportDialog(false)}>Cerrar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
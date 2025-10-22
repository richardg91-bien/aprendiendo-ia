import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Chip,
  LinearProgress,
  Grid,
  IconButton,
  Paper,
  Fade,
  Grow,
  Zoom,
  CircularProgress
} from '@mui/material';
import {
  CloudSync,
  AutoAwesome,
  Bolt,
  Speed,
  Memory,
  Visibility,
  VolumeUp,
  School,
  TrendingUp
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import RobotFace from './RobotFace';

const FuturisticAriaInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [ariaEmotion, setAriaEmotion] = useState('neutral');
  const [emotionColor, setEmotionColor] = useState('#0080FF');
  const [isThinking, setIsThinking] = useState(false);
  const [isLearning, setIsLearning] = useState(false);
  const [cloudStats, setCloudStats] = useState({
    knowledge_count: 0,
    ai_sources: 0,
    confidence: 0
  });
  const [recentEmotions, setRecentEmotions] = useState([]);
  const chatContainerRef = useRef(null);

  // Configuración de colores emocionales
  const emotionColors = {
    neutral: '#0080FF',      // Azul - Estado normal/interacción
    learning: '#00FF00',     // Verde - Aprendiendo
    frustrated: '#FF0000',   // Rojo - Molesta/Frustrada
    happy: '#FFD700',        // Dorado - Feliz
    thinking: '#8A2BE2',     // Púrpura - Pensando
    excited: '#FF69B4',      // Rosa - Emocionada
    satisfied: '#32CD32'     // Verde lima - Satisfecha
  };

  // Efectos de partículas futuristas
  const ParticleEffect = ({ emotion }) => {
    const particles = Array.from({ length: 50 }, (_, i) => i);
    
    return (
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          pointerEvents: 'none',
          overflow: 'hidden'
        }}
      >
        {particles.map((particle) => (
          <motion.div
            key={particle}
            initial={{
              x: Math.random() * window.innerWidth,
              y: Math.random() * window.innerHeight,
              opacity: 0
            }}
            animate={{
              x: Math.random() * window.innerWidth,
              y: Math.random() * window.innerHeight,
              opacity: [0, 1, 0]
            }}
            transition={{
              duration: Math.random() * 3 + 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            style={{
              position: 'absolute',
              width: '2px',
              height: '2px',
              backgroundColor: emotionColors[emotion] || '#0080FF',
              borderRadius: '50%',
              boxShadow: `0 0 6px ${emotionColors[emotion] || '#0080FF'}`
            }}
          />
        ))}
      </Box>
    );
  };

  // Componente de cerebro pulsante
  // Actualizar emociones desde el servidor
  useEffect(() => {
    const fetchEmotions = async () => {
      try {
        const response = await fetch('/api/cloud/emotions/recent');
        if (response.ok) {
          const emotions = await response.json();
          if (emotions.length > 0) {
            const latest = emotions[0];
            setAriaEmotion(latest.emotion_type);
            setEmotionColor(latest.color_code);
            setRecentEmotions(emotions);
          }
        }
      } catch (error) {
        console.error('Error fetching emotions:', error);
      }
    };

    fetchEmotions();
    const interval = setInterval(fetchEmotions, 3000);
    return () => clearInterval(interval);
  }, []);

  // Actualizar estadísticas de la nube
  useEffect(() => {
    const fetchCloudStats = async () => {
      try {
        const response = await fetch('/api/cloud/stats');
        if (response.ok) {
          const stats = await response.json();
          setCloudStats(stats);
        }
      } catch (error) {
        console.error('Error fetching cloud stats:', error);
      }
    };

    fetchCloudStats();
    const interval = setInterval(fetchCloudStats, 10000);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsThinking(true);
    setAriaEmotion('thinking');

    try {
      const response = await fetch('/api/chat/futuristic', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: inputMessage,
          emotion_context: ariaEmotion 
        })
      });

      const data = await response.json();

      if (data.success) {
        const ariaMessage = {
          id: Date.now() + 1,
          text: data.response,
          sender: 'aria',
          timestamp: new Date(),
          emotion: data.emotion,
          confidence: data.confidence,
          learned_something: data.learned_something
        };

        setMessages(prev => [...prev, ariaMessage]);
        
        if (data.emotion) {
          setAriaEmotion(data.emotion);
          setEmotionColor(emotionColors[data.emotion] || '#0080FF');
        }

        if (data.learned_something) {
          setIsLearning(true);
          setTimeout(() => setIsLearning(false), 3000);
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setAriaEmotion('frustrated');
      setEmotionColor(emotionColors.frustrated);
    } finally {
      setIsThinking(false);
    }
  };

  const triggerCloudLearning = async () => {
    setIsLearning(true);
    setAriaEmotion('learning');
    
    try {
      const response = await fetch('/api/cloud/learn_from_ais', {
        method: 'POST'
      });
      
      const data = await response.json();
      
      if (data.success) {
        setAriaEmotion('satisfied');
        // Actualizar estadísticas
        setTimeout(() => {
          window.location.reload(); // Recargar para mostrar nuevos datos
        }, 2000);
      } else {
        setAriaEmotion('frustrated');
      }
    } catch (error) {
      console.error('Error in cloud learning:', error);
      setAriaEmotion('frustrated');
    } finally {
      setIsLearning(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)`,
        color: 'white',
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Efecto de partículas de fondo */}
      <ParticleEffect emotion={ariaEmotion} />

      {/* CSS para animaciones adicionales */}
      <style>
        {`
          @keyframes pulse {
            0% { box-shadow: 0 0 30px ${emotionColor}; }
            50% { box-shadow: 0 0 60px ${emotionColor}, 0 0 90px ${emotionColor}; }
            100% { box-shadow: 0 0 30px ${emotionColor}; }
          }
          
          @keyframes glow {
            0% { text-shadow: 0 0 10px ${emotionColor}; }
            50% { text-shadow: 0 0 20px ${emotionColor}, 0 0 30px ${emotionColor}; }
            100% { text-shadow: 0 0 10px ${emotionColor}; }
          }
          
          .glowing-text {
            animation: glow 2s ease-in-out infinite alternate;
          }
        `}
      </style>

      {/* Header Futurista */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          py: 3,
          borderBottom: `2px solid ${emotionColor}`,
          boxShadow: `0 2px 20px ${emotionColor}30`
        }}
      >
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <Typography
            variant="h3"
            className="glowing-text"
            sx={{
              fontWeight: 'bold',
              background: `linear-gradient(45deg, ${emotionColor}, #ffffff)`,
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              textAlign: 'center'
            }}
          >
            A.R.I.A - Futuristic AI
          </Typography>
        </motion.div>
      </Box>

      {/* Panel Principal */}
      <Grid container spacing={3} sx={{ p: 3 }}>
        
        {/* Panel de Chat Futurista */}
        <Grid item xs={12} md={8}>
          <motion.div
            initial={{ opacity: 0, x: -100 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <Card
              sx={{
                background: 'rgba(26, 26, 46, 0.9)',
                border: `2px solid ${emotionColor}`,
                boxShadow: `0 0 30px ${emotionColor}30`,
                backdropFilter: 'blur(10px)',
                height: '70vh'
              }}
            >
              <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                
                {/* Cara del Robot */}
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                  <RobotFace 
                    emotion={ariaEmotion} 
                    confidence={cloudStats.confidence || 0.8} 
                  />
                </Box>

                {/* Estado Emocional */}
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                  <Chip
                    label={`Estado: ${ariaEmotion.toUpperCase()}`}
                    sx={{
                      backgroundColor: emotionColor,
                      color: 'white',
                      fontWeight: 'bold',
                      boxShadow: `0 0 10px ${emotionColor}`
                    }}
                  />
                </Box>

                {/* Área de mensajes */}
                <Box
                  ref={chatContainerRef}
                  sx={{
                    flex: 1,
                    overflowY: 'auto',
                    mb: 2,
                    p: 2,
                    border: `1px solid ${emotionColor}30`,
                    borderRadius: 2,
                    backgroundColor: 'rgba(0,0,0,0.3)'
                  }}
                >
                  <AnimatePresence>
                    {messages.map((message) => (
                      <motion.div
                        key={message.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <Box
                          sx={{
                            display: 'flex',
                            justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                            mb: 2
                          }}
                        >
                          <Paper
                            sx={{
                              p: 2,
                              maxWidth: '70%',
                              backgroundColor: message.sender === 'user' 
                                ? 'rgba(0,128,255,0.3)' 
                                : `rgba(${parseInt(emotionColor.slice(1,3), 16)}, ${parseInt(emotionColor.slice(3,5), 16)}, ${parseInt(emotionColor.slice(5,7), 16)}, 0.3)`,
                              border: `1px solid ${message.sender === 'user' ? '#0080FF' : emotionColor}`,
                              borderRadius: 3,
                              boxShadow: `0 0 15px ${message.sender === 'user' ? '#0080FF30' : emotionColor + '30'}`
                            }}
                          >
                            <Typography variant="body1">
                              {message.text}
                            </Typography>
                            {message.confidence && (
                              <Typography variant="caption" sx={{ opacity: 0.7 }}>
                                Confianza: {(message.confidence * 100).toFixed(1)}%
                              </Typography>
                            )}
                          </Paper>
                        </Box>
                      </motion.div>
                    ))}
                  </AnimatePresence>

                  {/* Indicador de escritura */}
                  {isThinking && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <CircularProgress size={20} sx={{ color: emotionColor, mr: 1 }} />
                        <Typography variant="body2" sx={{ color: emotionColor }}>
                          ARIA está procesando...
                        </Typography>
                      </Box>
                    </motion.div>
                  )}
                </Box>

                {/* Input de mensaje */}
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <TextField
                    fullWidth
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Escribe tu mensaje a ARIA..."
                    variant="outlined"
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        backgroundColor: 'rgba(0,0,0,0.3)',
                        '& fieldset': {
                          borderColor: emotionColor,
                        },
                        '&:hover fieldset': {
                          borderColor: emotionColor,
                          boxShadow: `0 0 10px ${emotionColor}30`
                        },
                        '&.Mui-focused fieldset': {
                          borderColor: emotionColor,
                          boxShadow: `0 0 20px ${emotionColor}50`
                        },
                      },
                      '& .MuiInputBase-input': {
                        color: 'white',
                      }
                    }}
                  />
                  <Button
                    variant="contained"
                    onClick={sendMessage}
                    disabled={!inputMessage.trim() || isThinking}
                    sx={{
                      backgroundColor: emotionColor,
                      boxShadow: `0 0 20px ${emotionColor}50`,
                      '&:hover': {
                        backgroundColor: emotionColor,
                        boxShadow: `0 0 30px ${emotionColor}70`
                      }
                    }}
                  >
                    Enviar
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Panel de Control de Nube */}
        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {/* Estadísticas de la Nube */}
            <Card
              sx={{
                background: 'rgba(26, 26, 46, 0.9)',
                border: `2px solid ${emotionColor}`,
                boxShadow: `0 0 30px ${emotionColor}30`,
                backdropFilter: 'blur(10px)',
                mb: 2
              }}
            >
              <CardContent>
                <Typography variant="h6" sx={{ color: emotionColor, mb: 2 }}>
                  🌐 Base de Datos en la Nube
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" sx={{ color: emotionColor }}>
                        {cloudStats.knowledge_count}
                      </Typography>
                      <Typography variant="caption">
                        Conocimientos
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" sx={{ color: emotionColor }}>
                        {cloudStats.ai_sources}
                      </Typography>
                      <Typography variant="caption">
                        Fuentes IA
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>

                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    Confianza Promedio
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={cloudStats.confidence * 100}
                    sx={{
                      height: 8,
                      borderRadius: 5,
                      backgroundColor: 'rgba(255,255,255,0.1)',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: emotionColor,
                        boxShadow: `0 0 10px ${emotionColor}`
                      }
                    }}
                  />
                </Box>

                <Button
                  fullWidth
                  variant="contained"
                  onClick={triggerCloudLearning}
                  disabled={isLearning}
                  startIcon={isLearning ? <CircularProgress size={20} /> : <CloudSync />}
                  sx={{
                    mt: 2,
                    backgroundColor: emotionColor,
                    boxShadow: `0 0 20px ${emotionColor}50`,
                    '&:hover': {
                      backgroundColor: emotionColor,
                      boxShadow: `0 0 30px ${emotionColor}70`
                    }
                  }}
                >
                  {isLearning ? 'Aprendiendo...' : 'Aprender de Otras IAs'}
                </Button>
              </CardContent>
            </Card>

            {/* Emociones Recientes */}
            <Card
              sx={{
                background: 'rgba(26, 26, 46, 0.9)',
                border: `2px solid ${emotionColor}`,
                boxShadow: `0 0 30px ${emotionColor}30`,
                backdropFilter: 'blur(10px)'
              }}
            >
              <CardContent>
                <Typography variant="h6" sx={{ color: emotionColor, mb: 2 }}>
                  🎭 Emociones Recientes
                </Typography>
                
                <Box sx={{ maxHeight: '200px', overflowY: 'auto' }}>
                  {recentEmotions.slice(0, 5).map((emotion, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Box
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          mb: 1,
                          p: 1,
                          backgroundColor: 'rgba(0,0,0,0.2)',
                          borderRadius: 1,
                          border: `1px solid ${emotion.color_code}30`
                        }}
                      >
                        <Box
                          sx={{
                            width: 12,
                            height: 12,
                            borderRadius: '50%',
                            backgroundColor: emotion.color_code,
                            boxShadow: `0 0 10px ${emotion.color_code}`,
                            mr: 1
                          }}
                        />
                        <Typography variant="body2" sx={{ flex: 1 }}>
                          {emotion.emotion_type}
                        </Typography>
                        <Typography variant="caption" sx={{ opacity: 0.7 }}>
                          {emotion.intensity * 100}%
                        </Typography>
                      </Box>
                    </motion.div>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default FuturisticAriaInterface;
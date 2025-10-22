import React, { useState, useEffect, useRef } from 'react';
import {
  Card,
  CardContent,
  TextField,
  Button,
  Box,
  Typography,
  Paper,
  CircularProgress,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Send,
  Psychology,
  Person,
  Clear,
  ThumbUp,
  ThumbDown,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

const ChatInterface = ({ serverStatus }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll al final
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Mensaje de bienvenida
  useEffect(() => {
    setMessages([
      {
        id: 1,
        type: 'assistant',
        content: '¡Hola! Soy **ARIA**, tu asistente IA avanzado. Puedo ayudarte con información, realizar búsquedas web y aprender de nuestras conversaciones. ¿En qué puedo ayudarte hoy? 🧠✨',
        timestamp: new Date(),
      }
    ]);
  }, []);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading || serverStatus !== 'connected') return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputValue }),
      });

      const data = await response.json();
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: data.response,
        confidence: data.confidence,
        learningStats: data.learning_stats,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: 'Error de conexión. Verifica que el servidor ARIA esté ejecutándose.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const provideFeedback = async (messageId, feedback) => {
    try {
      await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message_id: messageId,
          feedback: feedback,
          rating: feedback === 'positive' ? 5 : 1
        }),
      });
      
      // Actualizar el mensaje con el feedback
      setMessages(prev => 
        prev.map(msg => 
          msg.id === messageId 
            ? { ...msg, userFeedback: feedback }
            : msg
        )
      );
    } catch (error) {
      console.error('Error enviando feedback:', error);
    }
  };

  return (
    <Card 
      elevation={3}
      sx={{ 
        height: '70vh',
        display: 'flex',
        flexDirection: 'column',
        background: 'rgba(26, 26, 26, 0.8)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
      }}
    >
      <CardContent sx={{ 
        flexGrow: 1, 
        display: 'flex', 
        flexDirection: 'column',
        p: 2,
      }}>
        {/* Header del Chat */}
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          mb: 2,
          pb: 1,
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        }}>
          <Typography variant="h6" sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 1,
            color: 'primary.main',
          }}>
            <Psychology />
            Chat con ARIA
          </Typography>
          <Tooltip title="Limpiar chat">
            <IconButton onClick={clearChat} size="small">
              <Clear />
            </IconButton>
          </Tooltip>
        </Box>

        {/* Área de Mensajes */}
        <Box sx={{ 
          flexGrow: 1, 
          overflowY: 'auto',
          mb: 2,
          pr: 1,
          '&::-webkit-scrollbar': {
            width: '6px',
          },
          '&::-webkit-scrollbar-track': {
            background: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '3px',
          },
          '&::-webkit-scrollbar-thumb': {
            background: 'rgba(255, 255, 255, 0.2)',
            borderRadius: '3px',
            '&:hover': {
              background: 'rgba(255, 255, 255, 0.3)',
            },
          },
        }}>
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    mb: 2,
                    ml: message.type === 'user' ? 4 : 0,
                    mr: message.type === 'user' ? 0 : 4,
                    backgroundColor: 
                      message.type === 'user' 
                        ? 'primary.main'
                        : message.type === 'error'
                        ? 'error.main'
                        : 'background.paper',
                    color: message.type === 'user' ? 'white' : 'text.primary',
                    borderRadius: 2,
                    position: 'relative',
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                    <Box sx={{ 
                      backgroundColor: 
                        message.type === 'user' 
                          ? 'rgba(255, 255, 255, 0.2)'
                          : 'rgba(25, 118, 210, 0.2)',
                      borderRadius: '50%',
                      p: 0.5,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}>
                      {message.type === 'user' ? (
                        <Person sx={{ fontSize: 16 }} />
                      ) : (
                        <Psychology sx={{ fontSize: 16, color: 'primary.main' }} />
                      )}
                    </Box>
                    
                    <Box sx={{ flexGrow: 1 }}>
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                      
                      {/* Información adicional para respuestas de IA */}
                      {message.type === 'assistant' && (message.confidence || message.learningStats) && (
                        <Box sx={{ mt: 1, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                          {message.confidence && (
                            <Chip 
                              label={`Confianza: ${(message.confidence * 100).toFixed(0)}%`}
                              size="small"
                              color={message.confidence > 0.7 ? 'success' : message.confidence > 0.4 ? 'warning' : 'error'}
                              variant="outlined"
                            />
                          )}
                          {message.learningStats && (
                            <Chip 
                              label={`🧠 ${message.learningStats.total_conversations || 0} conversaciones`}
                              size="small"
                              color="info"
                              variant="outlined"
                            />
                          )}
                        </Box>
                      )}

                      {/* Botones de feedback para mensajes de IA */}
                      {message.type === 'assistant' && (
                        <Box sx={{ mt: 1, display: 'flex', gap: 0.5 }}>
                          <Tooltip title="Respuesta útil">
                            <IconButton 
                              size="small"
                              onClick={() => provideFeedback(message.id, 'positive')}
                              color={message.userFeedback === 'positive' ? 'primary' : 'default'}
                            >
                              <ThumbUp fontSize="small" />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Mejorar respuesta">
                            <IconButton 
                              size="small"
                              onClick={() => provideFeedback(message.id, 'negative')}
                              color={message.userFeedback === 'negative' ? 'error' : 'default'}
                            >
                              <ThumbDown fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      )}
                    </Box>
                  </Box>
                  
                  <Typography 
                    variant="caption" 
                    sx={{ 
                      position: 'absolute',
                      bottom: 4,
                      right: 8,
                      color: 'rgba(255, 255, 255, 0.6)',
                    }}
                  >
                    {message.timestamp.toLocaleTimeString()}
                  </Typography>
                </Paper>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Indicador de escritura */}
          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <Paper sx={{ p: 2, mr: 4, backgroundColor: 'background.paper' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Psychology sx={{ color: 'primary.main' }} />
                  <Typography variant="body2" color="text.secondary">
                    ARIA está pensando...
                  </Typography>
                  <CircularProgress size={16} />
                </Box>
              </Paper>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </Box>

        {/* Input de Mensaje */}
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            multiline
            maxRows={3}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe tu mensaje aquí..."
            disabled={isLoading || serverStatus !== 'connected'}
            variant="outlined"
            sx={{
              '& .MuiOutlinedInput-root': {
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                '& fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.2)',
                },
                '&:hover fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.3)',
                },
                '&.Mui-focused fieldset': {
                  borderColor: 'primary.main',
                },
              },
            }}
          />
          <Button
            variant="contained"
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading || serverStatus !== 'connected'}
            sx={{
              minWidth: 56,
              height: 56,
              borderRadius: 2,
            }}
          >
            {isLoading ? <CircularProgress size={24} /> : <Send />}
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ChatInterface;
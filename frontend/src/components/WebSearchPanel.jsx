import React, { useState } from 'react';
import {
  Card,
  CardContent,
  TextField,
  Button,
  Box,
  Typography,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Chip,
  IconButton,
  Tooltip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Search,
  Web,
  ExpandMore,
  OpenInNew,
  BookmarkBorder,
  Bookmark,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const WebSearchPanel = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [recentSearches, setRecentSearches] = useState([]);
  const [bookmarkedResults, setBookmarkedResults] = useState([]);

  const performWebSearch = async () => {
    if (!searchTerm.trim() || isSearching) return;

    setIsSearching(true);
    
    try {
      const response = await fetch('/api/buscar_web', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: searchTerm }),
      });

      const data = await response.json();
      
      if (response.ok && data.success) {
        // Transformar la respuesta del backend
        const resultados = data.resultados || [];
        setSearchResults(resultados.map(item => ({
          titulo: item.titulo,
          descripcion: item.contenido, // El backend usa 'contenido' como descripción
          url: item.url,
          contenido: item.contenido,
          fuente: item.fuente
        })));
        setRecentSearches(prev => [
          searchTerm,
          ...prev.filter(term => term !== searchTerm).slice(0, 4)
        ]);
      } else {
        console.error('Error en búsqueda:', data.error || 'Error desconocido');
        setSearchResults([]);
      }
    } catch (error) {
      console.error('Error en búsqueda web:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      performWebSearch();
    }
  };

  const toggleBookmark = (result) => {
    setBookmarkedResults(prev => {
      const isBookmarked = prev.some(item => item.url === result.url);
      if (isBookmarked) {
        return prev.filter(item => item.url !== result.url);
      } else {
        return [...prev, result];
      }
    });
  };

  const isBookmarked = (result) => {
    return bookmarkedResults.some(item => item.url === result.url);
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
          <Web />
          Búsqueda Web
        </Typography>

        {/* Campo de búsqueda */}
        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
          <TextField
            fullWidth
            size="small"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Buscar en la web..."
            disabled={isSearching}
            variant="outlined"
            sx={{
              '& .MuiOutlinedInput-root': {
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                '& fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.2)',
                },
              },
            }}
          />
          <Button
            variant="contained"
            onClick={performWebSearch}
            disabled={!searchTerm.trim() || isSearching}
            size="small"
            sx={{ minWidth: 48 }}
          >
            {isSearching ? <CircularProgress size={20} /> : <Search />}
          </Button>
        </Box>

        {/* Búsquedas recientes */}
        {recentSearches.length > 0 && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" sx={{ mb: 1, color: 'text.secondary' }}>
              Búsquedas recientes:
            </Typography>
            <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
              {recentSearches.map((term, index) => (
                <Chip
                  key={index}
                  label={term}
                  size="small"
                  onClick={() => {
                    setSearchTerm(term);
                    // Automáticamente buscar cuando se selecciona un término reciente
                    const performSearch = async () => {
                      setIsSearching(true);
                      try {
                        const response = await fetch('/api/buscar_web', {
                          method: 'POST',
                          headers: {
                            'Content-Type': 'application/json',
                          },
                          body: JSON.stringify({ query: term }),
                        });

                        const data = await response.json();
                        
                        if (response.ok && data.success) {
                          const resultados = data.resultados || [];
                          setSearchResults(resultados.map(item => ({
                            titulo: item.titulo,
                            descripcion: item.contenido,
                            url: item.url,
                            contenido: item.contenido,
                            fuente: item.fuente
                          })));
                        } else {
                          console.error('Error en búsqueda:', data.error || 'Error desconocido');
                          setSearchResults([]);
                        }
                      } catch (error) {
                        console.error('Error en búsqueda web:', error);
                        setSearchResults([]);
                      } finally {
                        setIsSearching(false);
                      }
                    };
                    performSearch();
                  }}
                  sx={{ cursor: 'pointer' }}
                />
              ))}
            </Box>
          </Box>
        )}

        {/* Resultados de búsqueda */}
        {searchResults.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Typography variant="subtitle2" sx={{ mb: 1, color: 'text.secondary' }}>
              Resultados encontrados: {searchResults.length}
            </Typography>
            
            <List dense sx={{ maxHeight: 300, overflowY: 'auto' }}>
              {searchResults.map((result, index) => (
                <ListItem
                  key={index}
                  sx={{
                    backgroundColor: 'rgba(255, 255, 255, 0.02)',
                    borderRadius: 1,
                    mb: 1,
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                  }}
                >
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                          {result.titulo || result.url}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 0.5 }}>
                          <Tooltip title={isBookmarked(result) ? "Quitar de favoritos" : "Agregar a favoritos"}>
                            <IconButton 
                              size="small"
                              onClick={() => toggleBookmark(result)}
                              color={isBookmarked(result) ? "primary" : "default"}
                            >
                              {isBookmarked(result) ? <Bookmark /> : <BookmarkBorder />}
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Abrir en nueva pestaña">
                            <IconButton 
                              size="small"
                              onClick={() => window.open(result.url, '_blank')}
                            >
                              <OpenInNew />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      </Box>
                    }
                    secondary={
                      <Typography variant="caption" color="text.secondary">
                        {result.descripcion || result.contenido?.substring(0, 100) + '...'}
                      </Typography>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </motion.div>
        )}

        {/* Favoritos */}
        {bookmarkedResults.length > 0 && (
          <Accordion sx={{ mt: 2, backgroundColor: 'rgba(255, 255, 255, 0.02)' }}>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Typography variant="subtitle2">
                Favoritos ({bookmarkedResults.length})
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <List dense>
                {bookmarkedResults.map((result, index) => (
                  <ListItem
                    key={index}
                    sx={{
                      backgroundColor: 'rgba(25, 118, 210, 0.1)',
                      borderRadius: 1,
                      mb: 1,
                    }}
                  >
                    <ListItemText
                      primary={result.titulo || result.url}
                      secondary={result.descripcion}
                    />
                    <IconButton 
                      size="small"
                      onClick={() => window.open(result.url, '_blank')}
                    >
                      <OpenInNew />
                    </IconButton>
                  </ListItem>
                ))}
              </List>
            </AccordionDetails>
          </Accordion>
        )}

        {/* Estado sin resultados */}
        {searchResults.length === 0 && !isSearching && searchTerm && (
          <Box sx={{ 
            textAlign: 'center', 
            py: 3,
            color: 'text.secondary',
          }}>
            <Web sx={{ fontSize: 48, opacity: 0.3, mb: 1 }} />
            <Typography variant="body2">
              No se encontraron resultados para "{searchTerm}"
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default WebSearchPanel;
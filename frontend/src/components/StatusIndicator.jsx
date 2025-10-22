import React from 'react';
import {
  Box,
  Chip,
  Tooltip,
  Typography,
} from '@mui/material';
import {
  CheckCircle,
  Error,
  HourglassEmpty,
  Cloud,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const StatusIndicator = ({ status }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'connected':
        return {
          icon: <CheckCircle />,
          label: 'Conectado',
          color: 'success',
          description: 'Servidor ARIA funcionando correctamente',
        };
      case 'connecting':
        return {
          icon: <HourglassEmpty />,
          label: 'Conectando',
          color: 'warning',
          description: 'Estableciendo conexión con el servidor...',
        };
      case 'error':
        return {
          icon: <Error />,
          label: 'Desconectado',
          color: 'error',
          description: 'No se puede conectar al servidor ARIA',
        };
      default:
        return {
          icon: <Cloud />,
          label: 'Desconocido',
          color: 'default',
          description: 'Estado del servidor desconocido',
        };
    }
  };

  const config = getStatusConfig();

  return (
    <Tooltip title={config.description} arrow>
      <Box
        component={motion.div}
        animate={{
          scale: status === 'connecting' ? [1, 1.05, 1] : 1,
        }}
        transition={{
          duration: 1,
          repeat: status === 'connecting' ? Infinity : 0,
        }}
      >
        <Chip
          icon={config.icon}
          label={
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography variant="caption" sx={{ fontWeight: 500 }}>
                {config.label}
              </Typography>
              {status === 'connected' && (
                <Box
                  sx={{
                    width: 8,
                    height: 8,
                    borderRadius: '50%',
                    backgroundColor: 'success.main',
                    animation: 'pulse 2s infinite',
                    '@keyframes pulse': {
                      '0%': {
                        boxShadow: '0 0 0 0 rgba(76, 175, 80, 0.7)',
                      },
                      '70%': {
                        boxShadow: '0 0 0 10px rgba(76, 175, 80, 0)',
                      },
                      '100%': {
                        boxShadow: '0 0 0 0 rgba(76, 175, 80, 0)',
                      },
                    },
                  }}
                />
              )}
            </Box>
          }
          color={config.color}
          variant="outlined"
          size="small"
          sx={{
            backgroundColor: 
              status === 'connected' 
                ? 'rgba(76, 175, 80, 0.1)'
                : status === 'error'
                ? 'rgba(244, 67, 54, 0.1)'
                : 'rgba(255, 152, 0, 0.1)',
            borderColor:
              status === 'connected'
                ? 'success.main'
                : status === 'error'
                ? 'error.main'
                : 'warning.main',
          }}
        />
      </Box>
    </Tooltip>
  );
};

export default StatusIndicator;
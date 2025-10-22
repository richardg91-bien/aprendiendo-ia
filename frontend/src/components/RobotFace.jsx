import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Paper } from '@mui/material';

const RobotFace = ({ emotion = 'neutral', confidence = 0.8 }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  
  // Estados para animación
  const [currentColor, setCurrentColor] = useState([0, 122, 255]); // Azul inicial
  const [targetColor, setTargetColor] = useState([0, 122, 255]);
  const [transitionT, setTransitionT] = useState(0);
  
  // Configuración de colores por emoción (constante para evitar recreación)
  const emotionColors = React.useMemo(() => ({
    neutral: [0, 122, 255],      // Azul
    learning: [0, 255, 127],     // Verde
    frustrated: [255, 40, 40],   // Rojo
    happy: [255, 215, 0],        // Dorado
    thinking: [147, 112, 219],   // Púrpura
    excited: [255, 105, 180],    // Rosa
    satisfied: [50, 205, 50],    // Verde lima
    calm: [0, 191, 255],         // Azul cielo
    alert: [255, 69, 0]          // Rojo naranja
  }), []);

  // Función de interpolación de colores
  const lerp = (a, b, t) => Math.round(a + (b - a) * t);
  
  const rgbToHex = (rgb) => {
    return `#${rgb.map(c => Math.max(0, Math.min(255, c)).toString(16).padStart(2, '0')).join('')}`;
  };

  // Dibujar la cara del robot
  const drawRobotFace = useCallback((ctx, canvas, currentRgb, confidence) => {
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const faceRadius = Math.min(canvas.width, canvas.height) * 0.35;
    
    // Limpiar canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Fondo con gradiente radial
    const bgGradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, faceRadius * 1.5);
    bgGradient.addColorStop(0, 'rgba(17, 17, 17, 0.8)');
    bgGradient.addColorStop(1, 'rgba(0, 0, 0, 0.95)');
    ctx.fillStyle = bgGradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Cara del robot (círculo principal)
    const faceGradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, faceRadius);
    faceGradient.addColorStop(0, '#2a2a2a');
    faceGradient.addColorStop(1, '#1a1a1a');
    ctx.fillStyle = faceGradient;
    ctx.beginPath();
    ctx.arc(centerX, centerY, faceRadius, 0, 2 * Math.PI);
    ctx.fill();
    
    // Borde de la cara con brillo emocional
    ctx.strokeStyle = rgbToHex(currentRgb);
    ctx.lineWidth = 3;
    ctx.shadowColor = rgbToHex(currentRgb);
    ctx.shadowBlur = 15;
    ctx.stroke();
    ctx.shadowBlur = 0;
    
    // Ojos del robot
    const eyeWidth = faceRadius * 0.25;
    const eyeHeight = eyeWidth * 0.8;
    const eyeOffsetX = faceRadius * 0.35;
    const eyeOffsetY = faceRadius * 0.15;
    
    // Ojo izquierdo
    const leftEyeX = centerX - eyeOffsetX;
    const leftEyeY = centerY - eyeOffsetY;
    
    // Gradiente para los ojos
    const eyeGradient = ctx.createRadialGradient(leftEyeX, leftEyeY, 0, leftEyeX, leftEyeY, eyeWidth);
    eyeGradient.addColorStop(0, rgbToHex(currentRgb));
    eyeGradient.addColorStop(0.7, rgbToHex(currentRgb.map(c => Math.max(0, c - 50))));
    eyeGradient.addColorStop(1, rgbToHex(currentRgb.map(c => Math.max(0, c - 100))));
    
    ctx.fillStyle = eyeGradient;
    ctx.beginPath();
    ctx.ellipse(leftEyeX, leftEyeY, eyeWidth, eyeHeight, 0, 0, 2 * Math.PI);
    ctx.fill();
    
    // Ojo derecho
    const rightEyeX = centerX + eyeOffsetX;
    const rightEyeY = centerY - eyeOffsetY;
    
    const rightEyeGradient = ctx.createRadialGradient(rightEyeX, rightEyeY, 0, rightEyeX, rightEyeY, eyeWidth);
    rightEyeGradient.addColorStop(0, rgbToHex(currentRgb));
    rightEyeGradient.addColorStop(0.7, rgbToHex(currentRgb.map(c => Math.max(0, c - 50))));
    rightEyeGradient.addColorStop(1, rgbToHex(currentRgb.map(c => Math.max(0, c - 100))));
    
    ctx.fillStyle = rightEyeGradient;
    ctx.beginPath();
    ctx.ellipse(rightEyeX, rightEyeY, eyeWidth, eyeHeight, 0, 0, 2 * Math.PI);
    ctx.fill();
    
    // Brillos en los ojos
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.beginPath();
    ctx.ellipse(leftEyeX - eyeWidth * 0.3, leftEyeY - eyeHeight * 0.3, eyeWidth * 0.2, eyeHeight * 0.2, 0, 0, 2 * Math.PI);
    ctx.fill();
    
    ctx.beginPath();
    ctx.ellipse(rightEyeX - eyeWidth * 0.3, rightEyeY - eyeHeight * 0.3, eyeWidth * 0.2, eyeHeight * 0.2, 0, 0, 2 * Math.PI);
    ctx.fill();
    
    // Boca del robot (varía según confianza y emoción)
    const mouthY = centerY + faceRadius * 0.4;
    const mouthWidth = faceRadius * 0.6;
    const mouthHeight = 12;
    
    // Color de la boca basado en confianza
    let mouthIntensity = Math.max(20, Math.round(120 - (1 - confidence) * 100));
    if (emotion === 'frustrated' || emotion === 'alert') {
      mouthIntensity = Math.max(mouthIntensity, 60);
    } else if (emotion === 'happy' || emotion === 'satisfied') {
      mouthIntensity = Math.min(mouthIntensity + 40, 255);
    }
    
    ctx.fillStyle = `rgb(${mouthIntensity}, ${mouthIntensity}, ${mouthIntensity})`;
    ctx.fillRect(centerX - mouthWidth/2, mouthY - mouthHeight/2, mouthWidth, mouthHeight);
    
    // Borde de la boca
    ctx.strokeStyle = '#444444';
    ctx.lineWidth = 2;
    ctx.strokeRect(centerX - mouthWidth/2, mouthY - mouthHeight/2, mouthWidth, mouthHeight);
    
    // Indicador de confianza (barra circular alrededor de la cara)
    if (confidence < 1.0) {
      ctx.strokeStyle = confidence < 0.6 ? '#ff4444' : '#44ff44';
      ctx.lineWidth = 5;
      ctx.beginPath();
      ctx.arc(centerX, centerY, faceRadius + 10, -Math.PI/2, -Math.PI/2 + (2 * Math.PI * confidence));
      ctx.stroke();
    }
    
    // Efectos adicionales según la emoción
    if (emotion === 'thinking') {
      // Puntos parpadeantes alrededor de la cabeza
      const time = Date.now() / 1000;
      for (let i = 0; i < 8; i++) {
        const angle = (i / 8) * 2 * Math.PI;
        const x = centerX + Math.cos(angle) * (faceRadius + 25);
        const y = centerY + Math.sin(angle) * (faceRadius + 25);
        const opacity = (Math.sin(time * 3 + i) + 1) / 2;
        
        ctx.fillStyle = `rgba(147, 112, 219, ${opacity})`;
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fill();
      }
    } else if (emotion === 'learning') {
      // Ondas de expansión
      const time = Date.now() / 1000;
      for (let i = 0; i < 3; i++) {
        const waveRadius = faceRadius + (time * 30 + i * 20) % 60;
        const opacity = 1 - ((time * 30 + i * 20) % 60) / 60;
        
        ctx.strokeStyle = `rgba(0, 255, 127, ${opacity * 0.5})`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(centerX, centerY, waveRadius, 0, 2 * Math.PI);
        ctx.stroke();
      }
    }
  }, [emotion]);

  // Animación de transición de colores
  const animate = useCallback(() => {
    if (transitionT < 1.0) {
      const newT = Math.min(1.0, transitionT + 0.02);
      setTransitionT(newT);
      
      const newColor = [
        lerp(currentColor[0], targetColor[0], newT),
        lerp(currentColor[1], targetColor[1], newT),
        lerp(currentColor[2], targetColor[2], newT)
      ];
      
      setCurrentColor(newColor);
      
      if (newT >= 1.0) {
        setCurrentColor(targetColor);
        setTransitionT(0);
      }
    }
    
    // Dibujar en el canvas
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      drawRobotFace(ctx, canvas, currentColor, confidence);
    }
    
    animationRef.current = requestAnimationFrame(animate);
  }, [transitionT, currentColor, targetColor, confidence, drawRobotFace]);

  // Efecto para cambiar color según emoción
  useEffect(() => {
    const newTargetColor = emotionColors[emotion] || emotionColors.neutral;
    
    // Aplicar lógica de confianza (como en tu código original)
    let finalColor = newTargetColor;
    if (confidence < 0.6) {
      finalColor = emotionColors.alert || emotionColors.frustrated;
    }
    
    if (JSON.stringify(finalColor) !== JSON.stringify(targetColor)) {
      setTargetColor(finalColor);
      setTransitionT(0);
    }
  }, [emotion, confidence, emotionColors, targetColor]);

  // Iniciar animación
  useEffect(() => {
    animationRef.current = requestAnimationFrame(animate);
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [animate]);

  // Ajustar tamaño del canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const updateSize = () => {
        const container = canvas.parentElement;
        const size = Math.min(container.clientWidth, container.clientHeight, 300);
        canvas.width = size;
        canvas.height = size;
      };
      
      updateSize();
      window.addEventListener('resize', updateSize);
      return () => window.removeEventListener('resize', updateSize);
    }
  }, []);

  return (
    <Paper
      elevation={8}
      sx={{
        background: 'linear-gradient(145deg, #1a1a1a 0%, #2d2d30 100%)',
        borderRadius: '20px',
        padding: 2,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: 320,
        border: `2px solid ${rgbToHex(currentColor)}`,
        boxShadow: `0 0 20px ${rgbToHex(currentColor)}40`,
        transition: 'all 0.3s ease-in-out'
      }}
    >
      <canvas
        ref={canvasRef}
        style={{
          display: 'block',
          maxWidth: '100%',
          maxHeight: '100%'
        }}
      />
    </Paper>
  );
};

export default RobotFace;
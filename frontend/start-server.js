#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Configurar el puerto
process.env.PORT = process.env.PORT || '3001';

console.log(`🚀 Iniciando React en puerto ${process.env.PORT}`);

// Iniciar React Scripts
const child = spawn('npm', ['run', 'start-react'], {
  cwd: path.resolve(__dirname),
  stdio: 'inherit',
  env: { ...process.env }
});

child.on('error', (error) => {
  console.error('Error iniciando React:', error);
});

child.on('close', (code) => {
  console.log(`React process exited with code ${code}`);
});
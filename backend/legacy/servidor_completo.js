import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

// Proxy para las rutas de API
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:5002',
  changeOrigin: true,
  pathRewrite: {
    '^/api': '', // remueve /api del path
  },
}));

// Proxy para las rutas directas del backend
app.use(['/test', '/chat', '/buscar_web', '/red_neuronal_info', '/entrenar_red_neuronal'], 
  createProxyMiddleware({
    target: 'http://localhost:5002',
    changeOrigin: true,
  })
);

// Servir archivos estáticos del build
app.use(express.static(path.join(__dirname, 'aria-frontend/build')));

// Fallback para SPA
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'aria-frontend/build', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`🌐 Servidor combinado corriendo en http://localhost:${PORT}`);
  console.log(`🔄 Proxy backend: http://localhost:5002`);
  console.log(`📁 Sirviendo frontend desde: aria-frontend/build`);
});
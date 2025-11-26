const express = require('express');
const path = require('path');
const app = express();

// Servir archivos estáticos desde la carpeta dist
app.use(express.static(path.join(__dirname, 'dist/frontend-angular-clean-architecture')));

// Manejar todas las rutas de Angular
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist/frontend-angular-clean-architecture/index.html'));
});

const port = process.env.PORT || 4200;
app.listen(port, () => {
  console.log(`Servidor corriendo en el puerto ${port}`);
});



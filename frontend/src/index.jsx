import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'; // O componente principal da aplicação
import './styles/globals.scss'; // Importar estilos globais, se aplicável'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);

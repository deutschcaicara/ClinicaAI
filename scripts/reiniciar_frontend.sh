#!/bin/bash

# Caminho do projeto frontend
FRONTEND_DIR="C:/ClinicaAI/frontend"

# 1. Apagar o diretório antigo do frontend
echo "Limpando o diretório antigo do frontend..."
rm -rf "$FRONTEND_DIR"

# 2. Recriar o diretório e inicializar um novo projeto React
echo "Recriando o projeto frontend..."
mkdir -p "$FRONTEND_DIR"
cd "$FRONTEND_DIR" || exit
npx create-react-app . --template cra-template

# 3. Configurar estrutura básica
echo "Criando estrutura básica de pastas..."
mkdir -p src/pages src/components src/api src/utils src/styles

# 4. Limpar arquivos desnecessários do CRA
echo "Removendo arquivos desnecessários..."
rm -f src/App.css src/App.test.js src/logo.svg src/reportWebVitals.js src/setupTests.js

# 5. Criar arquivos básicos
echo "Criando arquivos básicos..."
cat > src/pages/HomePage.js <<EOL
import React from "react";

const HomePage = () => {
  return <h1>Bem-vindo ao Frontend da Clínica AI</h1>;
};

export default HomePage;
EOL

cat > src/App.js <<EOL
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
      </Routes>
    </Router>
  );
}

export default App;
EOL

cat > src/api/api.js <<EOL
import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:8000/api",
});

export default api;
EOL

# 6. Instalar dependências essenciais
echo "Instalando dependências essenciais..."
npm install react-router-dom axios

# 7. Finalizar
echo "Projeto frontend reiniciado com sucesso!"

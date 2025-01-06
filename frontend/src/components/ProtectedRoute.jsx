import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '@context/AuthContext';

// Componente para proteger rotas
const ProtectedRoute = ({ children }) => {
    const { isAuthenticated } = useContext(AuthContext); // Verifica autenticação

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />; // Redireciona para login se não autenticado
    }

    return children; // Renderiza a rota protegida
};

export default ProtectedRoute;

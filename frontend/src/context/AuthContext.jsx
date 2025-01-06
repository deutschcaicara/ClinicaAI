import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();

    // Inicializa o estado de autenticação ao carregar a página
    useEffect(() => {
        const token = localStorage.getItem('accessToken'); // Ajustado para "accessToken"
        if (token) {
            api.defaults.headers['Authorization'] = `Bearer ${token}`;
            setIsAuthenticated(true);
        } else {
            setIsAuthenticated(false);
        }
    }, []);

    // Função de login
    const login = async (credentials) => {
        try {
            const { access, refresh } = await api.post('/token/', credentials).then(res => res.data);
            localStorage.setItem('accessToken', access); // Alinha com "accessToken"
            localStorage.setItem('refreshToken', refresh);
            api.defaults.headers['Authorization'] = `Bearer ${access}`;
            setIsAuthenticated(true);
            setUser({ username: credentials.username }); // Atualiza o usuário logado
            navigate('/dashboard'); // Redireciona para o dashboard
        } catch (error) {
            console.error('Erro ao fazer login:', error);
            throw error.response?.data?.detail || 'Erro inesperado ao fazer login';
        }
    };

    // Função de logout
    const logout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        api.defaults.headers['Authorization'] = null;
        setIsAuthenticated(false);
        setUser(null);
        navigate('/login');
    };

    const contextValue = {
        user,
        isAuthenticated,
        login,
        logout,
    };

    return <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>;
};

import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/auth',
    timeout: 5000,
});

// Interceptor para adicionar o token ao cabeçalho
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Função para renovar o token
export const refreshToken = async () => {
    const refresh = localStorage.getItem('refreshToken');
    if (!refresh) throw new Error('Token de refresh não encontrado');

    try {
        const { data } = await api.post('/token/refresh/', { refresh });
        localStorage.setItem('accessToken', data.access); // Atualiza o token de acesso
        return data.access;
    } catch (error) {
        console.error('Erro ao renovar o token:', error);
        throw error;
    }
};

// Interceptor para renovar o token automaticamente
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const newToken = await refreshToken();
                api.defaults.headers['Authorization'] = `Bearer ${newToken}`;
                originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
                return api(originalRequest);
            } catch (err) {
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                window.location.href = '/login';
                return Promise.reject(err);
            }
        }
        return Promise.reject(error);
    }
);

export default api;

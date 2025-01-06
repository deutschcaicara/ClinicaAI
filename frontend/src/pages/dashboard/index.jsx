/* import React, { useContext, useState, useEffect } from 'react';
import { AuthContext } from '@context/AuthContext';
import DashboardHeader from '@dashboard/DashboardHeader';
import CardsContainer from '@components/dashboard/CardsContainer';
import api from '../../services/api';
import './dashboard.scss';

function Dashboard() {
  const { logout } = useContext(AuthContext); // Adicionar função de logout
  const [cardsData, setCardsData] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await api.get('/dashboard/');
        setCardsData(response.data);
      } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        setErrorMessage('Não foi possível carregar os dados do dashboard.');
      }
    }
    fetchData();
  }, []);

  if (errorMessage) {
    return <div className="error-message">{errorMessage}</div>;
  }

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>Menu</h2>
        <ul>
          <li><a href="#">Pacientes</a></li>
          <li><a href="#">Exames</a></li>
          <li><a href="#">Histórico</a></li>
          <li><a href="#">Configurações</a></li>
          <li><button onClick={logout}>Logout</button></li> {/* Botão de logout }
        </ul>
      </aside>

      <main className="main-content">
        <DashboardHeader title="Dashboard Clínico" />
        <CardsContainer cards={cardsData} />
      </main>
    </div>
  );
}

export default Dashboard;
 
*/

import React, { useContext } from 'react';
import { AuthContext } from '@context/AuthContext';
import './dashboard.scss';

const Dashboard = () => {
    const { logout, user } = useContext(AuthContext);

    return (
        <div className="dashboard">
            <aside className="sidebar">
                <h2>Bem-vindo, {user?.username}</h2>
                <ul>
                    <li><a href="#">Pacientes</a></li>
                    <li><a href="#">Exames</a></li>
                    <li><a href="#">Histórico</a></li>
                    <li><a href="#">Configurações</a></li>
                    <li><button onClick={logout}>Logout</button></li>
                </ul>
            </aside>
            <main className="main-content">
                <h1>Dashboard</h1>
                <p>Este é o dashboard clínico.</p>
            </main>
        </div>
    );
};

export default Dashboard;

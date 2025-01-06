import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './pacientes.scss';

function Patients() {
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    async function fetchPatients() {
      try {
        const response = await api.get('/pacientes/');
        setPatients(response.data);
      } catch (error) {
        console.error('Erro ao buscar pacientes:', error);
      }
    }
    fetchPatients();
  }, []);

  return (
    <div className="patients">
      <h1>Lista de Pacientes</h1>
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Idade</th>
            <th>CPF</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((patient) => (
            <tr key={patient.uuid}>
              <td>{patient.nome_completo}</td>
              <td>{new Date().getFullYear() - new Date(patient.data_nascimento).getFullYear()}</td>
              <td>{patient.cpf}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Patients;

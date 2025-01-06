import React from 'react';
import './dashboardHeader.scss';

function DashboardHeader({ title }) {
  return (
    <header className="dashboard-header">
      <h1>{title}</h1>
    </header>
  );
}

export default DashboardHeader;

import React from 'react';
import './cardsContainer.scss';

function CardsContainer({ cards }) {
  return (
    <section className="cards-container">
      {cards.map((card, index) => (
        <div className="card" key={index}>
          <h3>{card.title}</h3>
          <p>{card.value}</p>
        </div>
      ))}
    </section>
  );
}

export default CardsContainer;

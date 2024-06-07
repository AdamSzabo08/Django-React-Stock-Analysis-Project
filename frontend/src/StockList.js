// src/StockList.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './App.css';

function StockList() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/stocks/')
      .then(response => {
        setStocks(response.data);
      })
      .catch(error => {
        console.error('Error fetching stocks:', error);
      });
  }, []);

  return (
    <div className="container">
      <h1 className="heading">Stock List</h1>
      <ul className="list">
        {stocks.map(stock => (
          <li key={stock.id} className="list-item">
            <Link to={`/stocks/${stock.symbol}`} className="link">
              {stock.name} - {stock.symbol}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default StockList;

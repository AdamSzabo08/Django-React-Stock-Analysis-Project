// src/StockDetail.js
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function StockDetail() {
  const { symbol } = useParams();
  const [stockDetail, setStockDetail] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/stocks/${symbol}/`)
      .then(response => {
        setStockDetail(response.data);
      })
      .catch(error => {
        console.error('Error fetching stock detail:', error);
      });
  }, [symbol]);

  if (!stockDetail) return <div className="loading">Loading...</div>;

  // Reverse the stock_prices array to have the dates in ascending order
  const reversedStockPrices = [...stockDetail.stock_prices].reverse();

  const data = {
    labels: reversedStockPrices.map(price => price.date),
    datasets: [
      {
        label: 'Close Price',
        data: reversedStockPrices.map(price => price.close_price),
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76, 175, 80, 0.2)',
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${stockDetail.stock.name} (${stockDetail.stock.symbol}) Price Chart`,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Date',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Close Price',
        },
      },
    },
  };

  return (
    <div className="container">
      <h1 className="heading">{stockDetail.stock.name} ({stockDetail.stock.symbol}) - Stock Detail</h1>
      <Link to={`/stocks/${symbol}/analysis`} className="view-analysis-link">View Analysis</Link>
      <div className="chart-container">
        <Line data={data} options={options} />
      </div>
      <ul className="list">
        {reversedStockPrices.map(price => (
          <li key={price.date} className="list-item">
            Date: {price.date}, Close: {price.close_price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default StockDetail;

// src/StockAnalysis.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './App.css';

function StockAnalysis() {
  const { symbol } = useParams();
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/stocks/${symbol}/analysis/`)
      .then(response => {
        setAnalysis(response.data);
      })
      .catch(error => {
        console.error('Error fetching stock analysis:', error);
      });
  }, [symbol]);

  if (!analysis) return <div className="loading">Loading...</div>;

  return (
    <div className="container">
      <h1 className="heading">{analysis.stock.name} ({analysis.stock.symbol}) - Stock Analysis</h1>
      <div className="analysis-container">
        <div className="analysis-item">
          <strong>Average Closing Price:</strong> {analysis.average_close.toFixed(2)}
        </div>
        <div className="analysis-item">
          <strong>Highest Closing Price:</strong> {analysis.highest_close.toFixed(2)}
        </div>
        <div className="analysis-item">
          <strong>Lowest Closing Price:</strong> {analysis.lowest_close.toFixed(2)}
        </div>
        <div className="analysis-item">
          <strong>Average Volume:</strong> {analysis.average_volume.toFixed(0)}
        </div>
      </div>
    </div>
  );
}

export default StockAnalysis;

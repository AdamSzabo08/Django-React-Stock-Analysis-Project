// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import StockList from './StockList';
import StockDetail from './StockDetail';
import StockAnalysis from './StockAnalysis';
import './App.css';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <Link to="/" className="home-button">Home</Link>
        </nav>
        <Routes>
          <Route path="/" element={<StockList />} />
          <Route path="/stocks/:symbol" element={<StockDetail />} />
          <Route path="/stocks/:symbol/analysis" element={<StockAnalysis />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

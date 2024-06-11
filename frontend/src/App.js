
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import StockList from './StockList';
import StockDetail from './StockDetail';
import StockAnalysis from './StockAnalysis';
import AddStock from './AddStock';
import './App.css';

function App() {
  return (
    <Router>
      <div>
      <nav>
        <Link to="/" className="home-button">Home</Link>
        <Link to="/add_stock" className="add-stock-button">Add Stock</Link>  {/* New link for adding stock */}
      </nav>
      <Routes>
        <Route path="/" element={<StockList />} />
        <Route path="/stocks/:symbol" element={<StockDetail />} />
        <Route path="/stocks/:symbol/analysis" element={<StockAnalysis />} />
        <Route path="/add_stock" element={<AddStock />} />  {/* New route for adding stock */}
      </Routes>
      </div>
    </Router>
  );
}

export default App;

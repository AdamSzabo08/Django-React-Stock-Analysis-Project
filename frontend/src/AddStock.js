import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function AddStock() {
  const [symbol, setSymbol] = useState('');
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.post('http://localhost:8000/add_stock/', { symbol, name })
      .then(response => {
        setMessage('Stock added successfully');
      })
      .catch(error => {
        setMessage('Error adding stock: ' + error.response.data.error);
      });
  };

  return (
    <div className="container">
      <h1 className="heading">Add Stock</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Symbol:</label>
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="submit-button">Add Stock</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default AddStock;

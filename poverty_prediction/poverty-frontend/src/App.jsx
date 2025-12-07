import { useState } from "react";
import { getPrediction } from "./api";
import React, { useState } from 'react';
import './App.css';
import { barangays } from './data/barangays';

function App() {
  // Form state
  const [selectedBarangay, setSelectedBarangay] = useState(barangays[0] || "");
  const [population, setPopulation] = useState('16700');
  const [unemployment, setUnemployment] = useState('7.5');
  const [income, setIncome] = useState('16500');
  
  // Prediction state
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
  setLoading(true);
  
  try {
    const response = await fetch('https://poverty-backend-production.up.railway.app/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    population: parseInt(population),
    average_income: parseFloat(income),
    unemployment_rate: parseFloat(unemployment)
  })
});

    
    const data = await response.json();
    
    if (response.ok) {
      setPrediction({
        rate: data.prediction.toFixed(2) + '%',
        risk: data.risk_level
      });
    } else {
      console.error('Error from API:', data.error);
      setPrediction({ rate: 'Error', risk: 'Could not get prediction' });
    }
  } catch (error) {
    console.error('Error:', error);
    setPrediction({ rate: 'Error', risk: 'Network error' });
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="container">
      <header className="header">
        <h1>POVERTY PREDICTION</h1>
        <p>Cagayan de Oro City</p>
      </header>

      <div className="stats-container">
        <div className="card">
          <h3>Avg Poverty Rate</h3><h2>31.2%</h2>
        </div>
        <div className="card">
          <h3>Total Population</h3><h2>612k</h2>
        </div>
        <div className="card">
          <h3>High-Risk Areas</h3><h2>12</h2>
        </div>
      </div>

      <div className="prediction-box">
        <h3>POVERTY RATE PREDICTION</h3>

        <div className="form-grid">
          <div className="input-group">
            <label>Select Barangay:</label>
            <select
              value={selectedBarangay}
              onChange={(e) => setSelectedBarangay(e.target.value)}
            >
              {barangays.map((b) => (
                <option key={b} value={b}>{b}</option>
              ))}
            </select>
          </div>

          <div className="input-group">
            <label>Population:</label>
            <input
              type="number"
              value={population}
              onChange={(e) => setPopulation(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Unemployment Rate (%):</label>
            <input
              type="number"
              step="0.1"
              value={unemployment}
              onChange={(e) => setUnemployment(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Average Income (PHP):</label>
            <input
              type="number"
              value={income}
              onChange={(e) => setIncome(e.target.value)}
            />
          </div>
        </div>

        <button className="predict-btn" onClick={handlePredict} disabled={loading}>
          {loading ? "Calculating..." : "Predict Poverty Rate"}
        </button>

        {prediction && (
          <div className="result-area">
            <h4>Predicted Poverty Rate: {prediction.rate}</h4>
            <p className={`risk-${prediction.risk.toLowerCase().replace(' risk area', '')}`}>
              {prediction.risk}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

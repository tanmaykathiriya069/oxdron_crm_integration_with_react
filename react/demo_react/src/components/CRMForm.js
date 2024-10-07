import React, { useState } from 'react';
import './styles.css';

const CRMForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8069/api/crm/create', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer 8695d545367146260b18bdd91eae6b928c44566c',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, phone })
      });

      const result = await response.json();

      if (result.success) {
        alert('CRM record created successfully!');
        setName('');
        setEmail('');
        setPhone('');
      } else {
        setError(result.error);
      }
    } catch (error) {
      console.error('There was an error creating the CRM record!', error);
      setError('There was an error creating the CRM record.');
    }
  };

  return (
    <div className="form-container">
      <form className="crm-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="phone">Phone:</label>
          <input
            id="phone"
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="submit-btn">Submit</button>
        {error && <p className="error-message">{error}</p>}
      </form>
    </div>
  );
};

export default CRMForm;

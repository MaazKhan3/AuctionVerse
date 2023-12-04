import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserTransactions = () => {
  const [userTransactions, setUserTransactions] = useState([]);

  useEffect(() => {
    // Fetch user's transactions from your backend API
    axios.get('http://your-backend-api-url/user_transactions')
      .then(response => setUserTransactions(response.data))
      .catch(error => console.error('Error fetching user transactions:', error));
  }, []);

  return (
    <div>
      <h2>Your Transactions</h2>
      {/* Render user's transactions here */}
    </div>
  );
};

export default UserTransactions;

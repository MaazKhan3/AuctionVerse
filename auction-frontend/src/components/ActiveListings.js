import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ActiveListings = () => {
  const [activeListings, setActiveListings] = useState([]);

  useEffect(() => {
    // Fetch active listings from your backend API
    axios.get('http://your-backend-api-url/active_listings')
      .then(response => setActiveListings(response.data))
      .catch(error => console.error('Error fetching active listings:', error));
  }, []);

  return (
    <div>
      <h2>Active Listings</h2>
      {/* Render active listings here */}
    </div>
  );
};

export default ActiveListings;

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserBids = () => {
  const [userBids, setUserBids] = useState([]);

  useEffect(() => {
    // Fetch user's bids from your backend API
    axios.get('http://your-backend-api-url/user_bids')
      .then(response => setUserBids(response.data))
      .catch(error => console.error('Error fetching user bids:', error));
  }, []);

  return (
    <div>
      <h2>Your Bids</h2>
      {/* Render user's bids here */}
    </div>
  );
};

export default UserBids;

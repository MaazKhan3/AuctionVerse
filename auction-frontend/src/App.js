import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import ActiveListings from './components/ActiveListings';
import ListingDetail from './components/ListingDetail';
import PlaceBid from './components/PlaceBid';
import UserBids from './components/UserBids';
import UserTransactions from './components/UserTransactions';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li><Link to="/active_listings">Active Listings</Link></li>
            <li><Link to="/user_bids">Your Bids</Link></li>
            <li><Link to="/user_transactions">Your Transactions</Link></li>
          </ul>
        </nav>

        <Switch>
          <Route path="/active_listings" component={ActiveListings} />
          <Route path="/listing/:id" component={ListingDetail} />
          <Route path="/place_bid/:id" component={PlaceBid} />
          <Route path="/user_bids" component={UserBids} />
          <Route path="/user_transactions" component={UserTransactions} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;

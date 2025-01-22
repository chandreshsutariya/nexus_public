import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import HomeScreen from './pages/HomeScreen';
import RestaurantListScreen from './pages/RestaurantListScreen';
import UserProfile from './pages/UserProfile';
import OrderHistory from './pages/OrderHistory';
import Cart from './pages/Cart';
import NotFound from './pages/NotFound';

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={HomeScreen} />
        <Route path="/restaurants" component={RestaurantListScreen} />
        <Route path="/profile" component={UserProfile} />
        <Route path="/orders" component={OrderHistory} />
        <Route path="/cart" component={Cart} />
        <Route component={NotFound} />
      </Switch>
    </Router>
  );
};

export default App;

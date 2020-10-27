import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.css';

import Home from './components/Home';
import Leaderboard from './components/Leaderboard';
import Navigation from './components/Navigation';

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          <Navigation />
            <Switch>
            <Route path="/" component={Home} exact/>
            <Route path="/leaderboard" component={Leaderboard}/>
            </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;

import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.scss';

import LogIn from './components/LogIn';
import Home from './components/Home';
import Quiz from './components/Quiz';
import Leaderboard from './components/Leaderboard';
import Navigation from './components/Navigation';

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          <Navigation />
            <Switch>
            <Route path="/" component={LogIn} exact/>
            <Route path="/dashboard" component={Home}/>
            <Route path="/quiz" component={Quiz}/>
            <Route path="/leaderboard" component={Leaderboard}/>
            </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;

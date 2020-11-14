import React, { Component } from 'react';
import { BrowserRouter, Redirect, Route, Switch } from 'react-router-dom';
import './App.scss';

import LogIn from './components/LogIn';
import Home from './components/Home';
import Quiz from './components/Quiz';
import Leaderboard from './components/Leaderboard';
import Navigation from './components/Navigation';
import History from './components/History';


const RequireAuth = ({children}) => {
  console.log("local storage token is: ")
  console.log(localStorage.getItem("token"))

  if(localStorage.getItem("token") !== 3) {
    console.log("Not Logged in, redirecting...");
    History.push('/');
    return <Redirect to="/" exact/>;
  } else {
    console.log("Logged In, going to original destination");
    return children;
  }
}

class App extends Component {
  
  render() {

    return (
      <BrowserRouter history={History}>
        <div>
          <Navigation />
            <Switch>
            <Route path="/" component={LogIn} exact/>

            <RequireAuth>
              <Route path="/dashboard" component={Home}/>
              <Route path="/quiz" component={Quiz}/>
              <Route path="/leaderboard" component={Leaderboard}/>
              </RequireAuth>
            </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;

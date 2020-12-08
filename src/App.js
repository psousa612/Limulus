import React, { Component } from 'react';
import { Router, Redirect, Route, Switch } from 'react-router-dom';
import './App.scss';

import LogIn from './components/LogIn';
import SignUp from './components/SignUp';
import Home from './components/Home';
import Quiz from './components/Quiz';
import Leaderboard from './components/Leaderboard';
import Navigation from './components/Navigation';
import History from './components/History';
import Profile from './components/Profile';
import FindFriends from './components/FindFriends';
import AddQuestion from './components/AddQuestion';

const RequireAuth = ({children}) => {
  if(localStorage.getItem("token") === null) {
    console.log("Not Logged in, redirecting...");
    console.log(children)
    return <Redirect to="/" exact/>;
  } else {
    console.log("Logged In, going to original destination");
    return children;
  }
}

class App extends Component {
  
  render() {

    return (
      <Router history={History} forceRefresh={true}>
        <div>
          <Navigation />
            <Switch>
                <Route path="/" component={LogIn} exact/>
                <Route path="/signup" component={SignUp}/>
              <RequireAuth>
                <Route path="/dashboard" component={Home}/>
                <Route path="/quiz" component={Quiz}/>
                <Route path="/leaderboard" component={Leaderboard}/>
                <Route path="/profile" component={Profile}/>
                <Route path="/findfriends" component={FindFriends}/>
                <Route path="/addquestion" component={AddQuestion}/>
              </RequireAuth>
            </Switch>
        </div>
      </Router>
    );
  }
}

export default App;

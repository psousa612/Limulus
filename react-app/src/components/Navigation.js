import React from 'react';
import { NavLink } from 'react-router-dom';
import History from './History'
import './navigation.scss';

function logOut() {
  console.log("logggggin out ")
  localStorage.clear();
  History.push("/");
  window.location.reload()
}

const IsLoggedIn = ({children}) => {
  if (localStorage.getItem("token") === null) {
    return <div>
      <ul>
        <li><NavLink to="/" exact>LogIn</NavLink></li>
        <li><NavLink to="/signup">SignUp</NavLink></li>
      </ul>
    </div>
  } else {
    return children
  }
}

const Navigation = () => {


  return (
    <div class="navbar">
      <ul>
      <IsLoggedIn>
          <li><NavLink to="/dashboard" class="navlink">Dashboard</NavLink></li>
          <li><NavLink to="/leaderboard" class="navlink">Leaderboard</NavLink></li>
          <li><NavLink to="/findfriends" class="navlink">Find Friends</NavLink></li>
          <li><NavLink to="/addquestion" class="navlink">Add Question</NavLink></li>
          <li class="right-align"><NavLink to="/profile" class="navlink">Profile</NavLink></li>
          <li class="right-align"><a onClick={logOut} href="a">Log Out</a></li>
      </IsLoggedIn>
      </ul>
    </div>
  );
}

export default Navigation;

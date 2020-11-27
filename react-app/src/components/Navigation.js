import React from 'react';
import { NavLink } from 'react-router-dom';
import History from './History'
import './navigation.scss';

function logOut() {
  console.log("logggggin out ")
  localStorage.clear();
  History.push("/");
}

const Navigation = () => {
  return (
    <div class="navbar">
      <ul>
      {/* <li><NavLink to="/" class="navlink">Login/SignUp</NavLink></li> */}
      <li><NavLink to="/dashboard" class="navlink">Dashboard</NavLink></li>
      <li><NavLink to="/leaderboard" class="navlink">Leaderboard</NavLink></li>
      <li><NavLink to="/profile" class="navlink">Profile</NavLink></li>
      <li><NavLink to="/findfriends" class="navlink">Find Friends</NavLink></li>
      <li><button onClick={logOut}>Log Out</button></li>
      </ul>
    </div>
  );
}

export default Navigation;

import React from 'react';
import { NavLink } from 'react-router-dom';
import './navigation.scss';

const Navigation = () => {
  return (
    <div class="navbar">
      <ul>
      <li><NavLink to="/" class="navlink">Home</NavLink></li>
      <li><NavLink to="/leaderboard" class="navlink">Leaderboard</NavLink></li>
      <li><NavLink to="/leaderboard" class="profile-pic">Leaderboard</NavLink></li>

      </ul>
    </div>
  );
}

export default Navigation;

import React, { useState } from 'react';
import {leaders} from './../api/leaderboard';
import './style.scss';
import './leaderboard.scss';

import RowItem from './RowItem';

const Leaderboard = () => {
  const [leader, setLeader] = useState({})

  function getLeaders() {
    leaders().then((l) => {
      setLeader(l);
    })
  }

  return (
    <div class="panel" onLoad={getLeaders()}>
      <h1> Leaderboard </h1>
      
      <table>
        <thead>
        <tr>
          <th>Ranking</th>
          <th>Username</th>
          <th>Points</th>
        </tr>
      </thead>
        {/* how to loop through leader and display data in a RowItem */}
        {  
        
        }
      <tbody>
        
      </tbody>

      </table>
      
    </div>
  );
}

export default Leaderboard;

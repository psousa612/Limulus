import React, { useEffect, useState } from 'react';
import {leaders} from './../api/leaderboard';
import './style.scss';
import './leaderboard.scss';

import RowItem from './RowItem';

const Leaderboard = () => {
  const [leader, setLeader] = useState({})

  useEffect( () => {
    leaders().then((l) => {
      setLeader(l);
    })
  }, []);

  return (
    <div class="panel">
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
          Object.keys(leader).map((value, index) => {
            return <RowItem info={leader[value]} key={index} />
          })

        }
      <tbody>
        
      </tbody>

      </table>
      
    </div>
  );
}

export default Leaderboard;

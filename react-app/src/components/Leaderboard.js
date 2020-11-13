import React from 'react';
import {leaders} from './../api/leaderboard';
import './style.scss';
import './leaderboard.scss';

import RowItem from './RowItem';

const Leaderboard = () => {
  const l = leaders()
  // console.log(leaders)
  // const rows = []
  // for (leader in leaders) {
  //   rows.push(<RowItem ranking={leader[0]} />)
  // }

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

      <tbody>
        {console.log(l)}
      </tbody>

      </table>
      
    </div>
  );
}

export default Leaderboard;

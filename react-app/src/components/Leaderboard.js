import React from 'react';
import './style.scss';
import './leaderboard.scss';

import RowItem from './RowItem';

const Leaderboard = () => {
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
        {/*Put the api call and create row items for each leaderboard row*/}
      <RowItem ranking="1" username="yash" points="300"/>
      <RowItem ranking="2" username="bob" points="299"/>
      </tbody>

      </table>
      
    </div>
  );
}

export default Leaderboard;

import React, { useEffect, useState } from 'react';
import {leaders} from './../api/leaderboard';
// import './style.scss';
// import './leaderboard.scss';

import RowItem from './RowItem';

const Leaderboard = () => {
  const [leader, setLeader] = useState({})
  const [topFriend, setTopFriend] = useState([]);
  const [toughestQuestion, setToughestQuestion] = useState("")

  useEffect( () => {
    leaders(localStorage.getItem("username")).then((l) => {
      setLeader(l["leaderboard"]);
      setTopFriend(l["topfriends"])
      setToughestQuestion(l["toughestquestion"])
      // console.log(toughestQuestion)
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
      <tbody>
        {/* how to loop through leader and display data in a RowItem */}
        {
          Object.keys(leader).map((value, index) => {
            return <RowItem info={leader[value]} key={index} />
          })

        }
      
        
      </tbody>

      </table>

      <br/>

      <h1>Friend Rankings</h1>

      {
        topFriend.length !== 0 ? 
        <table>
          <thead>
            <th>Ranking</th>
            <th>Username</th>
            <th>Points</th>
          </thead>

          <tbody>
            { 
            topFriend.map((value, index) => {
              return <tr>
                <td>{value[0]}</td>
                <td>{value[2]}</td>
                <td>{value[3]}</td>
              </tr>
            })
          }
            </tbody>
        </table>
        : <div>
            <p>You have no friends!</p>
            <a href="/findfriends">Make some here!</a>
          </div>
      }

      
    </div>
  );
}

export default Leaderboard;

import React, { useEffect, useState } from 'react';
import {categories} from '../api/questions';
import './style.scss';

const Home = () => {
  const [cats, setCats] = useState({})

  useEffect( () => {
    categories().then((l) => {
      setCats(l);
    })
  }, []);

  return (
    <div class="panel">
      <h1> home </h1>
      <h2>take da quiz</h2>
      
      <select class="category-selector">
        {
          Object.keys(cats).map((index) => {
          return <option value={cats[index]} key={index}>{cats[index][0].toString()}</option>
          })
        }

        {/* <option value="?">cs</option>
        <option value="?">meth</option>
        <option value="?">sceience</option> */}

      </select>

      <a href="/quiz">start da quiz</a>


    </div>
  );
}

export default Home;

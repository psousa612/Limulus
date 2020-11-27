import React, { useEffect, useState } from 'react';
import History from './History';
import {getCategories} from '../api/questions';
import './style.scss';

const Home = () => {
  const [cats, setCats] = useState({})
  
  function changeSelection(e) {
    // console.log(e.target.value);
    localStorage.setItem("cat", e.target.value);
  }

  function startQuiz() {
    console.log(localStorage.getItem("cat"))
    History.push("/quiz")
  }

  useEffect( () => {
    getCategories().then((l) => {
      setCats(l);
      localStorage.setItem("cat", l[0])
    })
  }, []);

  return (
    <div class="panel">
      <h1> home </h1>
      <h2>take da quiz</h2>
      
      <select class="category-selector" onChange={changeSelection}>
        {
          Object.keys(cats).map((value, index) => {
            return <option key={index}>{cats[value]}</option>
          })
        }
      </select>

      <button onClick={startQuiz}>take da quiz</button>


    </div>
  );
}

export default Home;

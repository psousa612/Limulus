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
    // console.log(localStorage.getItem("cat"))
    History.push("/quiz")
  }



  useEffect( () => {
    if(localStorage.getItem("refreshed") == null) {
      localStorage.setItem("refreshed", true);
      window.location.reload()
      return;
    }

    getCategories().then((l) => {
      
      setCats(l);
      localStorage.setItem("cat", l[0])
    })
  }, []);

  return (
    <div class="panel">
      <h1> Dashboard </h1>
      <h2>Quiz Set-Up</h2>
      
      <select class="category-selector" onChange={changeSelection}>
        {
          Object.keys(cats).map((value, index) => {
            return <option key={index}>{cats[value]}</option>
          })
        }
      </select>
      <br/>

      
      <button onClick={startQuiz}>Start Quiz</button>
    </div>
  );
}

export default Home;

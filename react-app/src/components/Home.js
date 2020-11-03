import React from 'react';
import './style.scss';

const Home = () => {
  return (
    <div class="panel">
      <h1> home </h1>
      <h2>take da quiz</h2>
      
      <select class="category-selector">
        <option value="?">cs</option>
        <option value="?">meth</option>
        <option value="?">sceience</option>

      </select>

      <a href="/quiz">start da quiz</a>


    </div>
  );
}

export default Home;

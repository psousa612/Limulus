import React from 'react';
import './style.scss';
import './quiz.scss';



const Quiz = () => {
    var nums = [1, 2, 3, 4];
    var i = 1;
    
    const buttons = [];
    for (var num in nums) {
        buttons.push(<button onClick={handleClick}>{num}</button>);
    }

    function handleClick(e) {
        console.log("button pressed");
        buttons[2] = <button onClick={handleClick}>999999</button>;
        i++;
    }

    return (
        <div class="panel">

            <h1>yar this do be the quiz page</h1>
            
            <p>question {i}</p>

            <div class="button-grid">
            {buttons}

            </div>

        </div>
    );
}

export default Quiz;
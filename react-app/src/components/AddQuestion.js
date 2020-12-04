import React from 'react';
import History from './History';
import {pushNewQuestion} from '../api/questions';

const addQuestion = () => {
    
    function handleSubmit(e) {
        e.preventDefault()
        
        let info = []
        for (var i = 0; i < 6; i++) {
            info.push(e.target[i].value)
        }

        pushNewQuestion(info, localStorage.getItem("username"))
            .then((data) => {
                console.log(data)
                History.push("/dashboard")
            })
    }

    return (
        <div class="panel">
            <form onSubmit={handleSubmit}>
                <label for="cat">Category: </label>
                <input id="cat" required></input>
                
                <br/>
                <label for="prompt">Question: </label>
                <input id="prompt" required></input>
                <br/>
                <label for="correct">Correct Answer: </label>
                <input id="correct" required></input>
                <br/>
                <label for="wrong1">Wrong Answer 1: </label>
                <input id="wrong1" required></input>
                <br/>
                <label for="wrong2">Wrong Answer 2: </label>
                <input id="wrong2" required></input>
                <br/>
                <label for="wrong3">Wrong Answer 3: </label>
                <input id="wrong3" required></input>
                <br/>

                <input type="submit"></input>
            </form>
        </div>
    );
}

export default addQuestion;
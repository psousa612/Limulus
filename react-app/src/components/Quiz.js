import React, { useEffect, useState } from 'react';
import {getQuestion} from '../api/questions';
import './style.scss';
import './quiz.scss';



const Quiz = () => {
    const [questionData, setQuestionData] = useState({})
    const [correctResponse, setCorrectResponse] = useState('')
    const [buttons, setButtons] = useState([])
    const [disabled, setDisabled] = useState("")
    const [prompt, setPrompt] = useState('')

    useEffect(() => {
        nextQuestion();
    }, []);

    function nextQuestion() {
        //Call the api to get the next question data
        getQuestion().then((data) => {
            // console.log(data)
            setQuestionData(data)
            setDisabled("false")
            //Populate the fields with the next question info
            let scrubbedPrompt = data["prompt"][2].replace(/&quot;/g, '\\"')

            setPrompt(scrubbedPrompt)
            var buts = []
            for (const row of data["responses"]) {
                let scrubbedBut = row[1].replace(/&quot;/g, '\\"')
                buts.push(<button onClick={handleClick} disabled={disabled} key={scrubbedBut}>{scrubbedBut}</button>)

                if(row[2]) {
                    setCorrectResponse(scrubbedBut)
                }
            }
            setButtons(buts)
        });
    }
    // buttons.map((value) => {
    //     return <button onClick={handleClick}>{value}</button>
    // })

    function handleClick(e) {
        console.log(e.target.innerHTML)
        if(e.target.innerHTML === correctResponse) {
            console.log("Correct!")
        } else {
            console.log("Wrong!")
        }

        setDisabled("true")
    }

    return (
        <div class="panel">

            <h2>yar this do be the quiz page</h2>
            <h1>{prompt}</h1>
            

            <div class="button-grid">
                {buttons}
            </div>

        </div>
    );
}

export default Quiz;
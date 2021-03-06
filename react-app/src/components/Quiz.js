import React, { useEffect, useState } from 'react';
import {getQuestion, answeredQuestion, getQuestionStats} from '../api/questions';
import './style.scss';
import './quiz.scss';



const Quiz = () => {
    // eslint-disable-next-line no-unused-vars
    const [questionData, setQuestionData] = useState({})
    const [correctResponse, setCorrectResponse] = useState("")
    const [buttons, setButtons] = useState([])
    const [disabled, setDisabled] = useState("")
    const [prompt, setPrompt] = useState('')
    const [resultText, setResultText] = useState("")
    const [pointsText, setPointsText] = useState("")
    const [questionStats, setQuestionStats] = useState([])

    var currQkey;
    let statsHeaders = ["Question Key", "Total Answers", "Total Correct Answers", "Total First Tries"]
    useEffect(() => {
        nextQuestion()        
    }, []);

    async function nextQuestion() {
        //Call the api to get the next question data
        getQuestion().then((data) => {
            //Populate internal variables for later use
            setQuestionData(data)
            currQkey = data["prompt"][0]
            setDisabled(false)

            //Populate the fields with the next question info
            let scrubbedPrompt = data["prompt"][2].replace(/&quot;/g, '"')
            scrubbedPrompt = scrubbedPrompt.replace(/&#039;/g, "'")
            
            setPrompt(scrubbedPrompt)
            var buts = []
            for (const row of data["responses"]) {
                let scrubbedBut = row[1].replace(/&quot;/g, '\\"')
                scrubbedBut = scrubbedBut.replace(/&#039;/g, '\\"')
                // buts.push(<button onClick={handleClick} disabled={disabled} key={scrubbedBut}>{scrubbedBut}</button>)
                buts.push(scrubbedBut);
                
                if(row[2]) {
                    // console.log("true!")
                    setCorrectResponse(scrubbedBut);
                    // console.log("Correct Response is: ", scrubbedBut)
                }
            }
            setButtons(buts)
        })
    }



    function handleClick(e) {
        let correct = false;
        if(e.target.innerHTML === correctResponse) {
            setResultText("Correct!")
            correct = true;
        } else {
            setResultText("Wrong!")
            correct = false;
        }

        let uname = localStorage.getItem("username")
        answeredQuestion(uname, questionData["prompt"][0], correct)
            .then((data) => {
                setPointsText(data)
            }).then(() => {
                getQuestionStats(questionData["prompt"][0]).then((data) => {
                    let statsData = []
                    statsData.push(data["question_key"])
                    statsData.push(data["total_amt"])
                    statsData.push(data["total_correct"])
                    statsData.push(data["total_first_try_correct"])
        
                    setQuestionStats(statsData)
                })
            })

        setDisabled(true)
    }

    return (
        <div class="panel">
            <h2>Quiz</h2>
            <h1>{prompt}</h1>
            

            <div class="button-grid">
                {/* {buttons} */}
                {
                    buttons.map((value) => {
                        return <button onClick={handleClick} disabled={disabled} key={value}>{value}</button>
                    })
                }
            </div>
            
            <div hidden={!disabled}>
                <br/>
                {<p>{resultText}</p>}
                {resultText === "Wrong!" ? 
                    <p> Correct Answer: {correctResponse}</p>
                    : null
                }

                {<p>You have {pointsText} points.</p>}

                <button onClick={nextQuestion}>Next Question</button>
                <br/>
                
                <h2>Statistics For This Question</h2>
                <table class="question-stats">
                <tbody>
                    {
                        questionStats.map((value, index) => {
                        return <tr key={index}><td class="td-header">{statsHeaders[index]}:</td><td class="td-value">{value}</td></tr>
                        })
                    }
                    {
                        <tr key={questionStats.length}><td class="td-header">Total Wrong Answers</td><td class="td-value">{questionStats[1]-questionStats[2]}</td></tr>
                    }
                </tbody>
                </table>
            </div>
        </div>
    );
}

export default Quiz;
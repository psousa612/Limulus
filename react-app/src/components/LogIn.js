import React, {useState} from 'react';
import {login} from './../api/login';
import History from './History';
import './style.scss';

const LogIn = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    function handleSubmit(event) {
        event.preventDefault()
        
        //Call the login api
        login(username, password).then((data) => {
            console.log(data)
            if(data["response"] === 200) {
                console.log("log in good!")
                localStorage.setItem("token", 3)
                localStorage.setItem("username", username)
                History.push('/dashboard')
            } else {
                console.log("log in bad :(")
                alert("Invalid Login! Try Again.")
            }
        })
    }

    return (
        <div>
            <div class="panel">
                <form onSubmit={handleSubmit}>
                    Username:
                    <input type="text" onChange={e => setUsername(e.target.value)}></input>

                    <br></br>
                    Password: 
                    <input type="password" onChange={e => setPassword(e.target.value)}></input>

                    <br></br>
                    <input type="submit"></input>
                </form>
            </div>
        </div>
    );
}

export default LogIn;
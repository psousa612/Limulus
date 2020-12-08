import React, {useState} from 'react';
import {login} from './../api/login';
import History from './History';
import './style.scss';

const LogIn = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    function handleSubmit(event) {
        event.preventDefault()
        
        if(username === "" || password === "") {
            return;
        }

        //Call the login api
        login(username, password).then((data) => {
            console.log(data)
            if(data["error"] === null) {
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
                <h1>Log In</h1>
                <form onSubmit={handleSubmit}>
                    <label for="uname">Username: </label>
                    <input type="text" id="uname" autocomplete="off" onChange={e => setUsername(e.target.value)}></input>

                    <label for="password">Password: </label>
                    <input type="password" id="password" autocomplete="off" onChange={e => setPassword(e.target.value)}></input>

                    <button type="submit">Submit</button>
                </form>
            </div>
        </div>
    );
}

export default LogIn;
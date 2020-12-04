import React from 'react';
import { signup } from '../api/login';
import History from './History';

const SignUp = () => {
    function handleSubmit(e) {
        e.preventDefault()
        let info = []
        for(var i = 0; i < 8; i++) {
            if(e.target[i].value === "") {
                info.push(null)
            } else {
                info.push(e.target[i].value)
            }
        }

        // console.log(info)
        signup(info).then(
            History.push("/")
        )
    }

    return (
        <div class="panel">
            <h2>Sign Up</h2>
            <form onSubmit={handleSubmit}>
                <label for="username">Username: </label>
                <input id="username" required></input>
                <br/>
                <label for="password" type="password">Password: </label>
                <input id="password" required></input>
                <br/>
                <label for="email" type="email">Email: </label>
                <input id="email" required></input>
                <br/>
                <h3>Optional Fields:</h3>
                <label for="firstname">First Name: </label>
                <input id="firstname"></input>
                <br/>
                <label for="lastname">Last Name: </label>
                <input id="lastname"></input>
                <br/>
                <label for="age">Age: </label>
                <input id="age"></input>
                <br/>
                <label for="location">Location: </label>
                <input id="location"></input>
                <br/>
                <label for="school">School: </label>
                <input id="school"></input>
                <br/>

                <input type="submit"/>
            </form>
        </div>
    )
}

export default SignUp;


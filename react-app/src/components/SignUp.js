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
            <h1>Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <label for="username">Username: </label>
                <input id="username" type="text" autocomplete="off" required></input>
                
                <label for="password" >Password: </label>
                <input id="password" type="password" autocomplete="off" required></input>
                
                <label for="email" >Email: </label>
                <input id="email" type="email" autocomplete="off" required></input>
                
                <h3>Optional Fields:</h3>
                <label for="firstname">First Name: </label>
                <input id="firstname" type="text" autocomplete="off"></input>
          
                <label for="lastname">Last Name: </label>
                <input id="lastname" type="text" autocomplete="off"></input>
     
                <label for="age">Age: </label>
                <input id="age" type="text" autocomplete="off"></input>
           
                <label for="location">Location: </label>
                <input id="location" type="text" autocomplete="off"></input>
            
                <label for="school">School: </label>
                <input id="school" type="text" autocomplete="off"></input>

                <button type="submit">Submit</button>
            </form>
        </div>
    )
}

export default SignUp;


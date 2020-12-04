import React, { useEffect, useState } from 'react';
import {getUserInfo, getUserHistory, getFriends, removeFriend} from '../api/user';
import './style.scss';

const Profile = () => {
    const [info, setInfo] = useState([])
    const [showHistory, setShowHistory] = useState(false)
    const [history, setHistory] = useState([])
    const [showFriends, setShowFriends] = useState(false)
    const [friends, setFriends] = useState([])

    let infoHeaders = ["User Key", "First Name", "Last Name", "Age", "Location", "School", "Points"]
    

    useEffect(() => {
        let uname = localStorage.getItem("username")
        getUserInfo(uname).then((data) => {
            setInfo(data);
        })

        getUserHistory(uname).then((data) => {
            setHistory(data)
        })

        getFriends(uname).then((data) => {
            setFriends(data)
        })
        
    }, [])

    function handleUnfriend(e) {
        removeFriend(info[0], friends[e.target.id][0]).then(() => {
            getFriends(localStorage.getItem("username")).then((data) => {
                setFriends(data)
            })
        })
    }

    function toggleShowHistory(e) {
        setShowHistory(!showHistory)
    }

    function toggleShowFriends(e) {
        setShowFriends(!showFriends)
    }

    return (
        <div class="panel">
            <h2>User Info</h2>
            {
                info.map((value, index) => {
                    return <div><h3>{infoHeaders[index]}</h3><p>{value}</p></div>
                })
            }

            <br/>
            <button onClick={toggleShowHistory}>{showHistory ? "Hide Question History" :  "Show Question History"}</button>
            <button onClick={toggleShowFriends}>{showFriends ? "Hide Friends List" :  "Show Friends List"}</button>
            <br/>

            { showHistory ? 
            <table>
                <thead>
                    <th>qKey</th>
                    <th>Prompt</th>
                </thead>

                <tbody>
                    {history.map((value, index) => {
                        let scrubbedPrompt = value[1].replace(/&quot;/g, '\\"')
                        scrubbedPrompt = value[1].replace(/&#039;/g, '\\"')
                        return <tr key={index}><td>{value[0]}</td><td>{scrubbedPrompt}</td></tr>
                    })}
                </tbody>
            </table> : null
            }

            { showFriends ?
            
            <table>
                <thead>
                    <th>uKey</th>
                    <th>Username</th>
                </thead>

                <tbody>
                    {friends.map((value, index) => {
                        return <tr key={index}><td>{value[0]}</td><td>{value[1]}</td><td><button onClick={handleUnfriend} id={index}>Remove Friend</button></td>  </tr>
                    })
                    }
                </tbody>
            </table> : null
            }
            
            
        </div>
    );
}

export default Profile;
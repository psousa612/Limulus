import React, { useEffect, useState } from 'react';
import { addFriend, getUserList } from '../api/user';

const FindFriends = () => {
    const [userList, setUserList] = useState([])

    useEffect( () => {
        updateList()
    }, [])

    function handleClick(e) {
        addFriend(localStorage.getItem("username"), userList[e.target.id][0])
            .then(updateList())
    }

    function updateList() {
        getUserList(localStorage.getItem("username")).then((data) => {
            setUserList(data)
        })
    }

    return (
        <div class="panel">
            <table>
                <tr>
                    <th>User Key</th>
                    <th>Username</th>
                </tr>

                <tbody>
                    {
                        userList.map((value, index) => {
                        return <tr key={index}>
                                    <td>{value[0]}</td>
                                    <td>{value[1]}</td>
                                    <td><button onClick={handleClick} id={index}>Add Friend</button></td>  
                                </tr>
                        })
                    }
                </tbody>
            </table>

        </div>
    );
}

export default FindFriends;
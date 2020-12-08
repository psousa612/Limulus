export const getUserInfo = async (uname) => {
    var data;
    // console.log(uname);
    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"user_name":uname})
    }

    await fetch('https://limulus0.herokuapp.com/getuserinfo', requestOpts)
        .then(response => response.json())
        .then(d => data = d)

    // console.log("From API: ")
    // console.log(data)
    return data["info"];
}

export const getUserHistory = async (uname) => {
    var data;

    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"user_name":uname})
    }

    await fetch('https://limulus0.herokuapp.com/questionhistory', requestOpts)
        .then(response => response.json())
        .then(d => data = d)

    // console.log("From API: ")
    // console.log(data["history"])
    return data["history"];
}

export const getFriends = async (uname) => {
    var data;

    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"user_name":uname})
    }

    await fetch('https://limulus0.herokuapp.com/getFriends', requestOpts)
        .then(response => response.json())
        .then(d => data = d)

    // console.log("From API: ")
    // console.log(data)
    return data["friends"];
}

export const removeFriend = async (ukey, fkey) => {
    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"userkey":ukey, "friendkey":fkey})
    }

    await fetch('https://limulus0.herokuapp.com/removeFriend', requestOpts)
}

export const getUserList = async (username) => {
    var data
    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"username":username})
    }

    await fetch('https://limulus0.herokuapp.com/getNonFriends', requestOpts)
        .then(response => response.json())
        .then(d => data = d)

    // console.log("From API: ")
    // console.log(data)
    return data["users"]
}

export const addFriend = async (username, friendkey) => {

    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"username":username, "friendkey":friendkey})
    }

    await fetch('https://limulus0.herokuapp.com/addFriend', requestOpts)
        .then(response => response.json())

    // console.log("From API: ")
    // console.log(data)
    // return data["users"]
}


export const login = async(username, password) => {

    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "username": username, "password": password })
    }

    var data;
    var status;

    await fetch('https://limulus0.herokuapp.com/login', requestOpts)
        .then(response => {
            response.json();
            status = response.status;
        })
        .then(d => data = d)
    console.log(data);
    console.log(status);

    return {
        "data": data,
        "response": status
    };
}

export const signup = async(info) => {
    var data
    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "info": info })
    }

    await fetch('https://limulus0.herokuapp.com/signup', requestOpts)
        .then(response => response.json())
        .then(d => data = d)

    // console.log(data);
    // console.log(status);
    return data
}
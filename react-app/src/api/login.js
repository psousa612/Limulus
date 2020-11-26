export const login = async (username, password) => {
    
    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"username":username, "password":password})
    }

    var data;

    await fetch('/login', requestOpts)
        .then(response => response.json())
        .then(d => data = d)
    
    // console.log(data);
    return data["response"] === 200;
}
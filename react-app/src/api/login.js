export const login = async (username, password) => {
    
    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"username":username, "password":password})
    }

    var data;
    var status;

    await fetch('/login', requestOpts)
        .then(response => {
            response.json();
            status = response.status;
        })
        .then(d => data = d)
    // console.log(data);
    // console.log(status);
    return {
        "data":data,
        "response":status
    };
}
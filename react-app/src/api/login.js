export const login = (username, password) => {
    
    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"username":username, "password":password})
    }

    fetch('/login', requestOpts)
        .then(response => response.json())
        .then(data => console.log(data))
    
}
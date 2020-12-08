export const leaders = async (username) => {
    var l;

    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"username":username})
    }
    await fetch('https://limulus0.herokuapp.com/leaderboard', requestOpts)
        .then(response => response.json())
        .then(data => l = data)

    // console.log("From API: ")
    // console.log(l);
    // var board = l["leaderboard"]

    return l;
}
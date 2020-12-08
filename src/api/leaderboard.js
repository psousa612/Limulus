export const leaders = async() => {
    var l;

    await fetch('https://limulus0.herokuapp.com/leaderboard')
        .then(response => response.json())
        .then(data => l = data)

    // console.log("From API: ")
    // console.log(l);
    var board = l["leaderboard"]

    return board;
}
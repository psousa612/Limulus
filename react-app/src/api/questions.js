export const getCategories = async () => {
    var data;

    await fetch('/categories')
        .then(response => response.json())
        .then(d => data = d)

    // console.log("From the API: ")
    // console.log(data)
    // data["categories"].map((value) => {
    //     console.log(value)
    // })


    return data["categories"];
}

export const getQuestion = async () => {
    var data;

    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"category":localStorage.getItem("cat"), "username":localStorage.getItem("username")})
    }

    await fetch('/nextquestion', requestOpts)
        .then(response => response.json())
        .then(d => data = d)

    // console.log("From API: ")
    // console.log(data)
    
    
    return data["question"];
}

export const answeredQuestion = async (uname, qkey, correct,) => {
    var data;

    // console.log("--Params ")
    // console.log("uname; ", uname)
    // console.log("qkey: ", qkey)
    // console.log("correct: ", correct)
    
    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"user_name":uname, "qkey":qkey, "result":correct})
    }

    await fetch('/answeredquestion', requestOpts)
        .then(response => response.json())
        .then(d => data = d)

    // console.log("From API: ")
    // console.log(data)
    return data["points"];
}

export const getQuestionStats = async (qkey) => {
    var data;

    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"questionkey":qkey})
    }

    await fetch('/questionstats', requestOpts)
        .then(response => response.json())
        .then(d => data = d)

    // console.log("From API: ")
    // console.log(data)
    return data;
}

export const pushNewQuestion = async (info, username) => {
    var data;

    const requestOpts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"username":username, "info":info})
    }

    await fetch('/addQuestion', requestOpts)
        .then(response => response.json())
        .then(d => data = d)

    console.log("From API: ")
    console.log(data)
    return data;
}
const backendURL = 'http://127.0.0.1:5000';

//signup
function signup(){ //declares function called signup. HTML calls this
    const username = document.getElementById('signup-username').value //doc...(username') finds username input in html. .value gets the actual value
    const password = document.getElementById('signup-password').value //doc...(password') finds password input in html. .value gets the actual value

    fetch('${backendURL}/signup',{ //fetch() makes a network request. ${backendURL}/signup is the URL of flask in app.py file
    method: 'POST', //send data to server
        headers: {'Content-Type': 'application/json' }, //tells server that data is JSON type
        body: JSON.stringify({ username, password}) //turns JS object to JSON so flask in app.py can read
    })
    .then(res => res.json()) //if backend responds .then gets that response and .json() turns it into JS so this can read it
    .then(data => alert(data.message || data.error)); //now data has what flask returned. Either "User created" or "User alr exists"
}

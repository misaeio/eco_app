const backendURL = "http://127.0.0.1:5000"; //base URL for backend api

// SIGNUP
function signup() {
    const username = document.getElementById('signup-username').value; //gets values from html form
    const password = document.getElementById('signup-password').value;

    fetch(`${backendURL}/signup`, { //send POST request to flask backend at /signup
        method: 'POST', //POST bc we are sending info
        headers: { 'Content-Type': 'application/json' }, //tells server this is JSON data
        body: JSON.stringify({ username, password }) //converts user n pass to JSON
    })
    .then(res => res.json()) //backend response to javascript object
    .then(data => {
        if (data.message) { //if signup is successful display success message 
            alert(data.message);
            // Redirect with username and user_id
            window.location.href = "dashboard.html?user_id=" + data.user_id + "&username=" + encodeURIComponent(username); 
        } else {
            alert(data.error);
        }
    });
}

// LOGIN
function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    fetch(`${backendURL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location.href = "dashboard.html?user_id=" + data.user_id + "&username=" + encodeURIComponent(data.username);
        } else {
            alert(data.error);
        }
    });
}

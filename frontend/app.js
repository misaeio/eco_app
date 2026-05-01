const backendURL = "http://127.0.0.1:5000";
const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//Welcome message about a fact 
 const ecoFacts = [
    "Recycling one aluminum can saves enough energy to run a TV for 3 hours.",
    "About 8 million tons of plastic enter the ocean each year.",
    "Turning off the tap while brushing your teeth can save 8 gallons of water daily.",
    "Trees absorb about 48 pounds of CO2 per year.",
    "LED bulbs use up to 75% less energy than traditional bulbs.",
    "A single reusable bag can replace over 700 plastic bags in its lifetime.",
    "Glass can be recycled endlessly without losing quality.",
    "Food waste makes up nearly 30% of what we throw away.",
    "Biking instead of driving reduces carbon emissions significantly.",
    "Planting more trees is one of the cheapest ways to fight climate change."
];

//function to set random fact on page load
function setRandomFact() {
    const factElement = document.getElementById("eco-fact");
    if (!factElement) return;
    const randomIndex = Math.floor(Math.random() * ecoFacts.length);
    factElement.textContent = ecoFacts[randomIndex];
}
window.onload = setRandomFact;
// SIGNUP
function signup() {
    const username = document.getElementById('signup-username').value;
    const password = document.getElementById('signup-password').value;

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(username)) {
        alert("Please enter a valid email address.");
        return;
    }

    fetch(`${backendURL}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
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

    // Basic frontend check
    if (!username || !password) {
        alert("Please enter both email and password.");
        return;
    }

    fetch(`${backendURL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            username: username, 
            password: password 
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.user_id) {
            alert("Login successful!");
            window.location.href = `dashboard.html?user_id=${data.user_id}&username=${encodeURIComponent(data.username)}`;
        } else {
            // This captures "Invalid password", "User not found", etc.
            alert(data.error || "Login failed. Please try again.");
        }
    })
    .catch(err => {
        console.error("Login Error:", err);
        alert("Connection error");
    });
}
      // FORGOT PASSWORD
function forgotPassword() {
    const email = document.getElementById('forgot-email').value;


    if (!email_pattern.test(email)) {
        alert("Please enter a valid email address.");
        return;
    }

    fetch(`${backendURL}/forgot-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            
            window.location.href = "index.html";
        } else {
            alert(data.error);
        }
    });
}
//RESET PASSWORD
function resetPassword() {
    const token = new URLSearchParams(window.location.search).get("token");
    const newPassword = document.getElementById('new-password').value;

    if (!newPassword || newPassword.length < 6) {
        alert("Password must be at least 6 characters.");
        return;
    }

    fetch(`${backendURL}/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            token: token,
            newPassword: newPassword
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location.href = "index.html";
        } else {
            alert(data.error);
        }
    });
}

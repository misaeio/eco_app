const backendURL = "http://127.0.0.1:5000";
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
    const randomIndex = Math.floor(Math.random() * ecoFacts.length);
    factElement.textContent = ecoFacts[randomIndex];
}
window.onload = setRandomFact;
// SIGNUP
function signup() {
    const username = document.getElementById('signup-username').value;
    const password = document.getElementById('signup-password').value;

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

// Parse URL to get user info, lets front end know which user logged in
const params = new URLSearchParams(window.location.search);
const currentUserId = params.get('user_id'); //extract value from URL
const currentUsername = params.get('username'); //extract value from URL

// Show welcome message
document.getElementById('welcome').innerText = "Welcome " + currentUsername; //gets html id with 'welcome' and concatenates w username

// Sets base URL 
const backendURL = "http://127.0.0.1:5000";

// Automatically load tasks when page loads
window.onload = function() {
    getTasks();
};

// GET TASKS
function getTasks() { //calls a backend function
    if (!currentUserId) return; //cehcks if user exists

    fetch(`${backendURL}/tasks/${currentUserId}`)//fetches for task with user id
    .then(res => res.json()) //response turns into JSON
    .then(data => { 
        const list = document.getElementById('tasks-list');
        list.innerHTML = ""; //removes all currently displayed tasks so we dont get duplicates
        
        data.forEach(t => { //loops through each task and creates <li> list
            const li = document.createElement('li');
            li.innerHTML = `${t.title} <button onclick="deleteTask(${t.id})">x</button>`; //creates a delete button next to each task
            list.appendChild(li); //appends tasks to the unordered or ordered list with task-list ID
        }); 
    })
    .catch(err => console.error("Error fetching tasks:", err)); //catches error
}

// ADD TASK
function addTask() {
    const task = document.getElementById('new-task').value; //reads task text from input with ID new-task
    
    if (!currentUserId) {
        alert("You must log in first!"); //not logged in
        return;
    }
    
    fetch(`${backendURL}/tasks`, {
        method: 'POST', //sends POST request
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task: task, user_id: currentUserId })
    })
    .then(res => res.json()) //response turns to JSON 
    .then(data => {
        alert(data.message || data.error);
        getTasks(); //calls get tasks to refresh tasks immediateley 
    })
    .catch(err => console.error("Error adding task:", err));
}

// DELETE TASK
function deleteTask(id) {
    fetch(`${backendURL}/tasks/${id}`, { method: 'DELETE' }) //deletes
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        getTasks(); //refreshes
    })
    .catch(err => console.error("Error deleting task:", err));
}

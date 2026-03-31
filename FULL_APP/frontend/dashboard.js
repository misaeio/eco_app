// Parse URL to get user info
const params = new URLSearchParams(window.location.search);
const currentUserId = params.get('user_id');
const currentUsername = params.get('username');

// Show welcome message
document.getElementById('welcome').innerText = "Welcome " + currentUsername;

// Replace with your backend URL
const backendURL = "http://127.0.0.1:5000";

// Automatically load tasks
window.onload = function() {
    getTasks();
};

// GET TASKS
function getTasks() {
    if (!currentUserId) return;

    fetch(`${backendURL}/tasks/${currentUserId}`)
    .then(res => res.json())
    .then(data => { 
        const list = document.getElementById('tasks-list');
        list.innerHTML = ""; 
        
        data.forEach(t => {
            const li = document.createElement('li');
            li.innerHTML = `${t.title} <button onclick="deleteTask(${t.id})">x</button>`;
            list.appendChild(li);
        }); 
    })
    .catch(err => console.error("Error fetching tasks:", err));
}

// ADD TASK
function addTask() {
    const task = document.getElementById('new-task').value;
    
    if (!currentUserId) {
        alert("You must log in first!");
        return;
    }
    
    fetch(`${backendURL}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task: task, user_id: currentUserId })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || data.error);
        getTasks();
    })
    .catch(err => console.error("Error adding task:", err));
}

// DELETE TASK
function deleteTask(id) {
    fetch(`${backendURL}/tasks/${id}`, { method: 'DELETE' })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        getTasks();
    })
    .catch(err => console.error("Error deleting task:", err));
}
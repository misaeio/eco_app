// URL params
const params = new URLSearchParams(window.location.search);
const currentUserId = params.get('user_id');
const currentUsername = params.get('username');

// backend URL
const backendURL = "http://127.0.0.1:5000";

// welcome message
document.getElementById('welcome').innerText = "Welcome " + currentUsername;

// tab func
function showTab(tabId) {
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
}

// load data on start
window.addEventListener('DOMContentLoaded', () => {
    getTasks();
    loadFeed();

    document.getElementById('add-task-btn').addEventListener('click', addTask);
    document.getElementById('post-btn').addEventListener('click', createPost);
});

// task func
function getTasks() {
    if (!currentUserId) return;

    fetch(`${backendURL}/tasks/${currentUserId}`)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('tasks-list');
            list.innerHTML = "";
            data.forEach(t => {
                const li = document.createElement('li');
                li.textContent = t.title + " ";

                const btn = document.createElement('button');
                btn.textContent = 'x';
                btn.addEventListener('click', () => deleteTask(t.id));
                li.appendChild(btn);

                list.appendChild(li);
            });
        })
        .catch(err => console.error(err));
}

function addTask() {
    const taskInput = document.getElementById('new-task');
    const task = taskInput.value.trim();
    if (!task) return alert("Task cannot be empty");

    fetch(`${backendURL}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task, user_id: currentUserId })
    })
        .then(res => res.json())
        .then(data => {
            alert(data.message || data.error);
            taskInput.value = "";
            getTasks();
        });
}

function deleteTask(id) {
    fetch(`${backendURL}/tasks/${id}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
            getTasks();
        });
}

//  post func
function loadFeed() {
    fetch(`${backendURL}/posts`)
        .then(res => res.json())
        .then(data => {
            const feed = document.getElementById('feed');
            feed.innerHTML = "";
            data.forEach(post => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${post.username}</strong>: ${post.content}`;
                feed.appendChild(li);
            });
        });
}

function createPost() {
    const contentInput = document.getElementById('new-post');
    const content = contentInput.value.trim();
    if (!content) return alert("Post cannot be empty");

    fetch(`${backendURL}/posts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, user_id: currentUserId })
    })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
            contentInput.value = "";
            loadFeed();
        });
}

const backendURL = "http://127.0.0.1:5000";

// USER INFO
const params = new URLSearchParams(window.location.search);
const currentUserId = params.get('user_id');
const currentUsername = params.get('username');

// WELCOME
document.getElementById('welcome').innerText =
    "Welcome " + currentUsername;

// INIT
window.addEventListener('DOMContentLoaded', () => {
    getTasks();
    loadFeed();

    document.getElementById('add-task-btn').addEventListener('click', addTask);
    document.getElementById('post-btn').addEventListener('click', createPost);
});

// --------------------
// TAB SWITCH
// --------------------
function showTab(tabId) {
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
}

// --------------------
// TASKS
// --------------------
function getTasks() {
    fetch(`${backendURL}/tasks/${currentUserId}`)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('tasks-list');
            list.innerHTML = "";

            data.forEach(t => {
                const li = document.createElement('li');
                li.textContent = t.title + " ";

                const btn = document.createElement('button');
                btn.textContent = "x";
                btn.onclick = () => deleteTask(t.id);

                li.appendChild(btn);
                list.appendChild(li);
            });
        });
}

function addTask() {
    const task = document.getElementById('new-task').value.trim();
    if (!task) return alert("Task cannot be empty");

    fetch(`${backendURL}/tasks`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            task,
            user_id: currentUserId
        })
    }).then(() => {
        document.getElementById('new-task').value = "";
        getTasks();
    });
}

function deleteTask(id) {
    fetch(`${backendURL}/tasks/${id}`, {
        method: "DELETE"
    }).then(() => getTasks());
}

// --------------------
// POSTS + FEED
// --------------------
function loadFeed() {
    fetch(`${backendURL}/posts`)
        .then(res => res.json())
        .then(posts => {
            const feed = document.getElementById('feed');
            feed.innerHTML = "";

            posts.forEach(post => {
                const div = document.createElement('div');

                div.innerHTML = `
                    <div style="margin-bottom:15px;">
                        <p><strong>${post.username}</strong></p>
                        <p>${post.content}</p>

                        ${post.image_url ? `<img src="${post.image_url}" width="200">` : ""}

                        <button onclick="likePost(${post.id})">🌱 Like</button>
                        <span id="likes-${post.id}">0</span>

                        <button onclick="toggleComments(${post.id})">💬 Comments</button>

                        <div id="comments-${post.id}" style="display:none;">
                            <input id="comment-input-${post.id}" placeholder="Write comment">
                            <button onclick="addComment(${post.id})">Post</button>

                            <ul id="comment-list-${post.id}"></ul>
                        </div>
                    </div>
                `;

                feed.appendChild(div);

                loadLikes(post.id);
                loadComments(post.id);
            });
        });
}

// --------------------
// CREATE POST
// --------------------
function createPost() {
    const content = document.getElementById('new-post').value.trim();
    const imageUrl = document.getElementById('new-image').value.trim();

    if (!content && !imageUrl) {
        return alert("Post cannot be empty");
    }

    fetch(`${backendURL}/posts`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: currentUserId,
            content,
            image_url: imageUrl
        })
    }).then(() => {
        document.getElementById('new-post').value = "";
        document.getElementById('new-image').value = "";
        loadFeed();
    });
}

// --------------------
// LIKES
// --------------------
function likePost(postId) {
    fetch(`${backendURL}/posts/${postId}/like`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id: currentUserId })
    })
    .then(res => res.json())
    .then(() => loadLikes(postId));
}

function loadLikes(postId) {
    fetch(`${backendURL}/posts/${postId}/likes`)
        .then(res => res.json())
        .then(data => {
            document.getElementById(`likes-${postId}`).innerText = data.count;
        });
}

// --------------------
// COMMENTS
// --------------------
function toggleComments(postId) {
    const box = document.getElementById(`comments-${postId}`);
    box.style.display = box.style.display === "none" ? "block" : "none";
}

function addComment(postId) {
    const input = document.getElementById(`comment-input-${postId}`);
    const text = input.value.trim();

    if (!text) return;

    fetch(`${backendURL}/posts/${postId}/comments`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: currentUserId,
            comment: text
        })
    }).then(() => {
        input.value = "";
        loadComments(postId);
    });
}

function loadComments(postId) {
    fetch(`${backendURL}/posts/${postId}/comments`)
        .then(res => res.json())
        .then(comments => {
            const list = document.getElementById(`comment-list-${postId}`);
            list.innerHTML = "";

            comments.forEach(c => {
                const li = document.createElement('li');
                li.textContent = `${c.username}: ${c.comment}`;
                list.appendChild(li);
            });
        });
}

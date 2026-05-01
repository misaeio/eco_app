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
    loadProfile();

    document.getElementById('add-task-btn').addEventListener('click', addTask);
    document.getElementById('post-btn').addEventListener('click', createPost);
});
// TAB SWITCH
function showTab(tabId) {
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
}
// TASKS
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
// POSTS + FEED
function loadFeed() {
    fetch(`${backendURL}/posts`)
        .then(res => res.json())
        .then(posts => {
            const feed = document.getElementById('feed');
            feed.innerHTML = "";

            posts.forEach(post => {
                const div = document.createElement('div');

                div.innerHTML = `
                    <div style="display:flex; gap:10px; align-items:center; margin-bottom:8px;">
                        <img src="${post.profile_pic || 'default.png'}" 
                             width="40" height="40" 
                             style="border-radius:50%; object-fit:cover;">

                        <strong>${post.username}</strong>
                    </div>

                    <p>${post.content}</p>

                    ${post.image_url ? `<img src="${post.image_url}" width="200" style="border-radius:8px;">` : ""}

                    <div style="margin-top:8px;">
                        <button onclick="likePost(${post.id})">❤️ Like</button>
                        <span id="likes-${post.id}">0</span>

                        <button onclick="toggleComments(${post.id})">💬 Comments</button>
                    </div>

                    <div id="comments-${post.id}" style="display:none;">
                        <input id="comment-input-${post.id}" placeholder="Write comment">
                        <button onclick="addComment(${post.id})">Post</button>
                        <ul id="comment-list-${post.id}"></ul>
                    </div>
                `;

                feed.appendChild(div);

                loadLikes(post.id);
                loadComments(post.id);
            });
        });
}
// CREATE POST
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
// LIKES
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

// COMMENTS
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

function loadProfile(){
            fetch(`${backendURL}/profile/${currentUserId}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('profile-username').value = data.username || "";
                document.getElementById('profile-bio').value = data.bio || "";
                document.getElementById('profile-pic').value = data.profile_pic || "";
            });
        }


function saveProfile() {
    const username = document.getElementById('profile-username').value;
    const bio = document.getElementById('profile-bio').value;
    const profile_pic = document.getElementById('profile-pic').value;

    fetch(`${backendURL}/profile`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: currentUserId,
            username,
            bio,
            profile_pic
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || data.error);

       document.getElementById('welcome').innerText = "Welcome " + username;

const newUrl = `dashboard.html?user_id=${currentUserId}&username=${encodeURIComponent(username)}`;
window.history.replaceState({}, "", newUrl);

        loadFeed();
    });
}

function updateProfile(){
    const username = document.getElementById("edit-username").value;
    const bio = document.getElementById("edit-bio").value;
    const profile_pic = document.getElementById("edit-pfp").value;

    fetch(`${backendURL}/profile/${currentUserId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username,
            bio,
            profile_pic
        })
    })
    .then(res => res.json())
    .then(data => {
        alert("Profile updated!");
        location.reload();
    });
}

function loadProfile() {
    fetch(`${backendURL}/profile/${currentUserId}`)
        .then(res => res.json())
        .then(user => {
            document.getElementById('profile-username-display').innerText = user.username;
            document.getElementById('profile-bio-display').innerText = user.bio || "";
            document.getElementById('profile-pic-display').src = user.profile_pic || "default.png";

            document.getElementById('followers').innerText = "Followers: " + user.followers_count;
            document.getElementById('following').innerText = "Following: " + user.following_count;
        });
}

function showTab(tabId) {
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');

    if (tabId === "profile") {
        loadProfile();
    }
}



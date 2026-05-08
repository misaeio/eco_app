 const backendURL = "http://127.0.0.1:5000";

// USER INFO
const params = new URLSearchParams(window.location.search);
const currentUserId = params.get('user_id');
const currentUsername = params.get('username');

let viewingUserId = currentUserId;

// safety check
if (!currentUserId) {
    console.error("Missing user_id in URL");
    window.location.href = "login.html";
}

// init
window.addEventListener("DOMContentLoaded", () => {
    loadFeed();
    loadProfile(currentUserId);
    loadUserHeader();

    document.getElementById("post-btn").onclick = createPost;
});

// welcome
function loadUserHeader() {
    fetch(`${backendURL}/user/${currentUserId}?current_user_id=${currentUserId}`)
        .then(r => r.json())
        .then(u => {
            document.getElementById("welcome").innerText =
                "Welcome " + (u.username || "User");
        })
        .catch(err => console.error("Header error:", err));
}

// tab switch
function showTab(tabId) {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.getElementById(tabId).classList.add("active");
}

// feed
function loadFeed() {
    fetch(`${backendURL}/posts`)
        .then(r => r.json())
        .then(posts => {
            const feed = document.getElementById("feed");
            feed.innerHTML = "";

            posts.forEach(post => {
                const div = document.createElement("div");

                div.innerHTML = `
                    <div onclick="viewProfile(${post.user_id})"
                         style="cursor:pointer; display:flex; gap:10px; align-items:center;">

                        <img src="${post.profile_pic || 'default.png'}"
                             width="40" height="40"
                             style="border-radius:50%">

                        <b>${post.username}</b>
                    </div>

                    <p>${post.content || ""}</p>

                    ${post.image_url ? `<img src="${post.image_url}" width="200">` : ""}

                    <button onclick="likePost(${post.id})">❤️ Like</button>
                    <span id="likes-${post.id}">0</span>

                    <button onclick="toggleComments(${post.id})">💬</button>

                    <div id="comments-${post.id}" style="display:none;">
                        <input id="comment-${post.id}" placeholder="Comment">
                        <button onclick="addComment(${post.id})">Send</button>
                        <ul id="list-${post.id}"></ul>
                    </div>
                `;

                feed.appendChild(div);

                loadLikes(post.id);
                loadComments(post.id);
            });
        })
        .catch(err => console.error("Feed error:", err));
}

// create posts
function createPost() {
    fetch(`${backendURL}/posts`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: currentUserId,
            content: document.getElementById("new-post").value,
            image_url: document.getElementById("new-image").value
        })
    })
    .then(() => loadFeed())
    .catch(err => console.error("Post error:", err));
}

// likes
function likePost(postId) {
    fetch(`${backendURL}/posts/${postId}/like`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id: currentUserId })
    })
    .then(() => loadLikes(postId))
    .catch(err => console.error("Like error:", err));
}

function loadLikes(postId) {
    fetch(`${backendURL}/posts/${postId}/likes`)
        .then(r => r.json())
        .then(d => {
            document.getElementById(`likes-${postId}`).innerText = d.count || 0;
        })
        .catch(err => console.error("Likes load error:", err));
}

// comments
function toggleComments(id) {
    const el = document.getElementById(`comments-${id}`);
    if (!el) return;
    el.style.display = el.style.display === "none" ? "block" : "none";
}

function addComment(id) {
    const input = document.getElementById(`comment-${id}`);

    fetch(`${backendURL}/posts/${id}/comments`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: currentUserId,
            comment: input.value
        })
    })
    .then(() => loadComments(id))
    .catch(err => console.error("Comment error:", err));
}

function loadComments(id) {
    fetch(`${backendURL}/posts/${id}/comments`)
        .then(r => r.json())
        .then(comments => {
            const list = document.getElementById(`list-${id}`);
            if (!list) return;

            list.innerHTML = "";

            comments.forEach(c => {
                const li = document.createElement("li");
                li.innerText = `${c.username}: ${c.comment}`;
                list.appendChild(li);
            });
        })
        .catch(err => console.error("Load comments error:", err));
}

// profile
function viewProfile(userId) {
    viewingUserId = userId;

    fetch(`${backendURL}/user/${userId}?current_user_id=${currentUserId}`)
        .then(r => r.json())
        .then(u => {

            showTab("profile");

            document.getElementById("profile-username-display").innerText = u.username || "";
            document.getElementById("profile-bio-display").innerText = u.bio || "";
            document.getElementById("profile-pic-display").src = u.profile_pic || "default.png";

            document.getElementById("followers").innerText = "Followers: " + (u.followers || 0);
            document.getElementById("following").innerText = "Following: " + (u.following || 0);

            const btn = document.getElementById("follow-btn");

            const editSection = document.getElementById("edit-section");

            if (String(userId) === String(currentUserId)) {
         
                btn.style.display = "none";
                editSection.style.display = "block";
            } else {
               
                btn.style.display = "block";
                editSection.style.display = "none";
            }

            btn.innerText = u.is_following ? "Unfollow" : "Follow";
            btn.onclick = () => toggleFollow(userId, u.is_following);
        })
        .catch(err => console.error("Profile error:", err));
}

//  follow
function toggleFollow(userId, isFollowing) {
    const url = isFollowing ? "/unfollow" : "/follow";

    fetch(`${backendURL}${url}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            follower_id: currentUserId,
            following_id: userId
        })
    })
    .then(() => viewProfile(userId))
    .catch(err => console.error("Follow error:", err));
}

function showTab(tabId) {
    document.querySelectorAll(".tab").forEach(tab => {
        tab.classList.remove("active");
    });

    const selected = document.getElementById(tabId);
    if (selected) {
        selected.classList.add("active");
    }
}

function openMyProfile() {
    viewProfile(currentUserId);
}

//saveProfile
function saveProfile() {
    const username = document.getElementById('profile-username').value;
    const bio = document.getElementById('profile-bio').value;
    const profile_pic = document.getElementById('profile-pic').value;

    fetch(`${backendURL}/profile`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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

        viewProfile(currentUserId);
    })
    .catch(err => {
        console.error("Save profile error:", err);
        alert("Failed to update profile");
    });
}

//updateProfile
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

//loadProfile
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

async function searchRecyclingCenters() {
    const zipCode = document.getElementById('zipCode').value;
    const resultsDiv = document.getElementById('recycling-results');

    if (!zipCode || zipCode.length !== 5 || isNaN(zipCode)) {
        resultsDiv.innerHTML = '<div class="error">Please enter a valid ZIP code</div>';
        return;
    }

    resultsDiv.innerHTML = '<div class="loading"> Searching...</div>';

    try {
        const response = await fetch('http://127.0.0.1:5000/recycling-centers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ zip_code: zipCode })
        });

        const data = await response.json();

        if (data.error) {
            resultsDiv.innerHTML = `<div class="error"> ${data.error}</div>`;
            return;
        }

        if (!data.centers || data.centers.length === 0) {
            resultsDiv.innerHTML = '<div class="error"> No recycling centers found.</div>';
            return;
        }

        let html = `<h3>Found ${data.centers.length} center(s) near ${data.zip_code}:</h3>`;

        data.centers.forEach((center, index) => {
            html += `
                <div class="center-card">
                    <div class="center-name">${index + 1}. ${center.name}</div>
                    <div> ${center.address}</div>
                    <div>🗺️ <a href="https://www.google.com/maps?q=${center.latitude},${center.longitude}" target="_blank">Open in Google Maps</a></div>
                </div>
            `;
        });

        resultsDiv.innerHTML = html;

    } catch (error) {
        resultsDiv.innerHTML = '<div class="error"> Unable to connect to server.</div>';
    }
}




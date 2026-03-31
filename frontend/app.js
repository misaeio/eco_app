const backendURL = 'http://127.0.0.1:5000';

//signup
function signup(){ //declares function called signup. HTML calls this
    const username = document.getElementById('signup-username').value //doc...(username') finds username input in html. .value gets the actual value
    const password = document.getElementById('signup-password').value //doc...(password') finds password input in html. .value gets the actual value

    fetch(`${backendURL}/signup`,{ //fetch() makes a network request. ${backendURL}/signup is the URL of flask in app.py file
    method: 'POST', //send data to server
        headers: {'Content-Type': 'application/json' }, //tells server that data is JSON type
        body: JSON.stringify({ username, password}) //turns JS object to JSON so flask in app.py can read
    })
    .then(res => res.json()) //if backend responds .then gets that response and .json() turns it into JS so this can read it
    .then(data => alert(data.message || data.error)); //now data has what flask returned. Either "User created" or "User alr exists"
}


//login
function login() { 
    const username = document.getElementById('login-username').value; //get text from username text box
    const password = document.getElementById('login-password').value;  //get text from PW text box 
    
    
    fetch(`${backendURL}/login`, {  //pushes user data to server 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, // tells server data is incoming (JSON)
        body: JSON.stringify({ username, password }) // data turns  into string
    }) 
    .then(res => res.json()) 
    .then(data => { 
        if (data.user_id) { // if server responds with user ID, all is well 
            currentUserId = data.user_id; // stores ID to memory to know who is logged in 
            alert(data.message); // confirms login
            getTasks(); // calls on getTasks to show current task list 
        } else { 
            alert(data.error); // login failure error
        } 
    }); 
} 

//shows user tasks (after login)
function getTasks() {  //pull list of task from database (currently they all display on "main menu" - can change later)
    if (!currentUserId) return; // stops if not logged in - will need to change for guest functionality
    

    fetch(`${backendURL}/tasks/${currentUserId}`)  //pulls tasks connected to specific user ID from server
    .then(res => res.json()) // converts server list to JS
    .then(data => { 
        const list = document.getElementById('tasks-list'); // displays on webpage 
        list.innerHTML = ""; // prevents duplicates from being shown
        
        
        
        data.forEach(t => { //for displaying tasks after login
            const li = document.createElement('li'); // creates new list item (basically listing tasks on home screen)
    
            li.innerHTML = `${t.title} <button onclick="deleteTask(${t.id})">x</button>`; //displays task name and puts "x" next to text for deletion
            list.appendChild(li); // attaches task and button to web page 
        }); 
    }); 
} 

// allows user to add new task
function addTask() { 
    const task = document.getElementById('new-task').value; // gets text from new task text box 
    
    if (!currentUserId) { // ensures user is logged in 
        alert("You must log in first!"); 
        return; 
    } 
    
    fetch(`${backendURL}/tasks`, {  //adds new task ID and user ID to server 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, 
        body: JSON.stringify({ task: task, user_id: currentUserId }) 
    }) 
    .then(res => res.json()) 
    .then(data => { 
        alert(data.message || data.error); // either confirms insertion or shows error
        getTasks(); // refresh so newly added task shows up
    }); 
} 

// task deletion
function deleteTask(id) { //delete task from account 
    fetch(`${backendURL}/tasks/${id}`, { //tells server which task ID to remove
        method: 'DELETE' 
    }) 
    .then(res => res.json()) 
    .then(data => { 
        alert(data.message); // confirmation of deletion (tells user)
        getTasks(); // refresh to show current tasks (after tasks get deleted)
    }); 
}
const API_URL = "http://192.168.49.2:30008/tasks"; // replace with your URL

async function addTask() {
    const input = document.getElementById("taskInput");
    const task = input.value;

    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ task: task })
    });

    input.value = "";
    loadTasks();
}

async function loadTasks() {
    const res = await fetch(API_URL);
    const data = await res.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";

    data.forEach(t => {
        const li = document.createElement("li");
        li.textContent = t.task;
        list.appendChild(li);
    });
}

window.onload = loadTasks;
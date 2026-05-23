const API_URL = "http://54.234.84.29:8000";

const textInput = document.getElementById("textInput");
const sendBtn = document.getElementById("sendBtn");
const tasksDiv = document.getElementById("tasks");

let savedTasks = JSON.parse(localStorage.getItem("tasks")) || [];

sendBtn.addEventListener("click", async () => {
  const text = textInput.value.trim();

  if (text === "") {
    alert("Escribe un texto primero");
    return;
  }

  const response = await fetch(`${API_URL}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text })
  });

  const task = await response.json();

  savedTasks.push(task.id);
  localStorage.setItem("tasks", JSON.stringify(savedTasks));

  textInput.value = "";

  addTaskToDOM({
    id: task.id,
    text: text,
    status: "pendiente",
    result: null
  });

  listenTask(task.id);
});

function addTaskToDOM(task) {
  let statusClass = task.status.replace(" ", "-");

  const taskElement = document.createElement("div");
  taskElement.className = `task ${statusClass}`;
  taskElement.id = `task-${task.id}`;

  taskElement.innerHTML = `
    <strong>ID:</strong> ${task.id}<br>
    <strong>Estado:</strong> <span class="status">${task.status}</span>
    <div class="result">${task.result ? JSON.stringify(task.result, null, 2) : "Sin resultado todavía"}</div>
  `;

  tasksDiv.prepend(taskElement);
}

function updateTask(task) {
  const taskElement = document.getElementById(`task-${task.id}`);

  if (!taskElement) {
    addTaskToDOM(task);
    return;
  }

  let statusClass = task.status.replace(" ", "-");

  taskElement.className = `task ${statusClass}`;

  taskElement.querySelector(".status").textContent = task.status;
  taskElement.querySelector(".result").textContent = task.result
    ? JSON.stringify(task.result, null, 2)
    : "Sin resultado todavía";
}

function listenTask(taskId) {
  const events = new EventSource(`${API_URL}/events/${taskId}`);

  events.onmessage = (event) => {
    const task = JSON.parse(event.data);
    updateTask(task);

    if (task.status === "completada" || task.status === "error") {
      events.close();
    }
  };
}

async function loadOldTasks() {
  const response = await fetch(`${API_URL}/tasks`);
  const tasks = await response.json();

  tasks.forEach(task => {
    updateTask(task);

    if (task.status !== "completada" && task.status !== "error") {
      listenTask(task.id);
    }
  });
}

loadOldTasks();

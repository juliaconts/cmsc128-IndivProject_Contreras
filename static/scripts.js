document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("add-task");
  const emptyView = document.getElementById("empty-view");
  const taskForm = document.getElementById("task-form");
  const viewAddTask = document.getElementById('task-view-box');

  addBtn.addEventListener("click", () => {
    if (!taskForm || !emptyView) return;

    // toggle between showing the form and the "no task selected" placeholder
    if (taskForm.classList.contains("hidden")) {
      emptyView.classList.add("hidden");
      taskForm.classList.remove("hidden");
      viewAddTask.classList.add('dim');
    
    } else {
      taskForm.classList.add("hidden");
      emptyView.classList.remove("hidden");
      viewAddTask.classList.remove('dim');
    }
  });
});

document.addEventListener("DOMContentLoaded", function() {
    const tasks = document.querySelectorAll(".task");
    const detailBox = document.getElementById("task-view-box");
    const placeholder = document.getElementById("placeholder");

    tasks.forEach(task => {
        task.addEventListener("click", function() {
            // Hide placeholder
            if (placeholder) placeholder.style.display = "none";

            // Get task data
            const label = task.dataset.label;
            const taskName = task.dataset.task;
            const date = task.dataset.date;
            const time = task.dataset.time;
            const desc = task.dataset.desc || "No description";
            const sub = task.dataset.sub || "None";
            const created = task.dataset.created || "Unknown";

            // Inject into right panel
            detailBox.innerHTML = `
                <h3>${label}</h3>
                <p><strong>Task:</strong> ${taskName}</p>
                <p><strong>Due:</strong> ${date} at ${time}</p>
                <p><strong>Description:</strong> ${desc}</p>
                <p><strong>Sub-tasks:</strong> ${sub}</p>
                <p><em>Added on: ${created}</em></p>
            `;
        });
    });
});
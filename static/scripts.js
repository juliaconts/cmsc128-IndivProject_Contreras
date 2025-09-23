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
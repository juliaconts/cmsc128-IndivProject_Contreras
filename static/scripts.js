document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("add-task");
  const viewBox = document.getElementById("task-view-box");
  const emptyView = document.getElementById("empty-view");
  const taskDetails = document.getElementById("task-details");
  const taskForm = document.getElementById("task-form");
  const taskBox = document.getElementById("task-box");

  // guard: if any critical element is missing, stop
  if (!addBtn || !viewBox || !emptyView || !taskDetails || !taskForm || !taskBox) return;

  // helper: escape text inserted into innerHTML
  function escapeHtml(str) {
    if (str === null || str === undefined) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // --- NEW: load saved completions from localStorage
  function loadCompletionState() {
    const saved = JSON.parse(localStorage.getItem("completedTasks") || "{}");
    return saved;
  }

  function saveCompletionState(state) {
    localStorage.setItem("completedTasks", JSON.stringify(state));
  }

  // --- NEW: restore state to DOM
  function restoreCompletionState() {
    const completedTasks = loadCompletionState();
    taskBox.querySelectorAll(".task").forEach((li) => {
      const id = li.dataset.id;
      const check = li.querySelector(".task-check");
      if (id && completedTasks[id]) {
        li.classList.add("completed");
        if (check) check.checked = true;
      } else {
        li.classList.remove("completed");
        if (check) check.checked = false;
      }
    });
  }

  // --- checkbox handler
  taskBox.addEventListener("change", (ev) => {
    if (ev.target.classList.contains("task-check")) {
      const li = ev.target.closest(".task");
      if (!li) return;

      const id = li.dataset.id;
      const completedTasks = loadCompletionState();

      if (ev.target.checked) {
        li.classList.add("completed");
        if (id) completedTasks[id] = true; // save
      } else {
        li.classList.remove("completed");
        if (id) delete completedTasks[id]; // remove
      }

      saveCompletionState(completedTasks); // persist
    }
  });

  // --- restore state on load
  restoreCompletionState();

  // toast notification helper
  function showToast(message, undoUrl) {
    const toast = document.getElementById("toast");
    const toastMsg = document.getElementById("toast-message");
    const undoBtn = document.getElementById("undo-btn");

    if (!toast || !toastMsg || !undoBtn) return;

    toastMsg.textContent = message;
    toast.classList.remove("hidden");
    toast.classList.add("show");

    if (undoUrl && undoUrl !== "#") {
      undoBtn.style.display = "inline-block";
      undoBtn.onclick = () => {
        toast.classList.remove("show");
        toast.classList.add("hidden");
        window.location.href = undoUrl;
      };
    } else {
      undoBtn.style.display = "none"; // hide undo for updates
    }

    // Auto-hide after 5s
    setTimeout(() => {
      toast.classList.remove("show");
      toast.classList.add("hidden");
    }, 5000);
  }

  // Show Add form (toggle)
  addBtn.addEventListener("click", (ev) => {
    ev.stopPropagation();

    const formVisible = !taskForm.classList.contains("hidden");
    if (!formVisible) {
      taskForm.classList.remove("hidden");
      taskDetails.classList.add("hidden");
      emptyView.classList.add("hidden");
      viewBox.classList.add("dim");
      const first = taskForm.querySelector("input, textarea, select");
      if (first) first.focus();
    } else {
      taskForm.classList.add("hidden");
      viewBox.classList.remove("dim");
      if (taskDetails.classList.contains("hidden")) {
        emptyView.classList.remove("hidden");
      }
    }
  });

  // clicking inside the right panel shouldn’t bubble
  viewBox.addEventListener("click", (e) => e.stopPropagation());

  // Event delegation for task clicks
  taskBox.addEventListener("click", (ev) => {
    const li = ev.target.closest(".task");
    if (!li) return;
    ev.stopPropagation();

    // remove 'selected' from others
    [...taskBox.querySelectorAll(".task")].forEach((t) => t.classList.remove("selected"));
    li.classList.add("selected");

    // hide form & placeholder
    taskForm.classList.add("hidden");
    emptyView.classList.add("hidden");
    viewBox.classList.remove("dim");
    taskDetails.classList.remove("hidden");

    // read data attributes
    const priority = li.dataset.priority || li.dataset.prio || "";
    const label = li.dataset.label || "";
    const taskName = li.dataset.task || "";
    const date = li.dataset.date || "";
    const time = li.dataset.time || "";
    const desc = li.dataset.desc || "";
    const sub = li.dataset.sub || "";
    const created = li.dataset.created || "";

    // show details
    taskDetails.innerHTML = `
      <div class="task-details-box">
        <div id="header">
          <span class="prio"><small>Priority Level: ${escapeHtml(priority)}</small></span>
          <h2>${escapeHtml(taskName)}</h2>
          <p><strong>Label:</strong> ${escapeHtml(label)}</p>
        </div>
        <p><strong>Due Date:</strong> ${escapeHtml(date)} ${escapeHtml(time)}</p>
        <p><strong>Description:</strong><br>${escapeHtml(desc)}</p>
        <p><strong>Sub-tasks:</strong> ${escapeHtml(sub)}</p>
        <p><em>Created: ${escapeHtml(created)}</em></p>
        <div style="margin-top:12px;">
          <button id="edit-task-btn" type="button">Edit</button>
          <button id="delete-task-btn" type="button">Delete</button>
        </div>
      </div>
    `;

    // edit button logic
    const editBtn = document.getElementById("edit-task-btn");
    if (editBtn) {
      editBtn.addEventListener("click", () => {
        taskDetails.innerHTML = `
          <form method="POST" action="/edit/${li.dataset.id}" class="task-details-box">
            <h2>Edit Task</h2>

            <label>Priority:</label>
            <input type="number" name="priority" value="${escapeHtml(priority)}" min="1" max="3" required><br>

            <label>Label:</label>
            <input type="text" name="label" value="${escapeHtml(label)}" required><br>

            <label>Task Name:</label>
            <input type="text" name="task_name" value="${escapeHtml(taskName)}" required><br>

            <label>Date:</label>
            <input type="date" name="date" value="${escapeHtml(date)}"><br>

            <label>Time:</label>
            <input type="time" name="time" value="${escapeHtml(time)}"><br>

            <label>Description:</label>
            <textarea name="task_desc">${escapeHtml(desc)}</textarea><br>

            <label>Sub-Tasks:</label>
            <input type="text" name="sub_todo" value="${escapeHtml(sub)}"><br>

            <div style="margin-top:12px;">
              <button type="submit">Save Changes</button>
              <button type="button" id="cancel-edit">Cancel</button>
            </div>
          </form>
        `;

        const editForm = taskDetails.querySelector("form");
        if (editForm) {
          editForm.addEventListener("submit", () => {
            localStorage.setItem("toastMessage", "Task Updated");
          });
        }

        const cancelBtn = document.getElementById("cancel-edit");
        if (cancelBtn) {
          cancelBtn.addEventListener("click", () => {
            if (typeof li.click === "function") {
              li.click();
            } else {
              emptyView.classList.remove("hidden");
            }
          });
        }
      });
    }

    // delete button logic
    const deleteBtn = document.getElementById("delete-task-btn");
    if (deleteBtn) {
      deleteBtn.addEventListener("click", () => {
        if (confirm("Delete this task?")) {
          fetch("/delete/" + li.dataset.id).then(() => {
            localStorage.setItem("toastMessage", "Task Deleted");
            localStorage.setItem("undoUrl", "/undo_delete");
            window.location.reload();
          });
        }
      });
    }
  });

  // Click outside → reset to placeholder
  document.addEventListener("click", () => {
    if (
      !emptyView.classList.contains("hidden") &&
      taskForm.classList.contains("hidden") &&
      taskDetails.classList.contains("hidden")
    ) {
      return;
    }
    taskForm.classList.add("hidden");
    taskDetails.classList.add("hidden");
    [...taskBox.querySelectorAll(".task")].forEach((t) => t.classList.remove("selected"));
    emptyView.classList.remove("hidden");
    viewBox.classList.remove("dim");
  });

  // show toast if stored in localStorage
  const savedMsg = localStorage.getItem("toastMessage");
  const savedUndo = localStorage.getItem("undoUrl");
  if (savedMsg) {
    showToast(savedMsg, savedUndo || "#");
    localStorage.removeItem("toastMessage");
    localStorage.removeItem("undoUrl");
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("toggle-sub");
  const subBox = document.getElementById("sub-task-box");

  if (toggle && subBox) {
    toggle.addEventListener("change", () => {
      subBox.style.display = toggle.checked ? "block" : "none";
    });
  }
});
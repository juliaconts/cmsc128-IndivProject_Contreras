document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("add-task");
  const viewBox = document.getElementById("task-view-box");
  const emptyView = document.getElementById("empty-view");
  const taskDetails = document.getElementById("task-details");
  const taskForm = document.getElementById("task-form");
  const taskItems = document.querySelectorAll("#task-box .task");

  if (!addBtn || !viewBox) return; // guard

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

  // Show Add form (toggle)
  addBtn.addEventListener("click", (ev) => {
    ev.stopPropagation(); // so document click won't immediately hide it

    const formVisible = !taskForm.classList.contains("hidden");
    if (!formVisible) {
      // show form; hide details and placeholder
      taskForm.classList.remove("hidden");
      taskDetails.classList.add("hidden");
      emptyView.classList.add("hidden");
      viewBox.classList.add("dim");
      // focus first input for convenience
      const first = taskForm.querySelector("input, textarea, select");
      if (first) first.focus();
    } else {
      // hide form; return to placeholder if details are hidden
      taskForm.classList.add("hidden");
      viewBox.classList.remove("dim");
      if (taskDetails.classList.contains("hidden")) {
        emptyView.classList.remove("hidden");
      }
    }
  });

  // clicking inside the right panel shouldn't bubble to document (prevent auto-close)
  viewBox.addEventListener("click", (e) => e.stopPropagation());

  // When a left-side task is clicked => show full details on right
  taskItems.forEach(li => {
    li.addEventListener("click", (ev) => {
      ev.stopPropagation();

      // remove 'selected' from other items and add to this
      taskItems.forEach(t => t.classList.remove("selected"));
      li.classList.add("selected");

      // hide form & placeholder
      taskForm.classList.add("hidden");
      emptyView.classList.add("hidden");
      viewBox.classList.remove("dim");
      taskDetails.classList.remove("hidden");

      // read data attributes (some templates use data-priority or data-prio)
      const priority = li.dataset.priority || li.dataset.prio || "";
      const label = li.dataset.label || "";
      const taskName = li.dataset.task || "";
      const date = li.dataset.date || "";
      const time = li.dataset.time || "";
      const desc = li.dataset.desc || "";
      const sub = li.dataset.sub || "";
      const created = li.dataset.created || "";

      // show details — using escapeHtml to avoid HTML injection
      taskDetails.innerHTML = `
        <div class="task-details-box">
          <div id="header">
              <span class="prio"><small>Priority Level: ${escapeHtml(priority)}</small></span>
              <h2>${escapeHtml(taskName)}</h2>
              <p><strong>Label:</strong> ${escapeHtml(label)}</p>
          </div>
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

      const editBtn = document.getElementById("edit-task-btn");
      const deleteBtn = document.getElementById("delete-task-btn");

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

          const cancelBtn = document.getElementById("cancel-edit");
          if (cancelBtn) {
            cancelBtn.addEventListener("click", () => {
              li.click();
          });
        }
      });
    }

    if (deleteBtn) {
      deleteBtn.addEventListener("click", () => {
        if (confirm("Delete this task?")) {
          window.location.href = "/delete/" + li.dataset.id;
        }
      });
    }
  });
});

  // Click outside (anywhere on doc) → hide details/form and show placeholder
  document.addEventListener("click", () => {
    // only reset if something was visible
    if (!emptyView.classList.contains("hidden") && taskForm.classList.contains("hidden") && taskDetails.classList.contains("hidden")) {
      return; // already placeholder
    }
    // hide form and details
    taskForm.classList.add("hidden");
    taskDetails.classList.add("hidden");
    // remove selected highlight
    taskItems.forEach(t => t.classList.remove("selected"));
    // show placeholder
    emptyView.classList.remove("hidden");
    viewBox.classList.remove("dim");
  });
});

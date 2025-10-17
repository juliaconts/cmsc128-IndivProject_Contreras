document.addEventListener("DOMContentLoaded", () => {
  const viewMode = document.getElementById("viewMode");
  const formContainer = document.getElementById("formContainer");
  const editBtn = document.getElementById("editBtn");

  // Fade out flash messages after 3s
  const flashMessages = document.getElementById("flash-messages");
  if (flashMessages) {
    setTimeout(() => {
      flashMessages.style.transition = "opacity 0.5s ease";
      flashMessages.style.opacity = "0";
      setTimeout(() => flashMessages.remove(), 500);
    }, 1000);
  }

  // Create the Edit form dynamically when "Edit" is clicked
  if (editBtn) {
    editBtn.addEventListener("click", () => {
      // Hide view mode
      viewMode.style.display = "none";

      // Build the form dynamically
      const formHTML = `
        <form id="editForm" method="POST" action="/profile">
        <div class="edit-rows">
          <label>First Name:</label>
          <input type="text" name="fname" value="${userData.fname}" required>
        </div>
          
        <div class="edit-rows">
          <label>Last Name:</label>
          <input type="text" name="lname" value="${userData.lname}" required>
        </div>
          
        <div class="edit-rows">
          <label>Username:</label>
          <input type="text" name="username" value="${userData.username}" required>
        </div>
          
        <div class="edit-rows">
          <label>New Password (leave blank to keep current):</label>
          <input type="password" name="password">
        </div>


          <div style="margin-top:10px;">
            <button type="submit">Save Changes</button>
            <button type="button" id="cancelBtn">Cancel</button>
          </div>
        </form>
      `;

      formContainer.innerHTML = formHTML;

      // Cancel button logic
      const cancelBtn = document.getElementById("cancelBtn");
      cancelBtn.addEventListener("click", () => {
        formContainer.innerHTML = "";
        viewMode.style.display = "block";
      });
    });
  } else {
    console.error("Edit button not found — check your HTML IDs!");
  }
});

const flashMessages = document.getElementById("flash-messages");
if (flashMessages) {
  setTimeout(() => {
    flashMessages.style.transition = "opacity 0.5s ease";
    flashMessages.style.opacity = "0";
    setTimeout(() => flashMessages.remove(), 500);
  }, 3000);
}
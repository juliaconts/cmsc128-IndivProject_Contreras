Name: Julia Louise M. Contreras
Laboratory Activity 1
CMSC 124 - 1 

Fullstack To-do List Web Application

This To-do list web app was built with the following tech stack:
- Backend: Flask
- Database: SQLite
- Frontend: HTML, CSS, Javascript

-> Why use Flask and SQLite as your backend + database?
    Flask and SQLite are both lightweight and minimal, making them easy to use for a small projects like this activity.
    Flask is easy to learn because it uses Python. You can add the features you need instead of being forced into a heavy framework. It uses simple Python functions, routes, and filters, making the code easy to read and understand. 
    SQLite is also to setup because all its data is stored in a single file where you don't need to install or run a separate database server. Since SQLite is built into Python, there is no need for extra installations or environment setup. Its syntax in making queries are very similar to mySQL as I have prior experience in handling mySQL.

-> How to run the web application?
1. Clone this repository
2. Create a virtual environment
    python -m venv venv

3. Activate the virtual environment
    venv\Scripts\activate

4. Install the required dependencies
    pip install flask

5. Run the app.py file
6. Click on the given running server found in your terminal as this will open the app in your browser

-> Example API Endpoints
1. Main interface / List all tasks
    GET/
    - Returns homepage (homepage.html) with all tasks listed
    - Optional query parameter:
        - ?sort=priority -> sort tasks by priority
        - ?sort=due -> sort by due date and time
        - ?sort=timestamp -> sort by when they were created

2. Add a new task
    POST /add
    - Adds a new task to the database
    - Example request body (form-data):
        {
            "priority": 1,
            "label": "CMSC 128",
            "task_name": "laboratory Activity 1",
            "date": "2025-09-29",
            "time": "12:00",
            "task_desc": "Do a fullstack to-do list",
            "sub_todo": "create a skeletal html, css & js files"
        }

3. Edit an existing task
    POST /edit/<task_id>
    - Updates task details by its id.
    - Example body (form-data):
        POST /edit/1
        {
            "priority": 1,
            "label": "CMSC 128",
            "task_name": "laboratory Activity 1",
            "date": "2025-09-29",
            "time": "12:30",
            "task_desc": "Do a fullstack to-do list",
            "sub_todo": "implement flask + sqlite"
        }

4. Delete a task
    GET/delete/<task_id>
    - Deletes a task by its id
    - Stores the deleted task in session for possible undo
    - Example: GET s/delete/1

5. Undo last deleted task
    GET/undo_delete
    - Restores the most recently deleted task (if available)
    - Example: GET /undo_delete

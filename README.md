# StudyTrack

StudyTrack is a lightweight desktop task-management application for university students.

It was implemented from the Assessment 3 design and keeps the same core scope:
- personal student task list
- simple navigation
- local storage
- four CRUD functions
- no LMS, grades, enrolment or staff communication features

## Core Features

1. **Create / Add Task**
   - Task name
   - Subject / unit code
   - Due date
   - Priority: Low, Medium or High
   - Optional notes

2. **Read / View Tasks**
   - Displays all saved tasks
   - Automatically sorts tasks by due date

3. **Update / Edit Task**
   - Reuses the same Add/Edit form
   - Existing task details are pre-filled

4. **Delete Task**
   - Requires confirmation before permanent deletion

## Technology

- Python 3
- PyQt6
- JSON local storage
- Object-oriented code structure
- `unittest` for automated testing

## Project Structure

```text
StudyTrack/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── tasks.json
├── src/
│   ├── main.py
│   ├── gui.py
│   ├── logic.py
│   └── data_handler.py
└── tests/
    └── test_functions.py
```

## How to Run

### 1. Open a terminal in the StudyTrack folder

### 2. Create a virtual environment (recommended)

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Start StudyTrack

Windows:

```bash
python src/main.py
```

macOS / Linux:

```bash
python3 src/main.py
```

## Run Automated Tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

The tests verify:
- adding a task and saving it to JSON
- viewing tasks in due-date order
- updating task details
- deleting a task
- rejecting invalid input

## Suggested Live Demonstration

1. Start the program.
2. Click **+ Add Task**.
3. Add:
   - Task: `Software Development Assessment`
   - Subject: `IT2000`
   - Due date: choose a valid date
   - Priority: `High`
4. Save it.
5. Show that it appears in the list.
6. Select it and click **Edit Selected**.
7. Change the due date or priority.
8. Save and show the updated task.
9. Select it and click **Delete Selected**.
10. Show the confirmation dialog and delete it.
11. Open `data/tasks.json` to explain local persistence.
12. Run the tests in the terminal.

## Assessment 3 Alignment

The implementation deliberately follows the Assessment 3 specification:

- The application remains a **single-student personal organisation tool**.
- The client priorities remain **ease of use** and **easy navigation**.
- The four required functions are **Add, View, Update and Delete**.
- The task list is automatically **sorted by due date**.
- The **Add/Edit form is reused** for Create and Update.
- The priority choices are **Low, Medium and High**.
- Delete requires a **confirmation**.
- Data is stored locally in a **JSON file**.
- The GUI is built with **Python + PyQt6**.
- The program does not add unrelated LMS, grades, enrolment or communication features.

## Testing Approach

Automated tests are used for the business logic because they are fast and repeatable.
The GUI should also be manually tested before presentation.

Recommended manual checks:
- application launches normally
- Add Task opens the form
- required fields cannot be left blank
- a valid task appears after saving
- tasks display in chronological due-date order
- Edit loads the selected task's existing data
- edited values remain after saving
- Delete asks for confirmation
- choosing No keeps the task
- choosing Yes removes the task
- tasks remain after closing and reopening the program

## Suggested Git Commit Plan

Each group member should make meaningful commits. Examples:

- `Set up StudyTrack project structure`
- `Implement JSON data handler`
- `Implement CRUD task manager`
- `Build PyQt6 task dashboard`
- `Add reusable task add edit dialog`
- `Add delete confirmation`
- `Add task input validation`
- `Add automated CRUD tests`
- `Improve GUI layout and priority indicators`
- `Update README and demo instructions`

Do not use meaningless commit messages such as `update`, `fix`, or `changes`.

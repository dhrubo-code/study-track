"""
StudyTrack PyQt6 graphical user interface.

The interface follows the Assessment 3 design:
- Main task dashboard
- Tasks sorted by due date
- One reusable Add/Edit Task dialog
- Priority indicator
- Simple navigation and minimal steps
"""

from __future__ import annotations

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from logic import TaskManager


class TaskDialog(QDialog):
    """Reusable form used by both Add Task and Update Task."""

    def __init__(self, parent=None, task: dict | None = None):
        super().__init__(parent)
        self.task = task
        self.setWindowTitle("Edit Task" if task else "Add Task")
        self.setMinimumWidth(430)

        self.name_input = QLineEdit()
        self.subject_input = QLineEdit()

        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDisplayFormat("dd/MM/yyyy")
        self.due_date_input.setDate(QDate.currentDate())

        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes")
        self.notes_input.setMaximumHeight(90)

        form = QFormLayout()
        form.addRow("Task Name:", self.name_input)
        form.addRow("Subject / Unit Code:", self.subject_input)
        form.addRow("Due Date:", self.due_date_input)
        form.addRow("Priority:", self.priority_input)
        form.addRow("Notes:", self.notes_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        heading = QLabel("Add / Edit Task")
        heading.setObjectName("dialogHeading")
        layout.addWidget(heading)
        layout.addLayout(form)
        layout.addWidget(buttons)

        if task:
            self.populate(task)

    def populate(self, task: dict) -> None:
        self.name_input.setText(task.get("name", ""))
        self.subject_input.setText(task.get("subject", ""))
        parsed = QDate.fromString(task.get("due_date", ""), "dd/MM/yyyy")
        if parsed.isValid():
            self.due_date_input.setDate(parsed)
        self.priority_input.setCurrentText(task.get("priority", "Medium"))
        self.notes_input.setPlainText(task.get("notes", ""))

    def get_data(self) -> dict:
        return {
            "name": self.name_input.text(),
            "subject": self.subject_input.text(),
            "due_date": self.due_date_input.date().toString("dd/MM/yyyy"),
            "priority": self.priority_input.currentText(),
            "notes": self.notes_input.toPlainText(),
        }

    def validate_and_accept(self) -> None:
        data = self.get_data()
        try:
            TaskManager.validate_task_fields(
                data["name"],
                data["subject"],
                data["due_date"],
                data["priority"],
            )
        except ValueError as error:
            QMessageBox.warning(self, "Invalid Task", str(error))
            return
        self.accept()


class StudyTrackWindow(QMainWindow):
    """Main StudyTrack dashboard."""

    def __init__(self, task_manager: TaskManager):
        super().__init__()
        self.task_manager = task_manager

        self.setWindowTitle("StudyTrack")
        self.resize(900, 560)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Task", "Subject", "Due Date", "Priority"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.doubleClicked.connect(self.edit_selected_task)

        self.add_button = QPushButton("+ Add Task")
        self.edit_button = QPushButton("Edit Selected")
        self.delete_button = QPushButton("Delete Selected")

        self.add_button.clicked.connect(self.add_task)
        self.edit_button.clicked.connect(self.edit_selected_task)
        self.delete_button.clicked.connect(self.delete_selected_task)

        self.build_ui()
        self.apply_styles()
        self.refresh_table()

    def build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        outer = QHBoxLayout(root)

        # Left navigation mirrors the Assessment 3 wireframe.
        sidebar = QVBoxLayout()
        logo = QLabel("StudyTrack")
        logo.setObjectName("logo")
        sidebar.addWidget(logo)

        home = QLabel("Home")
        tasks = QLabel("My Tasks")
        tasks.setObjectName("activeNav")
        sidebar.addWidget(home)
        sidebar.addWidget(tasks)
        sidebar.addStretch()

        sidebar_container = QWidget()
        sidebar_container.setObjectName("sidebar")
        sidebar_container.setFixedWidth(170)
        sidebar_container.setLayout(sidebar)

        content = QVBoxLayout()

        header = QHBoxLayout()
        title = QLabel("Upcoming Tasks")
        title.setObjectName("pageTitle")
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.add_button)

        content.addLayout(header)
        content.addWidget(self.table)

        actions = QHBoxLayout()
        actions.addStretch()
        actions.addWidget(self.edit_button)
        actions.addWidget(self.delete_button)
        content.addLayout(actions)

        outer.addWidget(sidebar_container)
        outer.addLayout(content, 1)

    def apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background: #f7f8fb;
                color: #222;
                font-size: 13px;
            }
            #sidebar {
                background: #eef2f8;
                padding: 18px;
                border-right: 1px solid #d9dee8;
            }
            #logo {
                font-size: 22px;
                font-weight: 700;
                padding-bottom: 18px;
            }
            #activeNav {
                background: #dce8fb;
                padding: 10px;
                border-radius: 6px;
                font-weight: 600;
            }
            #pageTitle, #dialogHeading {
                font-size: 20px;
                font-weight: 700;
            }
            QPushButton {
                padding: 8px 14px;
                border: 1px solid #c7ceda;
                border-radius: 6px;
                background: white;
            }
            QPushButton:hover {
                background: #eef4ff;
            }
            QTableWidget {
                background: white;
                border: 1px solid #d9dee8;
                border-radius: 6px;
                gridline-color: #edf0f5;
            }
            QHeaderView::section {
                background: #eef2f8;
                border: none;
                padding: 8px;
                font-weight: 600;
            }
            """
        )

    def selected_task_id(self) -> int | None:
        row = self.table.currentRow()
        if row < 0:
            return None

        item = self.table.item(row, 0)
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def refresh_table(self) -> None:
        tasks = self.task_manager.get_tasks_sorted()
        self.table.setRowCount(len(tasks))

        priority_colours = {
            "Low": QColor("#dff3e4"),
            "Medium": QColor("#fff1c9"),
            "High": QColor("#ffd9d9"),
        }

        for row, task in enumerate(tasks):
            task_item = QTableWidgetItem(task["name"])
            task_item.setData(Qt.ItemDataRole.UserRole, task["id"])

            subject_item = QTableWidgetItem(task["subject"])
            due_item = QTableWidgetItem(task["due_date"])
            priority_item = QTableWidgetItem(task["priority"])
            priority_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            colour = priority_colours.get(task["priority"])
            if colour:
                priority_item.setBackground(colour)

            self.table.setItem(row, 0, task_item)
            self.table.setItem(row, 1, subject_item)
            self.table.setItem(row, 2, due_item)
            self.table.setItem(row, 3, priority_item)

    def add_task(self) -> None:
        dialog = TaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.task_manager.add_task(**dialog.get_data())
                self.refresh_table()
            except ValueError as error:
                QMessageBox.warning(self, "Unable to Add Task", str(error))

    def edit_selected_task(self) -> None:
        task_id = self.selected_task_id()
        if task_id is None:
            QMessageBox.information(self, "Select a Task", "Please select a task to edit.")
            return

        task = self.task_manager.get_task(task_id)
        if task is None:
            QMessageBox.warning(self, "Task Not Found", "The selected task no longer exists.")
            self.refresh_table()
            return

        dialog = TaskDialog(self, task)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.task_manager.update_task(task_id, **dialog.get_data())
                self.refresh_table()
            except ValueError as error:
                QMessageBox.warning(self, "Unable to Update Task", str(error))

    def delete_selected_task(self) -> None:
        task_id = self.selected_task_id()
        if task_id is None:
            QMessageBox.information(self, "Select a Task", "Please select a task to delete.")
            return

        task = self.task_manager.get_task(task_id)
        if task is None:
            QMessageBox.warning(self, "Task Not Found", "The selected task no longer exists.")
            self.refresh_table()
            return

        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            f'Delete "{task["name"]}"?\n\nThis action cannot be undone.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            try:
                self.task_manager.delete_task(task_id)
                self.refresh_table()
            except ValueError as error:
                QMessageBox.warning(self, "Unable to Delete Task", str(error))

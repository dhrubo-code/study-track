"""
StudyTrack business logic.

Implements the four CRUD operations required by Assessment 4:
Create, Read, Update and Delete.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from data_handler import DataHandler


class TaskManager:
    """Manage task creation, retrieval, update, deletion and sorting."""

    VALID_PRIORITIES = {"Low", "Medium", "High"}
    DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler
        self.tasks = self.data_handler.load_tasks()

    def _next_id(self) -> int:
        if not self.tasks:
            return 1
        return max(int(task.get("id", 0)) for task in self.tasks) + 1

    @classmethod
    def validate_task_fields(
        cls,
        name: str,
        subject: str,
        due_date: str,
        priority: str,
    ) -> None:
        """Validate user-entered task fields and raise ValueError if invalid."""
        if not name.strip():
            raise ValueError("Task name is required.")

        if not subject.strip():
            raise ValueError("Subject / unit code is required.")

        try:
            datetime.strptime(due_date, cls.DATE_FORMAT)
        except ValueError as exc:
            raise ValueError("Due date must use DD/MM/YYYY format.") from exc

        if priority not in cls.VALID_PRIORITIES:
            raise ValueError("Priority must be Low, Medium or High.")

    def add_task(
        self,
        name: str,
        subject: str,
        due_date: str,
        priority: str,
        notes: str = "",
    ) -> dict[str, Any]:
        """CREATE: add a new task and save it."""
        self.validate_task_fields(name, subject, due_date, priority)

        task = {
            "id": self._next_id(),
            "name": name.strip(),
            "subject": subject.strip(),
            "due_date": due_date,
            "priority": priority,
            "notes": notes.strip(),
            "completed": False,
        }
        self.tasks.append(task)
        self.data_handler.save_tasks(self.tasks)
        return task

    def get_tasks_sorted(self) -> list[dict[str, Any]]:
        """READ: return all tasks ordered by due date, earliest first."""
        def sort_key(task: dict[str, Any]) -> datetime:
            try:
                return datetime.strptime(task["due_date"], self.DATE_FORMAT)
            except (KeyError, TypeError, ValueError):
                return datetime.max

        return sorted(self.tasks, key=sort_key)

    def get_task(self, task_id: int) -> dict[str, Any] | None:
        """Return one task by ID, or None if it does not exist."""
        return next((task for task in self.tasks if task.get("id") == task_id), None)

    def update_task(
        self,
        task_id: int,
        name: str,
        subject: str,
        due_date: str,
        priority: str,
        notes: str = "",
    ) -> dict[str, Any]:
        """UPDATE: change an existing task and save it."""
        self.validate_task_fields(name, subject, due_date, priority)

        task = self.get_task(task_id)
        if task is None:
            raise ValueError("Task not found.")

        task.update(
            {
                "name": name.strip(),
                "subject": subject.strip(),
                "due_date": due_date,
                "priority": priority,
                "notes": notes.strip(),
            }
        )
        self.data_handler.save_tasks(self.tasks)
        return task

    def delete_task(self, task_id: int) -> None:
        """DELETE: remove a task and save the updated list."""
        task = self.get_task(task_id)
        if task is None:
            raise ValueError("Task not found.")

        self.tasks.remove(task)
        self.data_handler.save_tasks(self.tasks)

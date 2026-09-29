"""
StudyTrack - JSON data persistence.

This module is responsible only for loading and saving task data.
Keeping file handling separate makes the code easier to test and maintain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class DataHandler:
    """Read and write StudyTrack task data to a local JSON file."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_tasks(self) -> list[dict[str, Any]]:
        """Return all tasks from JSON. If no file exists, return an empty list."""
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            # For this small educational project, fail safely with an empty list.
            return []

        return data if isinstance(data, list) else []

    def save_tasks(self, tasks: list[dict[str, Any]]) -> None:
        """Persist the complete task list to the JSON file."""
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2, ensure_ascii=False)

"""
Automated tests for StudyTrack core functionality.

These tests focus on the non-GUI logic so they can run reliably on any machine.
They verify Create, Read/sorting, Update, Delete and validation.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from data_handler import DataHandler
from logic import TaskManager


class StudyTrackTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "tasks.json"
        self.manager = TaskManager(DataHandler(self.data_file))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_task_saves_to_json(self):
        task = self.manager.add_task(
            name="Statistics Assignment 3",
            subject="IT1010",
            due_date="21/09/2026",
            priority="High",
            notes="Submit before 11:59 PM",
        )

        self.assertEqual(task["name"], "Statistics Assignment 3")
        self.assertTrue(self.data_file.exists())

        saved = json.loads(self.data_file.read_text(encoding="utf-8"))
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["priority"], "High")

    def test_view_tasks_are_sorted_by_due_date(self):
        self.manager.add_task("Later Task", "IT2000", "30/09/2026", "Low")
        self.manager.add_task("Earlier Task", "IT2030", "13/09/2026", "Medium")
        self.manager.add_task("Middle Task", "IT1010", "21/09/2026", "High")

        sorted_tasks = self.manager.get_tasks_sorted()
        self.assertEqual(
            [task["name"] for task in sorted_tasks],
            ["Earlier Task", "Middle Task", "Later Task"],
        )

    def test_update_task_changes_existing_record(self):
        task = self.manager.add_task(
            "Security Investigation Report",
            "IT2030",
            "13/09/2026",
            "Medium",
        )

        updated = self.manager.update_task(
            task["id"],
            "Security Investigation Report",
            "IT2030",
            "20/09/2026",
            "High",
            "Extension approved",
        )

        self.assertEqual(updated["due_date"], "20/09/2026")
        self.assertEqual(updated["priority"], "High")
        self.assertEqual(updated["notes"], "Extension approved")

    def test_delete_task_removes_record(self):
        task = self.manager.add_task(
            "Read Chapter 6 lecture notes",
            "IT2000",
            "30/09/2026",
            "Low",
        )

        self.manager.delete_task(task["id"])

        self.assertEqual(self.manager.get_tasks_sorted(), [])
        saved = json.loads(self.data_file.read_text(encoding="utf-8"))
        self.assertEqual(saved, [])

    def test_invalid_empty_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add_task(
                "",
                "IT2000",
                "30/09/2026",
                "Low",
            )

    def test_invalid_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add_task(
                "Example",
                "IT2000",
                "30/09/2026",
                "Urgent",
            )

    def test_invalid_date_is_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add_task(
                "Example",
                "IT2000",
                "2026-09-30",
                "High",
            )


if __name__ == "__main__":
    unittest.main()

"""StudyTrack application entry point."""

from pathlib import Path
import sys

from PyQt6.QtWidgets import QApplication

from data_handler import DataHandler
from gui import StudyTrackWindow
from logic import TaskManager


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    data_file = project_root / "data" / "tasks.json"

    app = QApplication(sys.argv)

    data_handler = DataHandler(data_file)
    task_manager = TaskManager(data_handler)
    window = StudyTrackWindow(task_manager)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

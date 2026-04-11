from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from canada_tracker.services.app_service import AppService
from canada_tracker.ui.main_window import MainWindow


def run() -> None:
    app = QApplication(sys.argv)
    service = AppService()
    window = MainWindow(service)
    window.show()
    sys.exit(app.exec())

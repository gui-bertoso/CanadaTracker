from __future__ import annotations

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QColor, QTextCharFormat
from PySide6.QtWidgets import QCalendarWidget


class ProgressCalendar(QCalendarWidget):
    COLORS = {
        "good": ("#143320", "#5fe087"),
        "mid": ("#3b3413", "#f1cb57"),
        "low": ("#30191c", "#f17a7a"),
    }

    def __init__(self) -> None:
        super().__init__()
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setNavigationBarVisible(True)
        self._default_format = QTextCharFormat()
        self._painted_dates: set[str] = set()
        self.setMinimumHeight(290)
        self._apply_theme()

    def _apply_theme(self) -> None:
        weekday = QTextCharFormat()
        weekday.setForeground(QColor("#d8e5f2"))
        weekend = QTextCharFormat()
        weekend.setForeground(QColor("#7fb8ff"))
        self.setWeekdayTextFormat(Qt.Monday, weekday)
        self.setWeekdayTextFormat(Qt.Tuesday, weekday)
        self.setWeekdayTextFormat(Qt.Wednesday, weekday)
        self.setWeekdayTextFormat(Qt.Thursday, weekday)
        self.setWeekdayTextFormat(Qt.Friday, weekday)
        self.setWeekdayTextFormat(Qt.Saturday, weekend)
        self.setWeekdayTextFormat(Qt.Sunday, weekend)
        self.setStyleSheet(
            """
            QCalendarWidget {
                background: #0f151d;
                border: 1px solid #233242;
                border-radius: 14px;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: #121c27;
                border-bottom: 1px solid #213141;
                min-height: 36px;
                border-top-left-radius: 14px;
                border-top-right-radius: 14px;
            }
            QCalendarWidget QToolButton {
                color: #e8f1fb;
                background: transparent;
                border: none;
                font-size: 16px;
                font-weight: 700;
                padding: 6px 10px;
            }
            QCalendarWidget QToolButton:hover {
                background: #182534;
                border-radius: 8px;
            }
            QCalendarWidget QMenu {
                background: #111821;
                color: #e8f1fb;
                border: 1px solid #233242;
            }
            QCalendarWidget QSpinBox {
                background: #182330;
                color: #e8f1fb;
                border: 1px solid #2a3c4f;
                border-radius: 8px;
                padding: 2px 6px;
            }
            QCalendarWidget QAbstractItemView {
                background: #0f151d;
                color: #e8f1fb;
                selection-background-color: #1d3246;
                selection-color: #ffffff;
                outline: 0;
                border: none;
                gridline-color: #192632;
            }
            """
        )

    def apply_scores(self, score_map: dict[str, dict[str, object]]) -> None:
        for iso_date in self._painted_dates:
            qdate = QDate.fromString(iso_date, "yyyy-MM-dd")
            if qdate.isValid():
                self.setDateTextFormat(qdate, self._default_format)
        self._painted_dates = set(score_map.keys())
        for iso_date, payload in score_map.items():
            qdate = QDate.fromString(iso_date, "yyyy-MM-dd")
            if not qdate.isValid():
                continue
            kind = str(payload.get("classification", "low"))
            bg, fg = self.COLORS.get(kind, self.COLORS["low"])
            fmt = QTextCharFormat()
            fmt.setBackground(QColor(bg))
            fmt.setForeground(QColor(fg))
            fmt.setFontWeight(700)
            self.setDateTextFormat(qdate, fmt)

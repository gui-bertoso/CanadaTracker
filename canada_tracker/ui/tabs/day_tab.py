from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QScrollArea, QVBoxLayout, QWidget

from canada_tracker.ui.tabs.english_tab import EnglishTab
from canada_tracker.ui.tabs.habits_tab import HabitsTab
from canada_tracker.ui.tabs.profits_tab import ProfitsTab


class DayTab(QWidget):
    def __init__(self, on_profit_save, on_english_save, on_habits_save, on_date_selected) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        nav = QHBoxLayout()
        nav.setContentsMargins(10, 8, 10, 0)
        nav.setSpacing(8)
        self.profits_button = QPushButton('earnings')
        self.english_button = QPushButton('English')
        self.habits_button = QPushButton('day')
        for button in (self.profits_button, self.english_button, self.habits_button):
            button.setProperty("secondary", True)
            nav.addWidget(button)
        nav.addStretch(1)
        layout.addLayout(nav)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.scroll = scroll
        layout.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(6)

        self.profits_tab = ProfitsTab(on_profit_save, compact=True)
        self.english_tab = EnglishTab(on_english_save, compact=True)
        self.habits_tab = HabitsTab(on_habits_save, on_date_selected, compact=True)

        content_layout.addWidget(self.profits_tab)
        content_layout.addWidget(self.english_tab)
        content_layout.addWidget(self.habits_tab)
        content_layout.addStretch(1)

        self.profits_button.clicked.connect(lambda: self._scroll_to(self.profits_tab))
        self.english_button.clicked.connect(lambda: self._scroll_to(self.english_tab))
        self.habits_button.clicked.connect(lambda: self._scroll_to(self.habits_tab))

    def _scroll_to(self, widget: QWidget) -> None:
        bar = self.scroll.verticalScrollBar()
        bar.setValue(widget.pos().y())

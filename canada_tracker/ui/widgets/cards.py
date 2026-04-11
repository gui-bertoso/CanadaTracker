from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class MetricCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str = "") -> None:
        super().__init__()
        self.setProperty("card", True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(6)
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #8ea0b2; font-size: 12px;")
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 28px; font-weight: 700; color: #ffffff;")
        self.value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setStyleSheet("color: #7e8d9b;")
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)

    def update_content(self, title: str, value: str, subtitle: str = "") -> None:
        self.title_label.setText(title)
        self.value_label.setText(value)
        self.subtitle_label.setText(subtitle)


class HeaderMetricCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str = "") -> None:
        super().__init__()
        self.setProperty("headerCard", True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(4)
        self.title_label = QLabel(title)
        self.title_label.setProperty("headerLabel", True)
        self.value_label = QLabel(value)
        self.value_label.setProperty("headerValue", True)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setProperty("muted", True)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setVisible(bool(subtitle))
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)

    def update_content(self, title: str, value: str, subtitle: str = "") -> None:
        self.title_label.setText(title)
        self.value_label.setText(value)
        self.subtitle_label.setText(subtitle)
        self.subtitle_label.setVisible(bool(subtitle))


class SectionCard(QFrame):
    def __init__(self, title: str, description: str = "") -> None:
        super().__init__()
        self.setProperty("card", True)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)
        self.title_label = QLabel(title)
        self.title_label.setProperty("section", True)
        self.layout.addWidget(self.title_label)
        self.description_label = QLabel(description)
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("color: #8ea0b2;")
        if description:
            self.layout.addWidget(self.description_label)

    def set_description(self, description: str) -> None:
        self.description_label.setText(description)
        self.description_label.setVisible(bool(description))

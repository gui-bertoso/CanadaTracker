from __future__ import annotations

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QDateEdit,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from canada_tracker.ui.widgets.cards import MetricCard, SectionCard
from canada_tracker.ui.widgets.charts import line_chart


class EnglishTab(QWidget):
    def __init__(self, on_save, compact: bool = False) -> None:
        super().__init__()
        self.on_save = on_save
        self.compact = compact
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12 if compact else 16, 12 if compact else 16, 12 if compact else 16, 12 if compact else 16)
        layout.setSpacing(10 if compact else 16)
        title = QLabel('English' if compact else 'English')
        title.setProperty("section" if compact else "title", True)
        layout.addWidget(title)
        self.summary = QLabel()
        self.summary.setWordWrap(True)
        self.summary.setProperty("muted", True)
        layout.addWidget(self.summary)

        cards_row = QHBoxLayout()
        self.total_card = MetricCard('Total time', "0h")
        self.days_card = MetricCard('Study Days', "0")
        self.streak_card = MetricCard("Streak", "0")
        self.goal_card = MetricCard('Goal', "0%")
        cards_row.addWidget(self.total_card)
        cards_row.addWidget(self.days_card)
        cards_row.addWidget(self.streak_card)
        cards_row.addWidget(self.goal_card)
        if compact:
            for card in (self.total_card, self.days_card, self.streak_card, self.goal_card):
                card.setMinimumHeight(104)
                card.setMaximumHeight(104)
        layout.addLayout(cards_row)

        form_layout = QHBoxLayout()
        form_box = SectionCard('New Session', 'Record study type and duration to keep your consistency visible.')
        form = QFormLayout()
        self.minutes = QSpinBox()
        self.minutes.setMaximum(1440)
        self.study_type = QLineEdit()
        self.session_date = QDateEdit()
        self.session_date.setCalendarPopup(True)
        self.session_date.setDate(QDate.currentDate())
        self.note = QTextEdit()
        self.note.setFixedHeight(70)
        save_button = QPushButton('Save session')
        save_button.clicked.connect(self._handle_save)
        form.addRow('Minutes', self.minutes)
        form.addRow('Type', self.study_type)
        form.addRow('Date', self.session_date)
        form.addRow('Note', self.note)
        form.addRow("", save_button)
        form_box.layout.addLayout(form)
        form_layout.addWidget(form_box, 1)
        self.chart_card = SectionCard('English Progress')
        self.chart_container = QVBoxLayout()
        self.chart_card.layout.addLayout(self.chart_container)
        form_layout.addWidget(self.chart_card, 2)
        layout.addLayout(form_layout)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['Date', 'Type', 'Minutes', 'Note'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setMaximumHeight(180 if compact else 260)
        layout.addWidget(self.table)

    def _handle_save(self) -> None:
        if not self.study_type.text().strip():
            QMessageBox.warning(self, 'Validation', 'Enter the study type.')
            return
        self.on_save(
            self.minutes.value(),
            self.study_type.text(),
            self.session_date.date().toString("yyyy-MM-dd"),
            self.note.toPlainText(),
        )
        self.minutes.setValue(0)
        self.study_type.clear()
        self.note.clear()

    def refresh(self, sessions: list[dict[str, object]], metrics: dict[str, object]) -> None:
        goal_pct = metrics["english_minutes"] / max(int(metrics["settings"]["english_goal_minutes"]), 1) * 100
        self.total_card.update_content('Total time', f"{metrics['english_hours']:.1f}h", f"{metrics['english_minutes']} min")
        self.days_card.update_content('Study Days', str(metrics["english_days"]), 'Unique days')
        self.streak_card.update_content("Streak", str(metrics["english_streak"]), 'Consecutive days')
        self.goal_card.update_content('Goal', f"{goal_pct:.1f}%", f"Goal {int(metrics['settings']['english_goal_minutes'])} min")
        self.summary.setText(
            f"Current pace: {metrics['english_days']} study days and a streak of {metrics['english_streak']} days. "
            f"Remaining: {max(int(metrics['settings']['english_goal_minutes']) - metrics['english_minutes'], 0)} minutes toward the goal."
        )
        self.table.setRowCount(len(sessions))
        for row_index, entry in enumerate(sessions):
            self.table.setItem(row_index, 0, QTableWidgetItem(entry["session_date"]))
            self.table.setItem(row_index, 1, QTableWidgetItem(entry["study_type"]))
            self.table.setItem(row_index, 2, QTableWidgetItem(str(entry["duration_minutes"])))
            self.table.setItem(row_index, 3, QTableWidgetItem(entry["note"] or ""))
        while self.chart_container.count():
            item = self.chart_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        points = [(entry["session_date"], float(entry["duration_minutes"])) for entry in reversed(sessions[:12])]
        self.chart_container.addWidget(line_chart(points or [("2000-01-01", 0)], 'English Progress', "#91f2b5", 200 if self.compact else 240))

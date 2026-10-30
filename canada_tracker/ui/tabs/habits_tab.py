from __future__ import annotations

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QCheckBox,
    QDateEdit,
    QFrame,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QDoubleSpinBox,
)

from canada_tracker.ui.widgets.calendar import ProgressCalendar
from canada_tracker.ui.widgets.cards import MetricCard, SectionCard
from canada_tracker.ui.widgets.charts import bar_chart


class HabitsTab(QWidget):
    BOOLEAN_FIELDS = [
        ("water", 'Water'),
        ("ate_well", 'Food'),
        ("trained", 'Training'),
        ("studied_english", 'English'),
        ("worked_progress", 'Work'),
        ("slept_well", 'Sleep'),
        ("cardio", "Cardio"),
        ("mobility", "Hand grip / mobility"),
    ]

    def __init__(self, on_save, on_date_selected, compact: bool = False) -> None:
        super().__init__()
        self.on_save = on_save
        self.on_date_selected = on_date_selected
        self.compact = compact
        self.checkboxes: dict[str, QCheckBox] = {}
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12 if compact else 16, 12 if compact else 16, 12 if compact else 16, 12 if compact else 16)
        layout.setSpacing(10 if compact else 16)
        title = QLabel('day' if compact else "Daily log / health / habits")
        title.setProperty("section" if compact else "title", True)
        layout.addWidget(title)

        cards_row = QHBoxLayout()
        self.score_card = MetricCard('Daily Score', "0%")
        self.completed_card = MetricCard('Completed Habits', "0")
        self.streak_card = MetricCard('Good-Day Streak', "0")
        self.week_card = MetricCard('Weekly Average', "0%")
        cards_row.addWidget(self.score_card)
        cards_row.addWidget(self.completed_card)
        cards_row.addWidget(self.streak_card)
        cards_row.addWidget(self.week_card)
        if compact:
            for card in (self.score_card, self.completed_card, self.streak_card, self.week_card):
                card.setMinimumHeight(104)
                card.setMaximumHeight(104)
        layout.addLayout(cards_row)

        content_row = QHBoxLayout()
        form_widget = SectionCard('Daily Check-in', 'Check off completed activities and save the day.')
        form_layout = form_widget.layout
        date_row = QHBoxLayout()
        self.log_date = QDateEdit()
        self.log_date.setCalendarPopup(True)
        self.log_date.setDate(QDate.currentDate())
        load_button = QPushButton('Load day')
        load_button.setProperty("secondary", True)
        load_button.clicked.connect(self._load_current_date)
        date_row.addWidget(QLabel('Date'))
        date_row.addWidget(self.log_date)
        date_row.addWidget(load_button)
        form_layout.addLayout(date_row)

        checks_grid = QGridLayout()
        for index, (field, label) in enumerate(self.BOOLEAN_FIELDS):
            checkbox = QCheckBox(label)
            self.checkboxes[field] = checkbox
            checks_grid.addWidget(checkbox, index // 2, index % 2)
        form_layout.addLayout(checks_grid)

        extras = QFormLayout()
        self.mood = QSpinBox()
        self.mood.setRange(0, 10)
        self.weight = QDoubleSpinBox()
        self.weight.setMaximum(500)
        self.weight.setDecimals(1)
        self.note = QTextEdit()
        self.note.setFixedHeight(70)
        extras.addRow("Mood / energy", self.mood)
        extras.addRow('Weight', self.weight)
        extras.addRow('Note', self.note)
        form_layout.addLayout(extras)
        save_button = QPushButton('Save record')
        save_button.clicked.connect(self._handle_save)
        form_layout.addWidget(save_button)
        self.selected_day_badge = QLabel('No record')
        self.selected_day_badge.setProperty("pill", "low")
        form_layout.addWidget(self.selected_day_badge)
        content_row.addWidget(form_widget, 2)

        right_column = QVBoxLayout()
        calendar_card = SectionCard('Progress Calendar', "Verde = forte, amarelo = medio, vermelho = fraco.")
        self.calendar = ProgressCalendar()
        self.calendar.selectionChanged.connect(self._calendar_changed)
        calendar_card.layout.addWidget(self.calendar)
        right_column.addWidget(calendar_card)
        self.habit_chart_card = SectionCard('Weekly Habit Summary')
        self.habit_chart_layout = QVBoxLayout()
        self.habit_chart_card.layout.addLayout(self.habit_chart_layout)
        right_column.addWidget(self.habit_chart_card)
        self.summary_table = QTableWidget(0, 4)
        self.summary_table.setHorizontalHeaderLabels(['Date', "Score", 'Rating', 'Habits'])
        self.summary_table.horizontalHeader().setStretchLastSection(True)
        self.summary_table.setAlternatingRowColors(True)
        self.summary_table.setMaximumHeight(180 if compact else 260)
        right_column.addWidget(self.summary_table)
        content_row.addLayout(right_column, 3)
        layout.addLayout(content_row)

    def _calendar_changed(self) -> None:
        self.log_date.setDate(self.calendar.selectedDate())
        self._load_current_date()

    def _load_current_date(self) -> None:
        self.on_date_selected(self.log_date.date().toString("yyyy-MM-dd"))

    def load_log(self, log: dict[str, object] | None) -> None:
        for field, checkbox in self.checkboxes.items():
            checkbox.setChecked(bool(log and int(log.get(field, 0) or 0)))
        self.mood.setValue(int(log.get("mood", 0) or 0) if log else 0)
        self.weight.setValue(float(log.get("weight", 0) or 0.0) if log else 0.0)
        self.note.setPlainText(str(log.get("note", "")) if log else "")

    def _handle_save(self) -> None:
        payload = {
            "log_date": self.log_date.date().toString("yyyy-MM-dd"),
            "mood": self.mood.value() or None,
            "weight": self.weight.value() or None,
            "note": self.note.toPlainText(),
        }
        for field in self.checkboxes:
            payload[field] = int(self.checkboxes[field].isChecked())
        self.on_save(payload)
        QMessageBox.information(self, 'Record saved', 'The daily record was saved.')

    def refresh(self, metrics: dict[str, object], calendar_scores: dict[str, dict[str, object]], selected_log: dict[str, object] | None) -> None:
        reference = selected_log or metrics["today_log"] or (metrics["recent_logs"][0] if metrics["recent_logs"] else None)
        self.score_card.update_content('Daily Score', f"{(reference or {}).get('score', 0)}%", 'Selected date')
        self.completed_card.update_content('Completed Habits', str((reference or {}).get("completed_habits", 0)), 'Selected date')
        self.streak_card.update_content('Good-Day Streak', str(metrics["good_day_streak"]), 'Consecutive days')
        self.week_card.update_content('Weekly Average', f"{metrics['average_daily_score']:.1f}%", f"Completion {metrics['weekly_completion_rate']:.1f}%")
        self.calendar.apply_scores(calendar_scores)
        self.load_log(selected_log)
        classification = (reference or {}).get("classification", "low")
        self.selected_day_badge.setText(
            'Strong day' if classification == "good" else 'Average day' if classification == "mid" else 'Low or empty day'
        )
        self.selected_day_badge.setProperty("pill", classification)
        self.selected_day_badge.style().unpolish(self.selected_day_badge)
        self.selected_day_badge.style().polish(self.selected_day_badge)
        logs = metrics["monthly_logs"][:12]
        self.summary_table.setRowCount(len(logs))
        for row_index, log in enumerate(logs):
            self.summary_table.setItem(row_index, 0, QTableWidgetItem(log["log_date"]))
            self.summary_table.setItem(row_index, 1, QTableWidgetItem(f"{log['score']}%"))
            self.summary_table.setItem(row_index, 2, QTableWidgetItem(log["classification"]))
            self.summary_table.setItem(row_index, 3, QTableWidgetItem(str(log["completed_habits"])))
        while self.habit_chart_layout.count():
            item = self.habit_chart_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        labels = ['Water', "Food", 'Training', 'English', 'Work', 'Sleep', "Cardio", "Mob."]
        ordered_fields = ["water", "ate_well", "trained", "studied_english", "worked_progress", "slept_well", "cardio", "mobility"]
        values = [float(metrics["weekly_habit_totals"].get(field, 0)) for field in ordered_fields]
        self.habit_chart_layout.addWidget(bar_chart(labels, values, 'Weekly Habit Check-ins', "#91f2b5", 180 if self.compact else 240))

from __future__ import annotations

from datetime import date, timedelta

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from canada_tracker.ui.widgets.cards import SectionCard
from canada_tracker.ui.widgets.charts import multi_line_chart


class DashboardTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(8)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        self.summary_card = SectionCard('overall summary')
        self.summary_card.setFixedHeight(128)
        self.summary_card.layout.setContentsMargins(16, 12, 16, 12)
        self.summary_card.layout.setSpacing(6)
        self.summary_text = QLabel()
        self.summary_text.setWordWrap(True)
        self.summary_text.setProperty("muted", True)
        self.summary_text.setStyleSheet("font-size: 13px;")
        self.summary_text.setMinimumHeight(56)
        self.summary_text.setMaximumHeight(56)
        self.summary_text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.summary_card.layout.addWidget(self.summary_text)
        top_row.addWidget(self.summary_card, 2)

        self.latest_card = SectionCard('recent achievements')
        self.latest_card.setFixedHeight(128)
        self.latest_card.layout.setContentsMargins(16, 12, 16, 12)
        self.latest_card.layout.setSpacing(6)
        self.latest_text = QLabel()
        self.latest_text.setWordWrap(True)
        self.latest_text.setProperty("muted", True)
        self.latest_text.setStyleSheet("font-size: 13px;")
        self.latest_text.setMinimumHeight(56)
        self.latest_text.setMaximumHeight(56)
        self.latest_text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.latest_card.layout.addWidget(self.latest_text)
        top_row.addWidget(self.latest_card, 1)
        self.layout.addLayout(top_row)

        self.chart_grid = QGridLayout()
        self.chart_grid.setSpacing(10)
        self.layout.addLayout(self.chart_grid)

        lower_row = QHBoxLayout()
        lower_row.setSpacing(10)
        self.activity_card = SectionCard('current week')
        self.activity_text = QLabel()
        self.activity_text.setWordWrap(True)
        self.activity_text.setProperty("muted", True)
        self.activity_text.setMinimumHeight(96)
        self.activity_text.setMaximumHeight(96)
        self.activity_card.layout.addWidget(self.activity_text)
        lower_row.addWidget(self.activity_card, 1)

        self.goal_card = SectionCard('platforms')
        self.goal_text = QLabel()
        self.goal_text.setWordWrap(True)
        self.goal_text.setProperty("muted", True)
        self.goal_text.setMinimumHeight(96)
        self.goal_text.setMaximumHeight(96)
        self.goal_card.layout.addWidget(self.goal_text)
        lower_row.addWidget(self.goal_card, 1)

        self.save_card = SectionCard("save")
        self.save_text = QLabel()
        self.save_text.setWordWrap(True)
        self.save_text.setProperty("muted", True)
        self.save_text.setMinimumHeight(96)
        self.save_text.setMaximumHeight(96)
        self.save_card.layout.addWidget(self.save_text)
        lower_row.addWidget(self.save_card, 1)
        self.layout.addLayout(lower_row)

    def refresh(self, data: dict[str, object], achievements: list[dict[str, object]]) -> None:
        settings = data["settings"]
        self.summary_text.setText(
            "\n".join(
                [
                    f"earned: ${data['profit_total']:.2f}   |   remaining: ${max(float(settings['financial_goal']) - data['profit_total'], 0):.2f}",
                    f"entries: {data['profit_entries']}   |   accumulated focus: {data['english_hours']:.1f}h   |   English: {data['english_minutes']} min",
                    f"English streak: {data['english_streak']}   |   good days: {data['good_day_streak']}   |   weekly average: {data['average_daily_score']:.1f}%",
                    f"current level: {data['english_hours']:.1f}/{round(int(settings['english_goal_minutes']) / 60, 1)}h",
                ]
            )
        )
        recent_unlocked = sorted(
            [item for item in achievements if item["unlocked"]],
            key=lambda item: item["unlocked_at"],
            reverse=True,
        )[:5]
        if not recent_unlocked:
            self.latest_text.setText('no badges yet; time to start farming.')
        else:
            self.latest_text.setText(
                "\n".join(f"{item['unlocked_at'][:10]}  {item['name']}" for item in recent_unlocked[:3])
            )
        self._replace_charts(data)
        self._fill_activity(data["recent_activity"])
        self._fill_platforms(data)
        self._fill_save(data)

    def _replace_charts(self, data: dict[str, object]) -> None:
        while self.chart_grid.count():
            item = self.chart_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        chart_height = 220
        today = date.today()
        days = [today - timedelta(days=offset) for offset in range(29, -1, -1)]
        day_labels = [day.isoformat() for day in days]
        profit_totals: dict[str, float] = {label: 0.0 for label in day_labels}
        cumulative = 0.0
        for row in sorted(data["recent_profits"], key=lambda item: item["entry_date"]):
            if row["entry_date"] in profit_totals:
                profit_totals[row["entry_date"]] += float(row["amount"])
        profit_real_points = []
        for label in day_labels:
            cumulative += profit_totals[label]
            profit_real_points.append((label, cumulative))
        target_total = float(data["settings"]["financial_goal"])
        profit_ideal_points = []
        for index, label in enumerate(day_labels, start=1):
            profit_ideal_points.append((label, (target_total / len(day_labels)) * index))
        english_minutes_daily: dict[str, float] = {label: 0.0 for label in day_labels}
        for row in sorted(data["recent_english"], key=lambda item: item["session_date"]):
            if row["session_date"] in english_minutes_daily:
                english_minutes_daily[row["session_date"]] += float(row["duration_minutes"])
        english_real_points = []
        english_cumulative_hours = 0.0
        for label in day_labels:
            english_cumulative_hours += english_minutes_daily[label] / 60.0
            english_real_points.append((label, english_cumulative_hours))
        english_target_hours = int(data["settings"]["english_goal_minutes"]) / 60.0
        english_ideal_points = []
        for index, label in enumerate(day_labels, start=1):
            english_ideal_points.append((label, (english_target_hours / len(day_labels)) * index))
        profit_widget = multi_line_chart(
            [
                {"name": "real", "color": "#2de38b", "points": profit_real_points},
                {"name": "ideal", "color": "#f0d020", "points": profit_ideal_points, "style": "dashed"},
            ],
            'financial progress',
            chart_height,
            max(target_total, max((value for _, value in profit_real_points), default=0.0), 10),
        )
        english_widget = multi_line_chart(
            [
                {"name": 'actual level', "color": "#59d0ff", "points": english_real_points},
                {"name": 'goal pace', "color": "#b97dff", "points": english_ideal_points, "style": "dashed"},
            ],
            'English progress',
            chart_height,
            max(english_target_hours, max((value for _, value in english_real_points), default=0.0), 10),
        )
        self.chart_grid.addWidget(profit_widget, 0, 0)
        self.chart_grid.addWidget(english_widget, 1, 0)

    def _fill_activity(self, activity: list[dict[str, str]]) -> None:
        rows = activity[:4]
        if not rows:
            self.activity_text.setText("March 23 to today\n\nNo recent activity yet.\nStart by logging profit, English study or your day.")
            return
        lines = ["March 23 to today", ""]
        for item in rows:
            lines.append(f"{item['date']}  {item['type'].lower()}  {item['detail']}")
        self.activity_text.setText("\n".join(lines))

    def _fill_platforms(self, data: dict[str, object]) -> None:
        self.goal_text.setText(
            "\n".join(
                [
                    f"earnings: {data['profit_entries']}",
                    f"English days: {data['english_days']}",
                    f"green days: {data['good_days']}",
                    f"perfect days: {data['perfect_days']}",
                ]
            )
        )

    def _fill_save(self, data: dict[str, object]) -> None:
        db_path = Path(str(data["db_path"]))
        compact = str(db_path)
        if len(compact) > 44:
            compact = f".../{db_path.parent.name}/{db_path.name}"
        self.save_text.setText(
            "\n".join(
                [
                    'file:',
                    compact,
                ]
            )
        )

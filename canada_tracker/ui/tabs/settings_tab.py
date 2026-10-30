from __future__ import annotations

from canada_tracker.config import DEFAULT_SETTINGS
from canada_tracker.ui.widgets.cards import SectionCard
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QDoubleSpinBox,
    QVBoxLayout,
    QWidget,
)


class SettingsTab(QWidget):
    def __init__(self, on_save, on_reset_all) -> None:
        super().__init__()
        self.on_save = on_save
        self.on_reset_all = on_reset_all
        self.inputs: dict[str, object] = {}
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outer.addWidget(scroll)
        content = QWidget()
        scroll.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        title = QLabel('Settings')
        title.setProperty("title", True)
        layout.addWidget(title)

        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)
        self.summary_label.setProperty("muted", True)
        layout.addWidget(self.summary_label)

        numeric_fields = {
            "financial_goal": ('Financial goal', QDoubleSpinBox(), 1_000_000),
            "english_goal_minutes": ('English goal (min)', QSpinBox(), 100_000),
            "daily_water_goal": ('Daily water goal', QSpinBox(), 100),
            "daily_training_goal": ('Daily training goal', QSpinBox(), 100),
            "daily_food_goal": ('Daily food goal', QSpinBox(), 100),
            "daily_sleep_goal": ('Daily sleep goal', QSpinBox(), 100),
            "daily_work_goal": ('Daily work goal', QSpinBox(), 100),
            "daily_cardio_goal": ('Daily cardio goal', QSpinBox(), 100),
            "daily_mobility_goal": ('Daily mobility goal', QSpinBox(), 100),
            "score_threshold_good": ('Green threshold', QSpinBox(), 100),
            "score_threshold_mid": ('Yellow threshold', QSpinBox(), 100),
            "weight_water": ('Water weight', QSpinBox(), 100),
            "weight_food": ('Food weight', QSpinBox(), 100),
            "weight_training": ('Training weight', QSpinBox(), 100),
            "weight_english": ('English weight', QSpinBox(), 100),
            "weight_work": ('Work weight', QSpinBox(), 100),
            "weight_sleep": ('Sleep weight', QSpinBox(), 100),
            "weight_cardio": ('Cardio weight', QSpinBox(), 100),
            "weight_mobility": ('Mobility weight', QSpinBox(), 100),
        }
        groups = {
            'Main goals': [
                "financial_goal",
                "english_goal_minutes",
                "daily_water_goal",
                "daily_training_goal",
                "daily_food_goal",
                "daily_sleep_goal",
                "daily_work_goal",
                "daily_cardio_goal",
                "daily_mobility_goal",
            ],
            'Daily rating': [
                "score_threshold_good",
                "score_threshold_mid",
            ],
            'Score weights': [
                "weight_water",
                "weight_food",
                "weight_training",
                "weight_english",
                "weight_work",
                "weight_sleep",
                "weight_cardio",
                "weight_mobility",
            ],
        }
        for key, (_, widget, maximum) in numeric_fields.items():
            widget.setMaximum(maximum)
            self.inputs[key] = widget
            if hasattr(widget, "valueChanged"):
                widget.valueChanged.connect(self._update_summary)

        for group_title, field_names in groups.items():
            card = SectionCard(group_title)
            form = QFormLayout()
            for key in field_names:
                label, widget, _ = numeric_fields[key]
                form.addRow(label, widget)
            card.layout.addLayout(form)
            layout.addWidget(card)

        self.inputs["accent_color"] = QLineEdit()
        visuals_card = SectionCard('Appearance and persistence')
        form = QFormLayout()
        form.addRow('Accent color', self.inputs["accent_color"])

        db_row = QHBoxLayout()
        self.inputs["db_path"] = QLineEdit()
        browse = QPushButton('Select database')
        browse.setProperty("secondary", True)
        browse.clicked.connect(self._choose_db)
        db_row.addWidget(self.inputs["db_path"])
        db_row.addWidget(browse)
        form.addRow('Database path', db_row)
        visuals_card.layout.addLayout(form)
        layout.addWidget(visuals_card)

        actions = QHBoxLayout()
        reset_button = QPushButton('Restore defaults')
        reset_button.setProperty("secondary", True)
        reset_button.clicked.connect(self._restore_defaults)
        reset_all_button = QPushButton('Reset all')
        reset_all_button.setProperty("danger", True)
        reset_all_button.clicked.connect(self._confirm_reset_all)
        save_button = QPushButton('Save settings')
        save_button.clicked.connect(self._handle_save)
        actions.addWidget(reset_button)
        actions.addWidget(reset_all_button)
        actions.addWidget(save_button)
        layout.addLayout(actions)

    def _choose_db(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, 'Select database', "", "SQLite (*.db)")
        if path:
            self.inputs["db_path"].setText(path)

    def populate(self, settings: dict[str, object], db_path: str) -> None:
        for key, widget in self.inputs.items():
            if key == "db_path":
                widget.setText(db_path)
                continue
            value = settings.get(key, "")
            if hasattr(widget, "setValue"):
                widget.setValue(int(value) if isinstance(widget, QSpinBox) else float(value))
            else:
                widget.setText(str(value))
        self._update_summary()

    def _handle_save(self) -> None:
        payload = {}
        for key, widget in self.inputs.items():
            if hasattr(widget, "value"):
                payload[key] = widget.value()
            else:
                payload[key] = widget.text().strip()
        self.on_save(payload)
        QMessageBox.information(self, 'Settings', 'Settings saved. Restart the app if you changed the database.')

    def _restore_defaults(self) -> None:
        self.populate(DEFAULT_SETTINGS, self.inputs["db_path"].text())

    def _confirm_reset_all(self) -> None:
        answer = QMessageBox.warning(
            self,
            'Reset all',
            'This will delete all local data and close the app. Continue?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer == QMessageBox.Yes:
            self.on_reset_all()

    def _update_summary(self) -> None:
        weight_keys = [
            "weight_water",
            "weight_food",
            "weight_training",
            "weight_english",
            "weight_work",
            "weight_sleep",
            "weight_cardio",
            "weight_mobility",
        ]
        total = sum(int(self.inputs[key].value()) for key in weight_keys)
        good = int(self.inputs["score_threshold_good"].value())
        mid = int(self.inputs["score_threshold_mid"].value())
        self.summary_label.setText(
            f"Total weight: {total}. Aim for 100 to keep the score intuitive. "
            f"Current thresholds: green >= {good}, yellow >= {mid}, red below that."
        )

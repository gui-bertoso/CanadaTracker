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
        title = QLabel("Configuracoes")
        title.setProperty("title", True)
        layout.addWidget(title)

        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)
        self.summary_label.setProperty("muted", True)
        layout.addWidget(self.summary_label)

        numeric_fields = {
            "financial_goal": ("Meta financeira", QDoubleSpinBox(), 1_000_000),
            "english_goal_minutes": ("Meta de ingles (min)", QSpinBox(), 100_000),
            "daily_water_goal": ("Meta diaria de agua", QSpinBox(), 100),
            "daily_training_goal": ("Meta diaria de treino", QSpinBox(), 100),
            "daily_food_goal": ("Meta diaria de alimentacao", QSpinBox(), 100),
            "daily_sleep_goal": ("Meta diaria de sono", QSpinBox(), 100),
            "daily_work_goal": ("Meta diaria de trabalho", QSpinBox(), 100),
            "daily_cardio_goal": ("Meta diaria de cardio", QSpinBox(), 100),
            "daily_mobility_goal": ("Meta diaria de mobilidade", QSpinBox(), 100),
            "score_threshold_good": ("Limite verde", QSpinBox(), 100),
            "score_threshold_mid": ("Limite amarelo", QSpinBox(), 100),
            "weight_water": ("Peso agua", QSpinBox(), 100),
            "weight_food": ("Peso alimentacao", QSpinBox(), 100),
            "weight_training": ("Peso treino", QSpinBox(), 100),
            "weight_english": ("Peso ingles", QSpinBox(), 100),
            "weight_work": ("Peso trabalho", QSpinBox(), 100),
            "weight_sleep": ("Peso sono", QSpinBox(), 100),
            "weight_cardio": ("Peso cardio", QSpinBox(), 100),
            "weight_mobility": ("Peso mobilidade", QSpinBox(), 100),
        }
        groups = {
            "Metas principais": [
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
            "Classificacao diaria": [
                "score_threshold_good",
                "score_threshold_mid",
            ],
            "Pesos do score": [
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
        visuals_card = SectionCard("Visual e persistencia")
        form = QFormLayout()
        form.addRow("Cor de destaque", self.inputs["accent_color"])

        db_row = QHBoxLayout()
        self.inputs["db_path"] = QLineEdit()
        browse = QPushButton("Selecionar banco")
        browse.setProperty("secondary", True)
        browse.clicked.connect(self._choose_db)
        db_row.addWidget(self.inputs["db_path"])
        db_row.addWidget(browse)
        form.addRow("Caminho do banco", db_row)
        visuals_card.layout.addLayout(form)
        layout.addWidget(visuals_card)

        actions = QHBoxLayout()
        reset_button = QPushButton("Restaurar padrao")
        reset_button.setProperty("secondary", True)
        reset_button.clicked.connect(self._restore_defaults)
        reset_all_button = QPushButton("Reset total")
        reset_all_button.setProperty("danger", True)
        reset_all_button.clicked.connect(self._confirm_reset_all)
        save_button = QPushButton("Salvar configuracoes")
        save_button.clicked.connect(self._handle_save)
        actions.addWidget(reset_button)
        actions.addWidget(reset_all_button)
        actions.addWidget(save_button)
        layout.addLayout(actions)

    def _choose_db(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Selecionar banco", "", "SQLite (*.db)")
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
        QMessageBox.information(self, "Configuracoes", "Configuracoes salvas. Reinicie o app se trocar o banco.")

    def _restore_defaults(self) -> None:
        self.populate(DEFAULT_SETTINGS, self.inputs["db_path"].text())

    def _confirm_reset_all(self) -> None:
        answer = QMessageBox.warning(
            self,
            "Reset total",
            "Isso vai apagar todos os dados locais e fechar o app. Deseja continuar?",
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
            f"Soma dos pesos: {total}. Idealmente fique em 100 para manter o score intuitivo. "
            f"Faixas atuais: verde >= {good}, amarelo >= {mid}, vermelho abaixo disso."
        )

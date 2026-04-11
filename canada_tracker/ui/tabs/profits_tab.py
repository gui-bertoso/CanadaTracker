from __future__ import annotations

from datetime import date, timedelta

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QDateEdit,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from canada_tracker.ui.widgets.cards import MetricCard, SectionCard
from canada_tracker.ui.widgets.charts import multi_line_chart


class ProfitsTab(QWidget):
    def __init__(self, on_save, compact: bool = False) -> None:
        super().__init__()
        self.on_save = on_save
        self.compact = compact
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12 if compact else 16, 12 if compact else 16, 12 if compact else 16, 12 if compact else 16)
        layout.setSpacing(10 if compact else 16)

        title = QLabel("lucros" if compact else "Lucros")
        title.setProperty("section" if compact else "title", True)
        layout.addWidget(title)
        self.summary = QLabel()
        self.summary.setWordWrap(True)
        self.summary.setProperty("muted", True)
        layout.addWidget(self.summary)

        cards_row = QHBoxLayout()
        self.total_card = MetricCard("Total", "R$ 0")
        self.count_card = MetricCard("Entradas", "0")
        self.goal_card = MetricCard("Meta", "0%")
        self.average_card = MetricCard("Media", "R$ 0")
        cards_row.addWidget(self.total_card)
        cards_row.addWidget(self.count_card)
        cards_row.addWidget(self.goal_card)
        cards_row.addWidget(self.average_card)
        if compact:
            for card in (self.total_card, self.count_card, self.goal_card, self.average_card):
                card.setMinimumHeight(104)
                card.setMaximumHeight(104)
        layout.addLayout(cards_row)

        form_layout = QHBoxLayout()
        form_box = SectionCard("Nova Entrada", "Registre qualquer valor recebido e acompanhe a curva de crescimento.")
        form = QFormLayout()
        self.amount = QDoubleSpinBox()
        self.amount.setMaximum(1_000_000)
        self.amount.setPrefix("R$ ")
        self.amount.setDecimals(2)
        self.source = QLineEdit()
        self.entry_date = QDateEdit()
        self.entry_date.setCalendarPopup(True)
        self.entry_date.setDate(QDate.currentDate())
        self.note = QTextEdit()
        self.note.setFixedHeight(70)
        save_button = QPushButton("Salvar entrada")
        save_button.clicked.connect(self._handle_save)
        form.addRow("Valor", self.amount)
        form.addRow("Fonte", self.source)
        form.addRow("Data", self.entry_date)
        form.addRow("Observacao", self.note)
        form.addRow("", save_button)
        form_box.layout.addLayout(form)
        form_layout.addWidget(form_box, 1)
        self.chart_card = SectionCard("Evolucao dos Lucros")
        self.chart_container = QVBoxLayout()
        self.chart_card.layout.addLayout(self.chart_container)
        form_layout.addWidget(self.chart_card, 2)
        layout.addLayout(form_layout)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Data", "Fonte", "Valor", "Observacao"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setMaximumHeight(180 if compact else 260)
        layout.addWidget(self.table)

    def _handle_save(self) -> None:
        if not self.source.text().strip():
            QMessageBox.warning(self, "Validacao", "Informe a fonte da entrada.")
            return
        self.on_save(
            self.amount.value(),
            self.source.text(),
            self.entry_date.date().toString("yyyy-MM-dd"),
            self.note.toPlainText(),
        )
        self.amount.setValue(0.0)
        self.source.clear()
        self.note.clear()

    def refresh(self, entries: list[dict[str, object]], metrics: dict[str, object]) -> None:
        settings = metrics["settings"]
        average = metrics["profit_total"] / max(metrics["profit_entries"], 1)
        self.total_card.update_content("Total", f"R$ {metrics['profit_total']:.2f}", "Acumulado")
        self.count_card.update_content("Entradas", str(metrics["profit_entries"]), "Quantidade")
        self.goal_card.update_content("Meta", f"{metrics['financial_progress']:.1f}%", f"Meta R$ {float(settings['financial_goal']):.0f}")
        self.average_card.update_content("Media", f"R$ {average:.2f}", "Por entrada")
        self.summary.setText(
            f"Faltam R$ {max(float(settings['financial_goal']) - metrics['profit_total'], 0):.2f} para a meta principal. "
            f"O ritmo atual soma {metrics['profit_entries']} entradas registradas."
        )
        self.table.setRowCount(len(entries))
        for row_index, entry in enumerate(entries):
            self.table.setItem(row_index, 0, QTableWidgetItem(entry["entry_date"]))
            self.table.setItem(row_index, 1, QTableWidgetItem(entry["source"]))
            self.table.setItem(row_index, 2, QTableWidgetItem(f"R$ {float(entry['amount']):.2f}"))
            self.table.setItem(row_index, 3, QTableWidgetItem(entry["note"] or ""))
        while self.chart_container.count():
            item = self.chart_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.chart_container.addWidget(self._build_profit_chart(entries, float(settings["financial_goal"])))

    def _build_profit_chart(self, entries: list[dict[str, object]], goal: float):
        days = [date.today() - timedelta(days=offset) for offset in range(29, -1, -1)]
        labels = [day.isoformat() for day in days]
        daily_values = {label: 0.0 for label in labels}
        for entry in entries:
            if entry["entry_date"] in daily_values:
                daily_values[entry["entry_date"]] += float(entry["amount"])
        cumulative = 0.0
        real_points = []
        for label in labels:
            cumulative += daily_values[label]
            real_points.append((label, cumulative))
        target_points = []
        for index, label in enumerate(labels, start=1):
            target_points.append((label, (goal / len(labels)) * index if goal else 0.0))
        return multi_line_chart(
            [
                {"name": "lucro real", "color": "#63d1ff", "points": real_points},
                {"name": "meta ideal", "color": "#f0d020", "points": target_points, "style": "dashed"},
            ],
            "Evolucao dos Lucros",
            height=200 if self.compact else 260,
            y_max=max(goal, max((value for _, value in real_points), default=0.0), 10),
        )

from __future__ import annotations

from collections import Counter

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QProgressBar, QScrollArea, QVBoxLayout, QWidget

from canada_tracker.ui.widgets.cards import MetricCard, SectionCard


CATEGORY_STYLES = {
    "Lucros": ("LC", "#63d1ff", "#132638"),
    "Ingles": ("EN", "#88f0b3", "#153025"),
    "Consistencia": ("CS", "#ffd166", "#372b14"),
    "Habitos": ("HB", "#ff9f6e", "#352018"),
    "Disciplina": ("DS", "#d29cff", "#2d1938"),
    "Uso do App": ("AP", "#9fb5ff", "#1b2340"),
    "Metas": ("MT", "#ff86a8", "#371725"),
    "Marcos Gerais": ("MG", "#d8e2ee", "#202833"),
}


class AchievementBadge(QFrame):
    def __init__(self, achievement: dict[str, object]) -> None:
        super().__init__()
        self.achievement = achievement
        self.setProperty("achievementCard", True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        top = QHBoxLayout()
        top.setSpacing(12)
        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setFixedSize(58, 58)
        self.icon.setProperty("achievementIcon", True)
        top.addWidget(self.icon)

        title_col = QVBoxLayout()
        title_col.setSpacing(3)
        self.name = QLabel()
        self.name.setWordWrap(True)
        self.name.setProperty("achievementName", True)
        title_col.addWidget(self.name)
        self.category = QLabel()
        self.category.setProperty("muted", True)
        title_col.addWidget(self.category)
        top.addLayout(title_col, 1)
        layout.addLayout(top)

        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setProperty("muted", True)
        layout.addWidget(self.description)
        self.progress_text = QLabel()
        self.progress_text.setProperty("muted", True)
        layout.addWidget(self.progress_text)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(12)
        layout.addWidget(self.progress_bar)

        bottom = QHBoxLayout()
        self.status = QLabel()
        self.status.setProperty("achievementStatus", True)
        bottom.addWidget(self.status)
        bottom.addStretch(1)
        self.date = QLabel()
        self.date.setProperty("muted", True)
        bottom.addWidget(self.date)
        layout.addLayout(bottom)
        self.apply_data(achievement)

    def apply_data(self, achievement: dict[str, object]) -> None:
        self.achievement = achievement
        category = str(achievement["category"])
        code, color, bg = CATEGORY_STYLES.get(category, ("??", "#d8e2ee", "#202833"))
        unlocked = bool(achievement["unlocked"])
        self.icon.setText(code)
        self.icon.setStyleSheet(
            f"background: qradialgradient(cx:0.5, cy:0.5, radius:0.9, stop:0 {bg}, stop:1 #0b1118); color: {color}; border: 1px solid {color}; border-radius: 29px; font-weight: 800; font-size: 16px;"
        )
        self.name.setText(str(achievement["name"]))
        self.category.setText(category)
        self.description.setText(str(achievement["description"]))
        self.status.setText("desbloqueada" if unlocked else "em progresso")
        self.status.setStyleSheet(
            "background: #163624; color: #6de49a; border-radius: 8px; padding: 3px 8px; font-weight: 700;"
            if unlocked
            else "background: #202833; color: #d4b366; border-radius: 8px; padding: 3px 8px; font-weight: 700;"
        )
        self.date.setText(str(achievement["unlocked_at"][:10]) if achievement["unlocked_at"] else "sem data")
        if unlocked:
            self.progress_text.setText("trofeu garantido")
            self.progress_bar.setValue(100)
        else:
            current_value = achievement["current_value"]
            threshold = achievement["threshold"]
            self.progress_text.setText(f"falta pouco: {self._format_metric(current_value)}/{self._format_metric(threshold)}")
            self.progress_bar.setValue(int(achievement["progress_percent"]))
        self.setStyleSheet(
            "QFrame[achievementCard=\"true\"] {"
            + (
                "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #162635, stop:1 #10202d); border: 1px solid #3a6e95;"
                if unlocked
                else "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #121b26, stop:1 #0f151d); border: 1px solid #24364a;"
            )
            + " border-radius: 18px; }"
        )

    @staticmethod
    def _format_metric(value: object) -> str:
        numeric = float(value)
        return f"{numeric:.0f}" if numeric.is_integer() else f"{numeric:.1f}"


class AchievementsTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._all_achievements: list[dict[str, object]] = []
        self._cards: list[AchievementBadge] = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        title = QLabel("achievements")
        title.setProperty("title", True)
        layout.addWidget(title)

        cards_row = QHBoxLayout()
        self.total_card = MetricCard("Desbloqueadas", "0")
        self.locked_card = MetricCard("Bloqueadas", "0")
        self.progress_card = MetricCard("Progresso", "0%")
        cards_row.addWidget(self.total_card)
        cards_row.addWidget(self.locked_card)
        cards_row.addWidget(self.progress_card)
        layout.addLayout(cards_row)

        self.summary = QLabel()
        self.summary.setWordWrap(True)
        self.summary.setProperty("muted", True)
        layout.addWidget(self.summary)

        filters = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar achievement...")
        self.search.textChanged.connect(self._apply_filters)
        self.category_filter = QComboBox()
        self.category_filter.currentTextChanged.connect(self._apply_filters)
        self.status_filter = QComboBox()
        self.status_filter.addItems(["Todas", "Desbloqueadas", "Bloqueadas"])
        self.status_filter.currentTextChanged.connect(self._apply_filters)
        filters.addWidget(self.search, 2)
        filters.addWidget(self.category_filter, 1)
        filters.addWidget(self.status_filter, 1)
        layout.addLayout(filters)

        content = QHBoxLayout()
        content.setSpacing(12)

        left = QVBoxLayout()
        self.highlight_card = SectionCard("destaque")
        self.highlight_card.layout.setSpacing(10)
        self.highlight_title = QLabel("nenhuma conquista ainda")
        self.highlight_title.setProperty("section", True)
        self.highlight_desc = QLabel("continue registrando seus dados para desbloquear a primeira badge.")
        self.highlight_desc.setWordWrap(True)
        self.highlight_desc.setProperty("muted", True)
        self.highlight_card.layout.addWidget(self.highlight_title)
        self.highlight_card.layout.addWidget(self.highlight_desc)
        left.addWidget(self.highlight_card)

        self.next_card = SectionCard("proxima conquista")
        self.next_title = QLabel("sem alvo")
        self.next_title.setProperty("section", True)
        self.next_desc = QLabel("registre dados para surgir uma meta aqui.")
        self.next_desc.setWordWrap(True)
        self.next_desc.setProperty("muted", True)
        self.next_card.layout.addWidget(self.next_title)
        self.next_card.layout.addWidget(self.next_desc)
        self.next_progress = QProgressBar()
        self.next_progress.setRange(0, 100)
        self.next_progress.setTextVisible(False)
        self.next_card.layout.addWidget(self.next_progress)
        left.addWidget(self.next_card)
        left.addStretch(1)
        content.addLayout(left, 1)

        right = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.grid_host = QWidget()
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(12)
        scroll.setWidget(self.grid_host)
        right.addWidget(scroll)
        content.addLayout(right, 3)
        layout.addLayout(content, 1)

    def refresh(self, achievements: list[dict[str, object]]) -> None:
        self._all_achievements = achievements
        unlocked = [item for item in achievements if item["unlocked"]]
        counts = Counter(item["category"] for item in unlocked)
        parts = ", ".join(f"{category}: {total}" for category, total in sorted(counts.items())) or "Nenhuma ainda"
        self.summary.setText(f"{len(unlocked)} de {len(achievements)} achievements desbloqueadas. Categorias: {parts}.")
        self.total_card.update_content("Desbloqueadas", str(len(unlocked)))
        self.locked_card.update_content("Bloqueadas", str(len(achievements) - len(unlocked)))
        self.progress_card.update_content("Progresso", f"{(len(unlocked) / max(len(achievements), 1) * 100):.1f}%")
        categories = sorted({item["category"] for item in achievements})
        self.category_filter.blockSignals(True)
        self.category_filter.clear()
        self.category_filter.addItems(["Todas", *categories])
        self.category_filter.blockSignals(False)
        self._refresh_highlight(unlocked)
        self._refresh_next_target(achievements)
        self._apply_filters()

    def _apply_filters(self) -> None:
        status = self.status_filter.currentText()
        category = self.category_filter.currentText() if self.category_filter.count() else "Todas"
        term = self.search.text().strip().lower()
        filtered = []
        for item in self._all_achievements:
            if category != "Todas" and item["category"] != category:
                continue
            if status == "Desbloqueadas" and not item["unlocked"]:
                continue
            if status == "Bloqueadas" and item["unlocked"]:
                continue
            haystack = f"{item['name']} {item['description']} {item['category']}".lower()
            if term and term not in haystack:
                continue
            filtered.append(item)
        self._render_grid(filtered)

    def _render_grid(self, achievements: list[dict[str, object]]) -> None:
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self._cards.clear()
        for index, achievement in enumerate(achievements):
            card = AchievementBadge(achievement)
            card.setMinimumHeight(158)
            self._cards.append(card)
            self.grid.addWidget(card, index // 3, index % 3)
        self.grid.setRowStretch((len(achievements) + 2) // 3, 1)

    def _refresh_highlight(self, unlocked: list[dict[str, object]]) -> None:
        if not unlocked:
            self.highlight_title.setText("nenhuma conquista ainda")
            self.highlight_desc.setText("continue registrando seus dados para desbloquear a primeira badge.")
            return
        latest = sorted(unlocked, key=lambda item: item["unlocked_at"], reverse=True)[0]
        self.highlight_title.setText(str(latest["name"]))
        self.highlight_desc.setText(
            f"{latest['description']}\n\ncategoria: {latest['category']}\ndesbloqueada em: {latest['unlocked_at'][:10]}"
        )

    def _refresh_next_target(self, achievements: list[dict[str, object]]) -> None:
        locked = [item for item in achievements if not item["unlocked"]]
        if not locked:
            self.next_title.setText("tudo limpo")
            self.next_desc.setText("todas as conquistas atuais foram desbloqueadas.")
            self.next_progress.setValue(100)
            return
        target = max(locked, key=lambda item: (item["progress_percent"], -float(item["threshold"])))
        remaining = max(float(target["threshold"]) - float(target["current_value"]), 0.0)
        self.next_title.setText(str(target["name"]))
        self.next_desc.setText(
            f"{target['description']}\n\n{self._remaining_text(str(target['metric']), remaining)}"
        )
        self.next_progress.setValue(int(target["progress_percent"]))

    @staticmethod
    def _remaining_text(metric: str, remaining: float) -> str:
        labels = {
            "profit_total": "faltam R$ {value}",
            "profit_entries": "faltam {value} entradas",
            "english_minutes": "faltam {value} min",
            "english_days": "faltam {value} dias",
            "good_day_streak": "faltam {value} dias bons seguidos",
            "good_days": "faltam {value} dias verdes",
            "perfect_days": "faltam {value} dias perfeitos",
            "app_launches": "faltam {value} aberturas do app",
            "goal_progress": "faltam {value}% de progresso",
            "logs_count": "faltam {value} registros",
        }
        value = AchievementBadge._format_metric(remaining)
        template = labels.get(metric, "faltam {value}")
        return template.format(value=value)

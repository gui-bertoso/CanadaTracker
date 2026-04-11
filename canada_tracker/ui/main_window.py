from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QLabel, QMainWindow, QMessageBox, QPushButton, QProgressBar, QStatusBar, QTabWidget, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout

from canada_tracker.config import DEFAULT_RUNTIME_CONFIG, RUNTIME_CONFIG_PATH, save_runtime_config
from canada_tracker.services.app_service import AppService
from canada_tracker.ui.styles import build_stylesheet
from canada_tracker.ui.tabs.achievements_tab import AchievementsTab
from canada_tracker.ui.tabs.dashboard_tab import DashboardTab
from canada_tracker.ui.tabs.day_tab import DayTab
from canada_tracker.ui.tabs.settings_tab import SettingsTab
from canada_tracker.ui.widgets.cards import HeaderMetricCard


class MainWindow(QMainWindow):
    def __init__(self, service: AppService) -> None:
        super().__init__()
        self.service = service
        self.selected_log_date = __import__("datetime").date.today().isoformat()
        self.setWindowTitle("Canada Tracker")
        self.resize(1600, 980)
        self._build_ui()
        self.setStatusBar(QStatusBar())
        self.refresh_all()

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(8, 6, 8, 8)
        root_layout.setSpacing(8)
        self.setCentralWidget(root)
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setSpacing(8)
        self.app_title = QLabel("canada tracker")
        self.app_title.setProperty("section", True)
        self.app_title.setStyleSheet("font-size: 18px;")
        self.close_button = QPushButton("fechar")
        self.close_button.setProperty("secondary", True)
        self.close_button.clicked.connect(self.close)
        top_bar.addWidget(self.app_title)
        top_bar.addStretch(1)
        top_bar.addWidget(self.close_button)
        root_layout.addLayout(top_bar)
        header_grid = QGridLayout()
        header_grid.setSpacing(8)
        self.header_cards = [
            HeaderMetricCard("meta usd", "$0"),
            HeaderMetricCard("feito", "$0"),
            HeaderMetricCard("falta", "$0"),
            HeaderMetricCard("meta dia", "$0"),
            HeaderMetricCard("meta semana", "$0"),
            HeaderMetricCard("ingles", "0/0"),
            HeaderMetricCard("badges", "0/0"),
            HeaderMetricCard("previsao", "sem ritmo"),
        ]
        for index, card in enumerate(self.header_cards):
            header_grid.addWidget(card, 0, index)
        root_layout.addLayout(header_grid)
        self.global_progress = QProgressBar()
        self.global_progress.setRange(0, 100)
        self.global_progress.setFormat("%.1f%%")
        root_layout.addWidget(self.global_progress)
        tabs = QTabWidget()
        self.tabs = tabs
        self.dashboard_tab = DashboardTab()
        self.day_tab = DayTab(self._save_profit, self._save_english, self._save_habits, self._load_log_by_date)
        self.profits_tab = self.day_tab.profits_tab
        self.english_tab = self.day_tab.english_tab
        self.habits_tab = self.day_tab.habits_tab
        self.achievements_tab = AchievementsTab()
        self.settings_tab = SettingsTab(self._save_settings, self._reset_all_data)

        tabs.addTab(self.dashboard_tab, "dashboard")
        tabs.addTab(self.day_tab, "dia")
        tabs.addTab(self.achievements_tab, "achievements")
        tabs.addTab(self.settings_tab, "config")
        root_layout.addWidget(tabs)

    def refresh_all(self) -> None:
        metrics = self.service.metrics()
        entries = self.service.list_profit_entries()
        sessions = self.service.list_english_sessions()
        calendar_scores = self.service.calendar_scores()
        selected_log = self.service.get_enriched_log(self.selected_log_date)
        achievements = self.service.achievement_status()

        self.setStyleSheet(build_stylesheet(str(metrics["settings"]["accent_color"])))
        self.dashboard_tab.refresh(metrics, achievements)
        self.profits_tab.refresh(entries, metrics)
        self.english_tab.refresh(sessions, metrics)
        self.habits_tab.refresh(metrics, calendar_scores, selected_log)
        self.achievements_tab.refresh(achievements)
        self.settings_tab.populate(self.service.get_settings(), str(self.service.database.db_path))
        self._refresh_header(metrics, achievements)
        self.statusBar().showMessage(
            f"Banco: {self.service.database.db_path} | Lucros: R$ {metrics['profit_total']:.2f} | Ingles: {metrics['english_hours']:.1f}h | Conquistas: {metrics['unlocked_achievements']}",
            8000,
        )

    def _save_profit(self, amount: float, source: str, entry_date: str, note: str) -> None:
        try:
            unlocked = self.service.add_profit_entry(amount, source, entry_date, note)
            self.refresh_all()
            self._notify_unlocks(unlocked)
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Nao foi possivel salvar a entrada.\n{exc}")

    def _save_english(self, minutes: int, study_type: str, session_date: str, note: str) -> None:
        try:
            unlocked = self.service.add_english_session(minutes, study_type, session_date, note)
            self.refresh_all()
            self._notify_unlocks(unlocked)
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Nao foi possivel salvar a sessao.\n{exc}")

    def _save_habits(self, payload: dict[str, object]) -> None:
        try:
            unlocked = self.service.save_daily_log(payload)
            self.selected_log_date = str(payload["log_date"])
            self.refresh_all()
            self._notify_unlocks(unlocked)
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Nao foi possivel salvar o registro.\n{exc}")

    def _load_log_by_date(self, iso_date: str) -> None:
        self.selected_log_date = iso_date
        self.habits_tab.load_log(self.service.get_enriched_log(iso_date))

    def _save_settings(self, payload: dict[str, object]) -> None:
        try:
            db_changed = self.service.save_settings(payload)
            self.refresh_all()
            if db_changed:
                self.statusBar().showMessage("Caminho do banco atualizado. Reinicie o app para usar o novo arquivo.", 10000)
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Nao foi possivel salvar as configuracoes.\n{exc}")

    def _notify_unlocks(self, unlocked_ids: list[str]) -> None:
        if not unlocked_ids:
            return
        self.statusBar().showMessage(f"{len(unlocked_ids)} nova(s) conquista(s) desbloqueada(s).", 10000)

    def _reset_all_data(self) -> None:
        db_path = Path(str(self.service.database.db_path))
        try:
            if db_path.exists():
                db_path.unlink()
            if RUNTIME_CONFIG_PATH.exists():
                RUNTIME_CONFIG_PATH.unlink()
            save_runtime_config(DEFAULT_RUNTIME_CONFIG)
            QMessageBox.information(
                self,
                "Reset concluido",
                "Todos os dados locais foram apagados. O app sera fechado agora.",
            )
            self.close()
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Nao foi possivel resetar os dados.\n{exc}")

    def _refresh_header(self, metrics: dict[str, object], achievements: list[dict[str, object]]) -> None:
        settings = metrics["settings"]
        goal = float(settings["financial_goal"])
        done = float(metrics["profit_total"])
        remaining = max(goal - done, 0.0)
        day_goal = round(goal / 150, 2) if goal else 0.0
        week_goal = round(day_goal * 7, 2)
        unlocked = sum(1 for item in achievements if item["unlocked"])
        total_achievements = len(achievements)
        english_now = round(metrics["english_hours"], 1)
        english_goal = round(int(settings["english_goal_minutes"]) / 60, 1)
        weekly_profit = 0.0
        for item in metrics["recent_profits"]:
            if item["entry_date"] >= (__import__("datetime").date.today() - __import__("datetime").timedelta(days=6)).isoformat():
                weekly_profit += float(item["amount"])
        forecast = "sem ritmo"
        if weekly_profit > 0:
            weeks_needed = remaining / weekly_profit
            forecast = f"{weeks_needed:.1f} sem"
        self.header_cards[0].update_content("meta usd", f"${goal:,.0f}")
        self.header_cards[1].update_content("feito", f"${done:,.0f}")
        self.header_cards[2].update_content("falta", f"${remaining:,.0f}")
        self.header_cards[3].update_content("meta dia", f"${day_goal:,.0f}")
        self.header_cards[4].update_content("meta semana", f"${week_goal:,.0f}")
        self.header_cards[5].update_content("ingles", f"{english_now}/{english_goal}")
        self.header_cards[6].update_content("badges", f"{unlocked}/{total_achievements}")
        self.header_cards[7].update_content("previsao", forecast)
        self.global_progress.setValue(min(100, int(metrics["goal_progress"])))
        self.global_progress.setFormat(f"{metrics['goal_progress']:.1f}%")

from __future__ import annotations


def build_stylesheet(accent_color: str) -> str:
    return f"""
    QWidget {{
        color: #e7edf5;
        background: transparent;
        font-family: "Noto Sans", "DejaVu Sans";
        font-size: 13px;
    }}
    QMainWindow {{
        background: #0b1016;
    }}
    QScrollArea, QTabWidget::pane {{
        background: #0f141b;
        border: none;
    }}
    QLabel {{
        background: transparent;
    }}
    QTableWidget, QListWidget, QTreeWidget, QTextEdit,
    QPlainTextEdit, QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox,
    QCalendarWidget QAbstractItemView {{
        background: #121922;
        color: #e7edf5;
        border: 1px solid #232d38;
        border-radius: 10px;
    }}
    QAbstractSpinBox {{
        padding: 2px 6px;
    }}
    QTabBar::tab {{
        background: #0f1620;
        border: 1px solid #24303d;
        padding: 9px 16px;
        margin-right: 6px;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        color: #8fa0b1;
        font-weight: 600;
    }}
    QTabBar::tab:selected {{
        background: #142132;
        color: #ffffff;
        border-color: {accent_color};
    }}
    QTabBar::tab:hover {{
        color: #dce7f1;
        border-color: #324455;
    }}
    QTabWidget::pane {{
        margin-top: 8px;
        padding: 8px;
    }}
    QPushButton {{
        background: {accent_color};
        color: #08111b;
        border: none;
        border-radius: 10px;
        padding: 10px 14px;
        font-weight: 700;
    }}
    QPushButton:hover {{
        background: #9fd7ff;
    }}
    QPushButton[secondary="true"] {{
        background: #161f29;
        color: #d8e2ee;
        border: 1px solid #2d3947;
    }}
    QPushButton[secondary="true"]:hover {{
        background: #1d2833;
    }}
    QPushButton[danger="true"] {{
        background: #8f2535;
        color: #fff4f6;
        border: 1px solid #b94459;
    }}
    QPushButton[danger="true"]:hover {{
        background: #a93144;
    }}
    QLabel[title="true"] {{
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
    }}
    QLabel[section="true"] {{
        font-size: 16px;
        font-weight: 700;
        color: #ffffff;
    }}
    QFrame[card="true"] {{
        background: #121922;
        border: 1px solid #232d38;
        border-radius: 16px;
    }}
    QFrame[achievementCard="true"] {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #121b26, stop:1 #0f151d);
        border: 1px solid #24364a;
        border-radius: 18px;
    }}
    QFrame[headerCard="true"] {{
        background: #101725;
        border: 1px solid #213450;
        border-radius: 14px;
    }}
    QFrame[hero="true"] {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #132232, stop:1 #101821);
        border: 1px solid #284054;
        border-radius: 20px;
    }}
    QLabel[headerLabel="true"] {{
        color: #70caff;
        font-size: 12px;
        font-weight: 700;
    }}
    QLabel[headerValue="true"] {{
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
    }}
    QLabel[muted="true"] {{
        color: #8ea0b2;
    }}
    QLabel[achievementName="true"] {{
        font-size: 16px;
        font-weight: 700;
        color: #f4f8fd;
    }}
    QLabel[pill="good"] {{
        background: #163624;
        color: #6de49a;
        border-radius: 9px;
        padding: 4px 8px;
        font-weight: 700;
    }}
    QLabel[pill="mid"] {{
        background: #3f3815;
        color: #f1cb57;
        border-radius: 9px;
        padding: 4px 8px;
        font-weight: 700;
    }}
    QLabel[pill="low"] {{
        background: #38181d;
        color: #f28a8a;
        border-radius: 9px;
        padding: 4px 8px;
        font-weight: 700;
    }}
    QHeaderView::section {{
        background: #0f151d;
        color: #97a5b3;
        border: none;
        padding: 8px;
    }}
    QTableWidget {{
        gridline-color: #232d38;
        selection-background-color: #213245;
        selection-color: #ffffff;
        alternate-background-color: #10161d;
    }}
    QProgressBar {{
        background: rgba(8, 14, 20, 0.55);
        border: 1px solid #232d38;
        border-radius: 10px;
        text-align: center;
        min-height: 20px;
        font-weight: 700;
    }}
    QProgressBar::chunk {{
        background: {accent_color};
        border-radius: 9px;
    }}
    QStatusBar {{
        background: #10161d;
        color: #92a5b7;
    }}
    QScrollBar:vertical {{
        background: #10161d;
        width: 12px;
        margin: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: #2b3948;
        min-height: 24px;
        border-radius: 6px;
    }}
    QCalendarWidget QWidget {{
        alternate-background-color: #0f141b;
    }}
    QToolTip {{
        background: #111820;
        color: #ffffff;
        border: 1px solid #2a3946;
    }}
    """

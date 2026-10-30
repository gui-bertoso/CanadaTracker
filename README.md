# Canada Tracker

A personal Python/PySide6 desktop app for tracking earnings, English practice,
habits, overall progress and achievements for your Canada Project.

## Stack

Python 3.11+, PySide6 and SQLite.

## Structure

- `main.py`: application entry point.
- `canada_tracker/config.py`: defaults and paths.
- `canada_tracker/database.py`: SQLite initialization.
- `canada_tracker/services/`: business rules, daily scores and achievements.
- `canada_tracker/ui/`: main window, tabs, widgets and dark theme.
- `scripts/run_canada_tracker.sh`: launcher with an absolute path.
- `scripts/install_autostart.sh`: Linux autostart installer.
- `scripts/canada-tracker.desktop`: desktop entry.

## Run

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python main.py
```

## Autostart

Install:

```bash
sh scripts/install_autostart.sh
```

Disable:

```bash
rm -f ~/.config/autostart/canada-tracker.desktop
```

## License

The author's code uses the [MIT License](LICENSE). Third-party materials retain their original licenses.

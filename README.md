# Canada Tracker

App desktop pessoal em Python/PySide6 para acompanhar lucros, ingles, habitos, progresso geral e conquistas do seu Canada Project.

## Stack

- Python 3.11+
- PySide6
- SQLite

## Estrutura

- `main.py`: entrada do app
- `canada_tracker/config.py`: defaults e caminhos
- `canada_tracker/database.py`: inicializacao do SQLite
- `canada_tracker/services/`: regras de negocio, score diario e conquistas
- `canada_tracker/ui/`: janela principal, abas, widgets, estilo dark
- `scripts/run_canada_tracker.sh`: launcher com caminho absoluto
- `scripts/install_autostart.sh`: instala o autostart padrao do Linux
- `scripts/canada-tracker.desktop`: arquivo `.desktop`

## Como rodar

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python main.py
```

## Autostart

Instalar:

```bash
sh scripts/install_autostart.sh
```

Desativar:

```bash
rm -f ~/.config/autostart/canada-tracker.desktop
```

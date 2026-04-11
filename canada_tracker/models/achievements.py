from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Achievement:
    achievement_id: str
    name: str
    description: str
    category: str
    metric: str
    threshold: int | float


def build_achievement_definitions() -> list[Achievement]:
    definitions: list[Achievement] = []
    categories = {
        "profits_total": (
            "Lucros",
            "profit_total",
            [
                (50, "Primeiros R$ 50", "Acumule R$ 50 em lucros."),
                (100, "Drop de Bronze", "Acumule R$ 100 em lucros."),
                (250, "Loot Inicial", "Acumule R$ 250 em lucros."),
                (500, "Bolso de Ferro", "Acumule R$ 500 em lucros."),
                (1000, "Tesouro de Quatro Digitos", "Acumule R$ 1.000 em lucros."),
                (1500, "Modo Farm", "Acumule R$ 1.500 em lucros."),
                (2000, "Cofre Destravado", "Acumule R$ 2.000 em lucros."),
                (3000, "Boss do Caixa", "Acumule R$ 3.000 em lucros."),
                (5000, "Primeira Grande Raid", "Acumule R$ 5.000 em lucros."),
                (10000, "Lenda dos Cinco Digitos", "Acumule R$ 10.000 em lucros."),
                (15000, "Elite do Farm", "Acumule R$ 15.000 em lucros."),
                (20000, "Funding Supremo", "Acumule R$ 20.000 em lucros."),
            ],
        ),
        "profits_entries": (
            "Lucros",
            "profit_entries",
            [
                (1, "Primeiro Loot", "Registre a primeira entrada."),
                (3, "Combo de Caixa", "Registre 3 entradas."),
                (5, "Drop em Serie", "Registre 5 entradas."),
                (10, "Ritmo de Grinder", "Registre 10 entradas."),
                (15, "Contador de Recompensas", "Registre 15 entradas."),
                (20, "Farm de Lucro", "Registre 20 entradas."),
                (30, "Stack Dourado", "Registre 30 entradas."),
                (40, "Mochila Cheia", "Registre 40 entradas."),
                (50, "Arquivo do Mercador", "Registre 50 entradas."),
                (75, "Run Sem Fim", "Registre 75 entradas."),
                (100, "Cronica do Farm", "Registre 100 entradas."),
                (150, "Lorde do Fluxo", "Registre 150 entradas."),
            ],
        ),
        "english_minutes": (
            "Ingles",
            "english_minutes",
            [
                (30, "Warmup do Heroi", "Estude 30 minutos."),
                (60, "Buff de 1 Hora", "Estude 60 minutos."),
                (120, "Classe Desbloqueada", "Estude 2 horas."),
                (300, "Magia de 5 Horas", "Estude 5 horas."),
                (600, "Build de 10 Horas", "Estude 10 horas."),
                (900, "Combo de 15 Horas", "Estude 15 horas."),
                (1200, "Tier de 20 Horas", "Estude 20 horas."),
                (1800, "Guilda de 30 Horas", "Estude 30 horas."),
                (2400, "Rank de 40 Horas", "Estude 40 horas."),
                (3600, "Mestre de 60 Horas", "Estude 60 horas."),
                (4800, "Arcano de 80 Horas", "Estude 80 horas."),
                (6000, "Fluencia Lendaria", "Estude 100 horas."),
            ],
        ),
        "english_days": (
            "Ingles",
            "english_days",
            [
                (1, "Spawn no Ingles", "Estude em 1 dia."),
                (3, "Streak de Arranque", "Estude em 3 dias."),
                (5, "Mini Season", "Estude em 5 dias."),
                (7, "Semana Fechada", "Estude em 7 dias."),
                (10, "Checkpoint 10", "Estude em 10 dias."),
                (14, "Ciclo da Quinzena", "Estude em 14 dias."),
                (21, "Habito em Combo", "Estude em 21 dias."),
                (30, "Mes de XP Linguistico", "Estude em 30 dias."),
                (45, "Cadencia de Elite", "Estude em 45 dias."),
                (60, "Temporada Dupla", "Estude em 60 dias."),
                (90, "Trimestre em Ingles", "Estude em 90 dias."),
                (120, "Rotina Mitica", "Estude em 120 dias."),
            ],
        ),
        "good_day_streak": (
            "Consistencia",
            "good_day_streak",
            [
                (2, "Combo x2", "Tenha 2 dias bons seguidos."),
                (3, "Combo x3", "Tenha 3 dias bons seguidos."),
                (5, "Mao Quente", "Tenha 5 dias bons seguidos."),
                (7, "Semana sem Miss", "Tenha 7 dias bons seguidos."),
                (10, "Sequencia de Ferro", "Tenha 10 dias bons seguidos."),
                (14, "Quinzena Blindada", "Tenha 14 dias bons seguidos."),
                (21, "Streak Monstro", "Tenha 21 dias bons seguidos."),
                (30, "Mes sem Quebra", "Tenha 30 dias bons seguidos."),
                (45, "Lenda da Consistencia", "Tenha 45 dias bons seguidos."),
                (60, "Titã da Rotina", "Tenha 60 dias bons seguidos."),
                (90, "Trimestre Implacavel", "Tenha 90 dias bons seguidos."),
                (120, "Disciplina Mitica", "Tenha 120 dias bons seguidos."),
            ],
        ),
        "good_days": (
            "Habitos",
            "good_days",
            [
                (1, "Primeiro Dia Verde", "Feche 1 dia verde."),
                (3, "Broto de Disciplina", "Feche 3 dias verdes."),
                (7, "Pacote Semanal", "Feche 7 dias verdes."),
                (10, "Rank Verde", "Feche 10 dias verdes."),
                (15, "Forca de Rotina", "Feche 15 dias verdes."),
                (20, "Habito Consolidado", "Feche 20 dias verdes."),
                (30, "Mes Dourado", "Feche 30 dias verdes."),
                (45, "Aura Verde", "Feche 45 dias verdes."),
                (60, "Trilha Perfeita", "Feche 60 dias verdes."),
                (90, "Temporada Verde", "Feche 90 dias verdes."),
                (120, "Selo de Constancia", "Feche 120 dias verdes."),
                (180, "Semi-Deus da Rotina", "Feche 180 dias verdes."),
            ],
        ),
        "perfect_days": (
            "Disciplina",
            "perfect_days",
            [
                (1, "Selo 100%", "Tenha 1 dia com score 100."),
                (2, "Dupla Perfeita", "Tenha 2 dias com score 100."),
                (3, "Trindade do Foco", "Tenha 3 dias com score 100."),
                (5, "Mao de Diamante", "Tenha 5 dias com score 100."),
                (7, "Semana Impecavel", "Tenha 7 dias com score 100."),
                (10, "Deca de Ouro", "Tenha 10 dias com score 100."),
                (15, "Armadura Perfeita", "Tenha 15 dias com score 100."),
                (20, "Sem Falhas", "Tenha 20 dias com score 100."),
                (30, "Mes Perfeito", "Tenha 30 dias com score 100."),
                (40, "Dominio da Rotina", "Tenha 40 dias com score 100."),
                (50, "Lorde da Disciplina", "Tenha 50 dias com score 100."),
                (75, "Reliquia Suprema", "Tenha 75 dias com score 100."),
            ],
        ),
        "app_launches": (
            "Uso do App",
            "app_launches",
            [
                (1, "Primeiro Login", "Abra o app pela primeira vez."),
                (3, "Retorno ao Hub", "Abra o app 3 vezes."),
                (5, "Player Frequente", "Abra o app 5 vezes."),
                (7, "Check-in Semanal", "Abra o app 7 vezes."),
                (10, "Portal Ativo", "Abra o app 10 vezes."),
                (15, "Ritual Digital", "Abra o app 15 vezes."),
                (20, "Olho no Painel", "Abra o app 20 vezes."),
                (30, "Hub Principal", "Abra o app 30 vezes."),
                (45, "Veterano do Tracker", "Abra o app 45 vezes."),
                (60, "Guardiao do Projeto", "Abra o app 60 vezes."),
                (90, "Mestre do Check-in", "Abra o app 90 vezes."),
                (120, "Nucleo de Comando", "Abra o app 120 vezes."),
            ],
        ),
        "goal_progress": (
            "Metas",
            "goal_progress",
            [
                (10, "Primeiro Marco", "Alcance 10% das metas principais."),
                (20, "Segundo Gate", "Alcance 20% das metas principais."),
                (30, "Subida de Tier", "Alcance 30% das metas principais."),
                (40, "Mapa Aberto", "Alcance 40% das metas principais."),
                (50, "Metade da Jornada", "Alcance 50% das metas principais."),
                (60, "Pressao de Endgame", "Alcance 60% das metas principais."),
                (70, "Reta Final", "Alcance 70% das metas principais."),
                (80, "Modo Boss", "Alcance 80% das metas principais."),
                (90, "Quase Lenda", "Alcance 90% das metas principais."),
                (100, "Quest Principal Completa", "Alcance 100% das metas principais."),
                (120, "Overcap", "Passe de 120% em metas principais."),
                (150, "Alem do Endgame", "Passe de 150% em metas principais."),
            ],
        ),
        "logs_count": (
            "Marcos Gerais",
            "logs_count",
            [
                (1, "Dia Um", "Registre o primeiro dia."),
                (3, "Trilha Inicial", "Registre 3 dias."),
                (5, "Cinco Passos", "Registre 5 dias."),
                (7, "Semana Gravada", "Registre 7 dias."),
                (10, "Arquivo Vivo", "Registre 10 dias."),
                (15, "Marca da Quinzena", "Registre 15 dias."),
                (20, "Rastro de 20", "Registre 20 dias."),
                (30, "Mes Registrado", "Registre 30 dias."),
                (45, "Campanha Longa", "Registre 45 dias."),
                (60, "Arquivo de Ferro", "Registre 60 dias."),
                (90, "Cronica de 90", "Registre 90 dias."),
                (120, "Livro do Projeto", "Registre 120 dias."),
            ],
        ),
    }
    for key, (category, metric, items) in categories.items():
        for index, (threshold, name, description) in enumerate(items, start=1):
            definitions.append(
                Achievement(
                    achievement_id=f"{key}_{index:02d}",
                    name=name,
                    description=description,
                    category=category,
                    metric=metric,
                    threshold=threshold,
                )
            )
    return definitions


ACHIEVEMENTS = build_achievement_definitions()

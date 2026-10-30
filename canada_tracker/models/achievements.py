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
            'Earnings',
            "profit_total",
            [
                (50, 'First R$ 50', 'Accumulate R$ 50 in earnings.'),
                (100, 'Bronze Drop', 'Accumulate R$ 100 in earnings.'),
                (250, 'Starting Loot', 'Accumulate R$ 250 in earnings.'),
                (500, 'Iron Pocket', 'Accumulate R$ 500 in earnings.'),
                (1000, 'Four-Digit Treasure', 'Accumulate R$ 1.000 in earnings.'),
                (1500, 'Farming Mode', 'Accumulate R$ 1.500 in earnings.'),
                (2000, 'Vault Unlocked', 'Accumulate R$ 2.000 in earnings.'),
                (3000, 'Cash Boss', 'Accumulate R$ 3.000 in earnings.'),
                (5000, 'First Big Raid', 'Accumulate R$ 5.000 in earnings.'),
                (10000, 'Five-Digit Legend', 'Accumulate R$ 10.000 in earnings.'),
                (15000, 'Farming Elite', 'Accumulate R$ 15.000 in earnings.'),
                (20000, 'Supreme Funding', 'Accumulate R$ 20.000 in earnings.'),
            ],
        ),
        "profits_entries": (
            'Earnings',
            "profit_entries",
            [
                (1, 'First Loot', 'Record the first entry.'),
                (3, 'Cash Combo', 'Record 3 entries.'),
                (5, 'Drop Streak', 'Record 5 entries.'),
                (10, 'Grinding Pace', 'Record 10 entries.'),
                (15, 'Reward Counter', 'Record 15 entries.'),
                (20, 'Profit Farm', 'Record 20 entries.'),
                (30, 'Golden Stack', 'Record 30 entries.'),
                (40, 'Full Backpack', 'Record 40 entries.'),
                (50, 'Merchant Archive', 'Record 50 entries.'),
                (75, 'Endless Run', 'Record 75 entries.'),
                (100, 'Farming Chronicle', 'Record 100 entries.'),
                (150, 'Lord of Flow', 'Record 150 entries.'),
            ],
        ),
        "english_minutes": (
            'English',
            "english_minutes",
            [
                (30, 'Hero Warmup', 'Study for 30 minutes.'),
                (60, '1-Hour Buff', 'Study for 60 minutes.'),
                (120, 'Class Unlocked', 'Study for 2 hours.'),
                (300, '5-Hour Magic', 'Study for 5 hours.'),
                (600, '10-Hour Build', 'Study for 10 hours.'),
                (900, '15-Hour Combo', 'Study for 15 hours.'),
                (1200, '20-Hour Tier', 'Study for 20 hours.'),
                (1800, '30-Hour Guild', 'Study for 30 hours.'),
                (2400, '40-Hour Rank', 'Study for 40 hours.'),
                (3600, '60-Hour Master', 'Study for 60 hours.'),
                (4800, '80-Hour Arcanist', 'Study for 80 hours.'),
                (6000, 'Legendary Fluency', 'Study for 100 hours.'),
            ],
        ),
        "english_days": (
            'English',
            "english_days",
            [
                (1, 'English Spawn', 'Study on 1 day(s).'),
                (3, 'Starting Streak', 'Study on 3 day(s).'),
                (5, "Mini Season", 'Study on 5 day(s).'),
                (7, 'Week Complete', 'Study on 7 day(s).'),
                (10, "Checkpoint 10", 'Study on 10 day(s).'),
                (14, 'Two-Week Cycle', 'Study on 14 day(s).'),
                (21, 'Habit Combo', 'Study on 21 day(s).'),
                (30, 'Month of Language XP', 'Study on 30 day(s).'),
                (45, 'Elite Pace', 'Study on 45 day(s).'),
                (60, 'Double Season', 'Study on 60 day(s).'),
                (90, 'English Quarter', 'Study on 90 day(s).'),
                (120, 'Mythic Routine', 'Study on 120 day(s).'),
            ],
        ),
        "good_day_streak": (
            'Consistency',
            "good_day_streak",
            [
                (2, "Combo x2", 'Complete 2 consecutive good days.'),
                (3, "Combo x3", 'Complete 3 consecutive good days.'),
                (5, 'Hot Hand', 'Complete 5 consecutive good days.'),
                (7, 'No-Miss Week', 'Complete 7 consecutive good days.'),
                (10, 'Iron Streak', 'Complete 10 consecutive good days.'),
                (14, "Quinzena Blindada", 'Complete 14 consecutive good days.'),
                (21, 'Monster Streak', 'Complete 21 consecutive good days.'),
                (30, 'Unbroken Month', 'Complete 30 consecutive good days.'),
                (45, 'Legend of Consistency', 'Complete 45 consecutive good days.'),
                (60, 'Routine Titan', 'Complete 60 consecutive good days.'),
                (90, 'Relentless Quarter', 'Complete 90 consecutive good days.'),
                (120, 'Mythic Discipline', 'Complete 120 consecutive good days.'),
            ],
        ),
        "good_days": (
            'Habits',
            "good_days",
            [
                (1, 'First Green Day', 'Complete 1 green day(s).'),
                (3, 'Discipline Sprout', 'Complete 3 green day(s).'),
                (7, 'Weekly Pack', 'Complete 7 green day(s).'),
                (10, 'Green Rank', 'Complete 10 green day(s).'),
                (15, 'Routine Strength', 'Complete 15 green day(s).'),
                (20, 'Habit Established', 'Complete 20 green day(s).'),
                (30, 'Golden Month', 'Complete 30 green day(s).'),
                (45, 'Green Aura', 'Complete 45 green day(s).'),
                (60, 'Perfect Trail', 'Complete 60 green day(s).'),
                (90, 'Green Season', 'Complete 90 green day(s).'),
                (120, 'Consistency Seal', 'Complete 120 green day(s).'),
                (180, 'Routine Demigod', 'Complete 180 green day(s).'),
            ],
        ),
        "perfect_days": (
            'Discipline',
            "perfect_days",
            [
                (1, '100% Seal', 'Complete 1 day(s) with a score of 100.'),
                (2, 'Perfect Pair', 'Complete 2 day(s) with a score of 100.'),
                (3, 'Focus Trinity', 'Complete 3 day(s) with a score of 100.'),
                (5, 'Diamond Hand', 'Complete 5 day(s) with a score of 100.'),
                (7, 'Flawless Week', 'Complete 7 day(s) with a score of 100.'),
                (10, 'Golden Ten', 'Complete 10 day(s) with a score of 100.'),
                (15, 'Perfect Armor', 'Complete 15 day(s) with a score of 100.'),
                (20, 'No Failures', 'Complete 20 day(s) with a score of 100.'),
                (30, 'Perfect Month', 'Complete 30 day(s) with a score of 100.'),
                (40, 'Routine Mastery', 'Complete 40 day(s) with a score of 100.'),
                (50, 'Lord of Discipline', 'Complete 50 day(s) with a score of 100.'),
                (75, 'Supreme Relic', 'Complete 75 day(s) with a score of 100.'),
            ],
        ),
        "app_launches": (
            'App Usage',
            "app_launches",
            [
                (1, 'First Login', 'Open the app for the first time.'),
                (3, 'Return to the Hub', 'Open the app 3 times.'),
                (5, 'Frequent Player', 'Open the app 5 times.'),
                (7, 'Weekly Check-in', 'Open the app 7 times.'),
                (10, 'Active Portal', 'Open the app 10 times.'),
                (15, 'Digital Ritual', 'Open the app 15 times.'),
                (20, 'Eyes on the Dashboard', 'Open the app 20 times.'),
                (30, 'Main Hub', 'Open the app 30 times.'),
                (45, 'Tracker Veteran', 'Open the app 45 times.'),
                (60, 'Project Guardian', 'Open the app 60 times.'),
                (90, 'Check-in Master', 'Open the app 90 times.'),
                (120, 'Command Core', 'Open the app 120 times.'),
            ],
        ),
        "goal_progress": (
            'Goals',
            "goal_progress",
            [
                (10, 'First Milestone', 'Reach 10% of the main goals.'),
                (20, 'Second Gate', 'Reach 20% of the main goals.'),
                (30, 'Tier Increase', 'Reach 30% of the main goals.'),
                (40, 'Open Map', 'Reach 40% of the main goals.'),
                (50, 'Halfway Through', 'Reach 50% of the main goals.'),
                (60, 'Endgame Pressure', 'Reach 60% of the main goals.'),
                (70, 'Final Stretch', 'Reach 70% of the main goals.'),
                (80, 'Boss Mode', 'Reach 80% of the main goals.'),
                (90, "Quase Lenda", 'Reach 90% of the main goals.'),
                (100, "Quest Principal Completa", 'Reach 100% of the main goals.'),
                (120, "Overcap", 'Exceed 120% of the main goals.'),
                (150, 'Beyond Endgame', 'Exceed 150% of the main goals.'),
            ],
        ),
        "logs_count": (
            'General Milestones',
            "logs_count",
            [
                (1, 'Day One', 'Record the first day.'),
                (3, 'Starting Trail', 'Record 3 day(s).'),
                (5, 'Five Steps', 'Record 5 day(s).'),
                (7, 'Week Recorded', 'Record 7 day(s).'),
                (10, 'Living Archive', 'Record 10 day(s).'),
                (15, 'Two-Week Mark', 'Record 15 day(s).'),
                (20, 'Trail of 20', 'Record 20 day(s).'),
                (30, 'Month Recorded', 'Record 30 day(s).'),
                (45, 'Long Campaign', 'Record 45 day(s).'),
                (60, 'Iron Archive', 'Record 60 day(s).'),
                (90, 'Chronicle of 90', 'Record 90 day(s).'),
                (120, 'Project Book', 'Record 120 day(s).'),
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

from data_loader import DataLoader
import pandas as pd

"""
Датасет: Результаты футбольных матчей сезона 2023-2024.
Источник: https://www.football-data.org/
Колонки:
- Date: Дата матча
- HomeTeam: Домашняя команда
- AwayTeam: Гостевая команда
- FTHG: Голы домашней команды
- FTAG: Голы гостевой команды
- FTR: Результат матча (H - победа дома, A - победа гостей, D - ничья)
- Referee: Судья
- HR: Пенальти домашней команды
- AR: Пенальти гостевой команды
"""

# Создание объекта и загрузка данных
loader = DataLoader()
loader.load_from_csv("season-2324.csv")

if loader.data is not None:
    df = loader.data

    # Проверка перед созданием TotalGoals
    if "FTHG" in df.columns and "FTAG" in df.columns:
        df["TotalGoals"] = df["FTHG"] + df["FTAG"]
    else:
        print("Ошибка: Колонки FTHG/FTAG отсутствуют.")


    # 1. Общее количество матчей
    print("\n=== 1. Общее количество матчей ===")
    print(f"Всего матчей: {df.shape[0]}")

    # 2. Топ-5 домашних команд по победам
    print("\n=== 2. Топ-5 домашних команд по победам ===")
    if "FTR" in df.columns and "HomeTeam" in df.columns:
        home_wins = df[df["FTR"] == "H"]["HomeTeam"].value_counts().head(5)
        print(home_wins.to_string())
    else:
        print("Ошибка: Колонки FTR или HomeTeam отсутствуют.")

    # 3. Самый результативный матч
    print("\n=== 3. Самый результативный матч ===")
    if "TotalGoals" in df.columns:
        max_goals_row = df.loc[df["TotalGoals"].idxmax()]
        print(f"{max_goals_row['HomeTeam']} {max_goals_row['FTHG']}-{max_goals_row['FTAG']} {max_goals_row['AwayTeam']} (Всего голов: {max_goals_row['TotalGoals']})")
    else:
        print("Ошибка: Колонка TotalGoals отсутствует.")

    # 4. Команда с лучшей разницей голов
    print("\n=== 4. Команда с лучшей разницей голов ===")
    if "HomeTeam" in df.columns and "AwayTeam" in df.columns:
        home_stats = df.groupby("HomeTeam").agg({"FTHG": "sum", "FTAG": "sum"})
        away_stats = df.groupby("AwayTeam").agg({"FTAG": "sum", "FTHG": "sum"})
        goal_diff = (home_stats["FTHG"] - home_stats["FTAG"] + away_stats["FTAG"] - away_stats["FTHG"]).sort_values(ascending=False)
        print(f"Лучшая разница: {goal_diff.idxmax()} ({goal_diff.max()} голов)")
    else:
        print("Ошибка: Колонки HomeTeam или AwayTeam отсутствуют.")

    # 5. Топ-5 самых частых результатов
    print("\n=== 5. Топ-5 самых частых результатов ===")
    if "FTHG" in df.columns and "FTAG" in df.columns:
        score_counts = df.groupby(["FTHG", "FTAG"]).size().sort_values(ascending=False).head(5)
        print(score_counts.to_string())
    else:
        print("Ошибка: Колонки FTHG или FTAG отсутствуют.")

    # 6. Анализ пенальти
    print("\n=== 6. Анализ пенальти ===")
    if "HR" in df.columns and "AR" in df.columns:
        total_penalties = df["HR"].sum() + df["AR"].sum()
        print(f"Всего пенальти: {total_penalties}")
    else:
        print("Колонки с пенальти отсутствуют")

    # 7. Самый активный рефери
    print("\n=== 7. Самый активный рефери ===")
    if "Referee" in df.columns:
        df["Referee"] = df["Referee"].fillna("Unknown")
        top_referee = df["Referee"].value_counts().head(1)
        print(f"Рефери: {top_referee.index[0]} (матчей: {top_referee.values[0]})")
    else:
        print("Колонка Referee отсутствует.")
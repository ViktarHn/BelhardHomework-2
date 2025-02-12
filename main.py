from data_loader import DataLoader
import pandas as pd

# Создание объекта и загрузка данных
loader = DataLoader()
loader.load_from_csv("season-2324.csv")

if loader.data is not None:
    df = loader.data

    # 1. Общее количество матчей
    print("\n=== 1. Общее количество матчей ===")
    print(f"Всего матчей: {df.shape[0]}")

    # 2. Топ-5 домашних команд по победам
    print("\n=== 2. Топ-5 домашних команд по победам ===")
    home_wins = df[df["FTR"] == "H"]["HomeTeam"].value_counts().head(5)
    print(home_wins.to_string())

    # 3. Самый результативный матч
    print("\n=== 3. Самый результативный матч ===")
    df["TotalGoals"] = df["FTHG"] + df["FTAG"]
    max_goals_row = df.loc[df["TotalGoals"].idxmax()]
    print(
        f"{max_goals_row['HomeTeam']} {max_goals_row['FTHG']}-{max_goals_row['FTAG']} {max_goals_row['AwayTeam']} "
        f"(Всего голов: {max_goals_row['TotalGoals']})"
    )

    # 4. Команда с лучшей разницей голов
    print("\n=== 4. Команда с лучшей разницей голов ===")
    home_stats = df.groupby("HomeTeam").agg({"FTHG": "sum", "FTAG": "sum"})
    away_stats = df.groupby("AwayTeam").agg({"FTAG": "sum", "FTHG": "sum"})
    goal_diff = (home_stats["FTHG"] - home_stats["FTAG"] + away_stats["FTAG"] - away_stats["FTHG"]).sort_values(ascending=False)
    print(f"Лучшая разница: {goal_diff.idxmax()} ({goal_diff.max()} голов)")

    # 5. Топ-5 самых частых результатов
    print("\n=== 5. Топ-5 самых частых результатов ===")
    score_counts = df.groupby(["FTHG", "FTAG"]).size().sort_values(ascending=False).head(5)
    print(score_counts.to_string())

    # 6. Анализ пенальти
    print("\n=== 6. Анализ пенальти ===")
    if "HR" in df.columns and "AR" in df.columns:
        total_penalties = df["HR"].sum() + df["AR"].sum()
        print(f"Всего пенальти: {total_penalties}")
    else:
        print("Колонки с пенальти отсутствуют")

    # 7. Самый активный рефери
    print("\n=== 7. Самый активный рефери ===")
    df["Referee"] = df["Referee"].fillna("Unknown")
    top_referee = df["Referee"].value_counts().head(1)
    print(f"Рефери: {top_referee.index[0]} (матчей: {top_referee.values[0]})")

else:
    print("Данные не загружены.")
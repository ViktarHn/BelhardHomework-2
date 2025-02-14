from data_loader import DataLoader

loader = DataLoader()
loader.load_from_csv("season-2324.csv")

# Отчет о пропусках
loader.report_missing_values()

# Удаляем полностью пустой столбец
loader.data.drop(columns=["Referee"], inplace=True)

# Заполняем числовые столбцы медианой
loader.fill_missing_values(strategy="median", columns=["FTHG", "FTAG"])

# Проверяем результат
loader.report_missing_values()
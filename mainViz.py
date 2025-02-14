from data_loader import DataLoader

# 1. Создаем объект DataLoader
loader = DataLoader()

# 2. Загружаем данные из CSV
loader.load_from_csv("season-2324.csv")

# 3. Строим графики (после загрузки данных!)
loader.add_histogram("FTHG", "hist_goals")  # Гистограмма голов домашней команды
loader.add_line_plot("Date", "FTHG", "line_goals")  # Линейный график
loader.add_scatter_plot("HS", "AS", "scatter_shots")  # Диаграмма рассеяния

# 4. Сохранить все графики в файлы
for name, fig in loader.figures.items():
    fig.savefig(f"{name}.png")
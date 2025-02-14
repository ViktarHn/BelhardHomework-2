import pandas as pd
import requests
import matplotlib.pyplot as plt

class DataLoader:
    def __init__(self):
        self.data = None
        self.figures = {}  # Для хранения графиков

    def load_from_csv(self, file_path):
        """Загрузка данных из CSV файла."""
        try:
            self.data = pd.read_csv(file_path)
            print("Данные успешно загружены из CSV.")
        except Exception as e:
            print(f"Ошибка при загрузке CSV: {e}")

    def load_from_json(self, file_path):
        """Загрузка данных из JSON файла."""
        try:
            self.data = pd.read_json(file_path)
            print("Данные успешно загружены из JSON.")
        except Exception as e:
            print(f"Ошибка при загрузке JSON: {e}")

    def load_from_api(self, url):
        """Загрузка данных из API."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.data = pd.DataFrame(response.json())
                print("Данные успешно загружены из API.")
            else:
                print(f"Ошибка при запросе к API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при загрузке из API: {e}")
    def add_histogram(self, column, figure_name, bins=15, color='skyblue', 
                     edgecolor='black', title=None, save_path=None):
        """Создание гистограммы с использованием библиотеки matplotlib
        
        Параметры:
        - column: столбец для построения
        - figure_name: имя для сохранения в коллекции
        - bins: количество интервалов (по умолчанию 15)
        - color: цвет столбцов
        - edgecolor: цвет границ
        - title: заголовок графика
        - save_path: путь для сохранения в файл (например, 'plot.png')
        """
        if self.data is None:
            print("Ошибка: Данные не загружены.")
            return
        if column not in self.data.columns:
            print(f"Ошибка: Столбец '{column}' не найден.")
            return
        
        fig = plt.figure()
        plt.hist(self.data[column], bins=bins, color=color, edgecolor=edgecolor)
        
        # Заголовок
        if title:
            plt.title(title)
        else:
            plt.title(f"Гистограмма: {column}")
        # Добавить здесь подписи осей
        plt.xlabel(column)                 # <-- Вставить эту строку
        plt.ylabel("Частота")              # <-- Вставить эту строку
        # Сохранение
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        self.figures[figure_name] = fig
        plt.show()

    def add_line_plot(self, x_column, y_column, figure_name, color='blue', 
                     marker='o', linestyle='-', linewidth=1, title=None, 
                     save_path=None):
        """Создание линейного графика с использованием библиотеки matplotlib."""
        if self.data is None:
            print("Ошибка: Данные не загружены.")
            return
        if x_column not in self.data.columns or y_column not in self.data.columns:
            print("Ошибка: Столбец не найден.")
            return
        
        fig = plt.figure()
        plt.plot(
            self.data[x_column], 
            self.data[y_column], 
            color=color, 
            marker=marker, 
            linestyle=linestyle,
            linewidth=linewidth
        )
        
        if title:
            plt.title(title)
        else:
            plt.title(f"Линейный график: {x_column} vs {y_column}")
        # Добавить здесь подписи осей
        plt.xlabel(x_column)               # <-- Вставить эту строку
        plt.ylabel(y_column)               # <-- Вставить эту строку
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        self.figures[figure_name] = fig
        plt.show()

    def add_scatter_plot(self, x_column, y_column, figure_name, color='red', 
                        marker='o', s=20, title=None, save_path=None):
        """Создание диаграммы рассеяния с использованием библиотеки matplotlib."""
        if self.data is None:
            print("Ошибка: Данные не загружены.")
            return
        if x_column not in self.data.columns or y_column not in self.data.columns:
            print("Ошибка: Столбец не найден.")
            return
        
        fig = plt.figure()
        plt.scatter(
            self.data[x_column], 
            self.data[y_column], 
            color=color, 
            marker=marker,
            s=s  # Размер точек
        )
        
        if title:
            plt.title(title)
        else:
            plt.title(f"Диаграмма рассеяния: {x_column} vs {y_column}")
        # Добавить здесь подписи осей
        plt.xlabel(x_column)               # <-- Вставить эту строку
        plt.ylabel(y_column)               # <-- Вставить эту строку
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        self.figures[figure_name] = fig
        plt.show()

    def remove_visualization(self, figure_name):
        """Удаление графика."""
        if figure_name in self.figures:
            plt.close(self.figures[figure_name])
            del self.figures[figure_name]
            print(f"График '{figure_name}' удален.")
        else:
            print(f"График '{figure_name}' не найден.")
    
    def count_missing_values(self):
        """Подсчет пропущенных значений в каждом столбце."""
        if self.data is None:
            print("Ошибка: Данные не загружены.")
            return None
        return self.data.isna().sum()

    def report_missing_values(self):
        """Отчет о пропущенных значениях."""
        missing = self.count_missing_values()
        if missing is None:
            return
            
        print("\n" + "="*40)
        print("Отчет о пропущенных значениях:")
        print("="*40)
        
        if missing.sum() == 0:
            print("Пропущенных значений не обнаружено!")
            return

        for col, count in missing.items():
            if count > 0:
                print(f"- Столбец '{col}': {count} пропусков ({count/len(self.data)*100:.1f}%)")

    def fill_missing_values(self, strategy='mean', columns=None):
        """Заполнение пропущенных значений.
    
        Параметры:
        - strategy: 
            - 'mean', 'median' (только для числовых столбцов), 
            - 'mode' (для любых типов данных),
            - конкретное значение (например, 0 или 'N/A').
    - columns: список столбцов для обработки (по умолчанию все).
    
        Возвращает:
            None
        """
        if self.data is None:
            print("Ошибка: Данные не загружены.")
            return

        if columns is None:
            columns = self.data.columns

        for col in columns:
            if col not in self.data.columns:
                print(f"Предупреждение: Столбец '{col}' не существует.")
                continue

            # Проверка типа данных для стратегий mean/median
            if strategy in ['mean', 'median'] and not pd.api.types.is_numeric_dtype(self.data[col]):
                print(f"Предупреждение: Стратегия '{strategy}' неприменима к нечисловому столбцу '{col}'. Пропуск.")
                continue

            # Логика заполнения
            try:
                if strategy == 'mean':
                    fill_value = self.data[col].mean()
                elif strategy == 'median':
                    fill_value = self.data[col].median()
                elif strategy == 'mode':
                    fill_value = self.data[col].mode()[0]
                else:  # Конкретное значение
                    fill_value = strategy
            
                self.data[col].fillna(fill_value, inplace=True)
                print(f"Столбец '{col}': пропуски заполнены ({strategy}).")
            except Exception as e:
                print(f"Ошибка при заполнении столбца '{col}': {e}")
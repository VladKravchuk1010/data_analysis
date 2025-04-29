import pandas as pd
import re


def clean_column_name(column_name):
    """
    Преобразует название колонки в SQL-дружелюбный формат:
    - Заменяет пробелы и спецсимволы на подчёркивания
    - Удаляет скобки и единицы измерения
    - Приводит к нижнему регистру (опционально)
    """
    if column_name.startswith("20") or column_name.startswith("19"):
        return "population_" + column_name[:4]
    # Удаляем всё в скобках и спецсимволы
    cleaned = re.sub(r'\([^)]*\)', '', column_name)  # Удаляет (km²) и подобное
    cleaned = re.sub(r'[^\w\s]', '', cleaned)  # Удаляет оставшиеся спецсимволы
    cleaned = cleaned.strip()  # Убирает пробелы по краям
    cleaned = re.sub(r'\s+', '_', cleaned)  # Заменяет пробелы на _
    return cleaned.lower()  # Приводим к нижнему регистру


def process_csv(input_path, output_path):
    """Читает CSV, переименовывает колонки и сохраняет новый файл"""
    df = pd.read_csv(input_path)

    # Переименовываем все колонки
    new_columns = {col: clean_column_name(col) for col in df.columns}
    df = df.rename(columns=new_columns)

    # Сохраняем результат
    df.to_csv(output_path, index=False)
    print(f"Файл успешно обработан и сохранён как {output_path}")
    print("Новые названия колонок:", list(df.columns))


# Пример использования
if __name__ == "__main__":
    input_csv = "../data/world_population.csv"  # Исходный файл
    output_csv = "../data/world_population.csv"  # Обработанный файл

    process_csv(input_csv, output_csv)
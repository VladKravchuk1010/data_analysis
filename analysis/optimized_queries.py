import sqlite3
import time
from itertools import groupby
from textwrap import dedent


def display_help():
    """Показывает инструкции по использованию"""
    print("\n" + "=" * 50)
    print("📋 ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ".center(50))
    print("=" * 50)
    print(dedent("""
    1. Для анализа доступны данные о населении за годы:
       1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022
    2. Можно вводить как полное название страны, так и часть названия
    3. Для значений по умолчанию вводите 'n'
    """))


def display_countries(conn):
    """Выводит список всех стран с группировкой по первой букве"""
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT countryterritory FROM world_population ORDER BY countryterritory")
    countries = [row[0] for row in cursor.fetchall()]

    print("\n" + "=" * 50)
    print("🌍 СПИСОК ДОСТУПНЫХ СТРАН 🌎".center(50))
    print("=" * 50)

    for letter, group in groupby(countries, key=lambda x: x[0].upper()):
        country_group = list(group)
        print(f"\n🔠 {letter}:")
        for i in range(0, len(country_group), 5):
            print(", ".join(country_group[i:i + 5]))


def get_user_input(conn):
    """Получает параметры от пользователя"""
    display_help()
    display_countries(conn)

    print("\n" + "🔹 НАСТРОЙКА ПАРАМЕТРОВ 🔹".center(50, "~"))

    # Ввод года с валидацией
    while True:
        print("\n╔" + "═" * 48 + "╗")
        print("║ {:^46} ║".format("ВВЕДИТЕ ГОД ДЛЯ АНАЛИЗА (1970-2022)"))
        print("╚" + "═" * 48 + "╝")
        year = input(">>> Ваш выбор (или 'n' для 2022): ").strip().lower()

        if not year:
            year = "2022"
            break
        if year == 'n':
            year = "2022"
            break
        if year.replace("_", "").isdigit() and int(year.replace("_", "")) in range(1970, 2023):
            year = year.replace("_", "")
            break
        print("⚠️ Ошибка: введите корректный год между 1970 и 2022")

    # Ввод страны
    print("\n╔" + "═" * 48 + "╗")
    print("║ {:^46} ║".format("ВВЕДИТЕ НАЗВАНИЕ СТРАНЫ ИЗ СПИСКА"))
    print("╚" + "═" * 48 + "╝")
    country = input(">>> Ваш выбор (или 'n' для China/India): ").strip().lower()
    if not country or country == 'n':
        country = "china"

    # Ввод периода для анализа изменений
    print("\n" + "=" * 50)
    print("📅 ВЫБЕРИТЕ ПЕРИОД ДЛЯ АНАЛИЗА ИЗМЕНЕНИЯ НАСЕЛЕНИЯ".center(50))
    print("=" * 50)

    while True:
        print("\n╔" + "═" * 48 + "╗")
        print("║ {:^46} ║".format("ВВЕДИТЕ НАЧАЛЬНЫЙ ГОД (1970-2020)"))
        print("╚" + "═" * 48 + "╝")
        start_year = input(">>> Ваш выбор (по умолчанию 1970): ").strip()
        if not start_year:
            start_year = "1970"
            break
        if start_year.replace("_", "").isdigit() and int(start_year.replace("_", "")) in range(1970, 2021):
            break
        print("⚠️ Ошибка: введите корректный год между 1970 и 2020")

    while True:
        print("\n╔" + "═" * 48 + "╗")
        print("║ {:^46} ║".format(f"ВВЕДИТЕ КОНЕЧНЫЙ ГОД ({int(start_year) + 1}-2022)"))
        print("╚" + "═" * 48 + "╝")
        end_year = input(">>> Ваш выбор (по умолчанию 2022): ").strip()
        if not end_year:
            end_year = "2022"
            break
        if (end_year.replace("_", "").isdigit() and
                int(end_year.replace("_", "")) > int(start_year) and
                int(end_year.replace("_", "")) <= 2022):
            break
        print(f"⚠️ Ошибка: введите год между {int(start_year) + 1} и 2022")

    return year, country, start_year, end_year


def run_optimized_query(conn, query, description, params=None):
    """Выполняет оптимизированный запрос"""
    cursor = conn.cursor()

    start_time = time.time()
    cursor.execute(query, params) if params else cursor.execute(query)
    results = cursor.fetchall()
    end_time = time.time()

    # Форматирование результатов
    print("\n" + "🔹 РЕЗУЛЬТАТЫ 🔹".center(50, "~"))
    print(f"\n📌 {description}")
    print(f"⏱ Время выполнения: {end_time - start_time:.4f} сек")

    if results:
        print("\n" + " ТОП РЕЗУЛЬТАТОВ ".center(50, "="))
        for i, row in enumerate(results[:15], 1):
            formatted_row = []
            for item in row:
                if isinstance(item, (int, float)):
                    formatted_num = f"{abs(item):,}"
                    if item < 0:
                        formatted_num = f"-{formatted_num}"
                    formatted_row.append(formatted_num)
                else:
                    formatted_row.append(str(item))
            print(f"{i}. {' | '.join(formatted_row)}")
    else:
        print("\n⚠️ Нет результатов для отображения")
    print("=" * 50)


def main():
    print("\n" + "=" * 50)
    print("🌎 АНАЛИЗ ДАННЫХ О НАСЕЛЕНИИ МИРА 🌏".center(50))
    print("=" * 50)

    # Подключение к БД
    conn = sqlite3.connect("../database/world_population.db")

    # Создание индексов
    conn.executescript("""
    CREATE INDEX IF NOT EXISTS idx_country ON world_population(countryterritory);
    CREATE INDEX IF NOT EXISTS idx_population_years ON world_population(
        population_1970, population_1980, population_1990, 
        population_2000, population_2010, population_2015,
        population_2020, population_2022
    );
    """)

    # Получение параметров от пользователя
    year, country, start_year, end_year = get_user_input(conn)

    # 1. Запрос топа стран
    query1 = f"""
    SELECT countryterritory, population_{year} 
    FROM world_population 
    WHERE population_{year} > 10000000 
    ORDER BY population_{year} DESC
    LIMIT 15
    """
    run_optimized_query(conn, query1, f"Топ стран по населению в {year} году")

    # 2. Поиск стран
    query2 = """
    SELECT countryterritory, population_2022 
    FROM world_population 
    WHERE LOWER(countryterritory) LIKE ? 
    ORDER BY population_2022 DESC
    LIMIT 15
    """
    run_optimized_query(conn, query2, f"Результаты поиска по '{country}'", (f"%{country}%",))

    # 3. Анализ изменения населения (абсолютный прирост)
    query3 = f"""
    SELECT 
        countryterritory,
        population_{start_year},
        population_{end_year},
        (population_{end_year} - population_{start_year}) AS population_growth,
        ROUND((population_{end_year} - population_{start_year}) * 100.0 / 
            NULLIF(population_{start_year}, 0), 2) AS growth_percent
    FROM world_population
    WHERE population_{start_year} IS NOT NULL
      AND population_{end_year} IS NOT NULL
      AND population_{start_year} > 0
    ORDER BY population_growth DESC
    LIMIT 15
    """
    run_optimized_query(conn, query3,
                        f"Страны с наибольшим приростом населения ({start_year}-{end_year})")

    # 4. Анализ изменения населения (процентный рост)
    query4 = f"""
    SELECT 
        countryterritory,
        population_{start_year},
        population_{end_year},
        (population_{end_year} - population_{start_year}) AS population_growth,
        ROUND((population_{end_year} - population_{start_year}) * 100.0 / 
            NULLIF(population_{start_year}, 0), 2) AS growth_percent
    FROM world_population
    WHERE population_{start_year} IS NOT NULL
      AND population_{end_year} IS NOT NULL
      AND population_{start_year} > 1000000 
    ORDER BY growth_percent DESC
    LIMIT 15
    """
    run_optimized_query(conn, query4,
                        f"Страны с наибольшим процентным ростом ({start_year}-{end_year})")

    conn.close()
    print("\n" + "=" * 50)
    print(" АНАЛИЗ ЗАВЕРШЁН ".center(50, "✨"))
    print("=" * 50)


if __name__ == "__main__":
    main()
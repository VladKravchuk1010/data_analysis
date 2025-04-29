import sqlite3
import time


def run_query(query, description):
    conn = sqlite3.connect("../database/world_population.db")
    cursor = conn.cursor()

    start_time = time.time()
    cursor.execute(query)
    results = cursor.fetchall()
    end_time = time.time()

    conn.close()

    print(f"\n🔹 {description}")
    print(f"⏱ Время выполнения: {end_time - start_time:.4f} сек")
    print(f"📊 Результат (первые 5 строк):")
    for row in results[:5]:
        print(row)


# ---------------------------------------------------------------------
# 1. Запрос с SELECT * и без индексов
query1 = """
SELECT rank, countryterritory, population_2022 
FROM world_population 
WHERE population_2022 > 100000000 
ORDER BY population_2022 DESC
"""
run_query(query1, "Топ стран с населением >100M в 2022 году")

# ---------------------------------------------------------------------
# 2. Запрос с LIKE и без индексов
query2 = """
SELECT countryterritory, population_2022 
FROM world_population 
WHERE countryterritory LIKE '%China%' 
   OR countryterritory LIKE '%India%'
"""
run_query(query2, "Поиск стран с 'China' или 'India'")

# ---------------------------------------------------------------------
# 3. Запрос с GROUP BY и HAVING
query3 = """
SELECT 
    continent,
    COUNT(*) AS Country_Count,
    SUM(population_2022) AS Total_Population
FROM world_population
GROUP BY continent
ORDER BY Total_Population DESC
"""
run_query(query3, "Население по континентам")

# ---------------------------------------------------------------------
# 4. Запрос с подзапросом
query4 = """
SELECT 
    countryterritory,
    population_2022,
    population_1970,
    (population_2022 - population_1970) AS Population_Growth
FROM world_population
ORDER BY Population_Growth DESC
LIMIT 10
"""
run_query(query4, "Страны с наибольшим приростом населения (1970-2022)")
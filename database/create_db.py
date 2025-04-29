import sqlite3
import pandas as pd

# Загрузка данных из CSV
df = pd.read_csv("../data/world_population.csv")

# Создание и подключение к БД
conn = sqlite3.connect("world_population.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS world_population (
    rank INTEGER,
    cca3 TEXT,
    countryterritory TEXT,
    capital TEXT,
    continent TEXT,
    population_2022 INTEGER,
    population_2020 INTEGER,
    population_2015 INTEGER,
    population_2010 INTEGER,
    population_2000 INTEGER,
    population_1990 INTEGER,
    population_1980 INTEGER,
    population_1970 INTEGER,
    area INTEGER,
    density REAL,
    growth_rate REAL,
    world_population_percentage REAL
)
""")

# Запись данных в БД
df.to_sql("world_population", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

print("База данных успешно создана!")

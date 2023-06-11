import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from models.database import get_db
from models.models import University
import numpy as np
import geopy
import requests
import folium

def get_data():
    # Получаем данные из базы данных
    db = next(get_db())
    q = db.query(University).all()
    data = [[i.name, i.city, i.salary, i.average_ege, i.percent_remaining_students] for i in q]
    df = pd.DataFrame(data, columns=['name', 'city', 'salary', 'average_ege', 'percent_remaining_students'])

    unique_cities = df['city'].unique()  # Получить все уникальные города
    city_coordinates = {}  # Словарь для хранения координат каждого города

    for city in unique_cities:
        if city not in city_coordinates:
            lat, lon = get_coordinates(city)  # Запросить координаты только один раз для каждого города
            city_coordinates[city] = (lat, lon)

    df['latitude'], df['longitude'] = zip(*df['city'].map(city_coordinates))  # Присвоить координаты каждому городу в DataFrame
    return df


def get_coordinates(city):
    print(f"Получение координат для города {city}")
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}"
    response = requests.get(url).json()
    if response:
        return response[0]['lat'], response[0]['lon']
    else:
        return np.nan, np.nan

def visualize_data():
    df = get_data()
    russia_center = [61.5240, 105.3188]
    folium_map = folium.Map(location=russia_center, zoom_start=3)

    min_avg_ege = df['average_ege'].min()
    max_avg_ege = df['average_ege'].max()

    min_salary = df['salary'].min()
    max_salary = df['salary'].max()

    for index, row in df.iterrows():
        size = 10 + 40 * (row['average_ege'] - min_avg_ege) / (max_avg_ege - min_avg_ege)

        normalized_salary = (row['salary'] - min_salary) / (max_salary - min_salary)
        color = sns.color_palette("RdYlGn", as_cmap=True)(normalized_salary)

        folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=size, color=color,
                            fill=True, fill_color=color).add_to(folium_map)

    folium_map.save('src/data/map.html')

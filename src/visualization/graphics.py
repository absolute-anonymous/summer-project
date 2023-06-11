import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from models.database import get_db
from models.models import University

def get_data():
    # Получаем данные из базы данных
    db = next(get_db())
    q = db.query(University).all()
    
    # Создаем DataFrame на основе полученных данных
    df = pd.DataFrame([[i.name, i.city, i.salary, i.average_ege, i.percent_remaining_students] for i in q],
                        columns=['name', 'city', 'salary', 'average_ege', 'percent_remaining_students'])
    return df

def plot_average_ege_salary_by_city():
    # Получаем данные
    df = get_data()
    
    # Группируем данные по городу и вычисляем средние значения
    grouped_city = df.groupby('city').mean().reset_index()

    # Сортируем города по убыванию среднего балла ЕГЭ
    sorted_city_ege = grouped_city.sort_values('average_ege', ascending=False)

    # Создаем график среднего балла ЕГЭ по городам
    plt.figure(figsize=(12, 8))
    barplot_ege = sns.barplot(data=sorted_city_ege, x='city', y='average_ege')
    plt.xlabel('Город', fontsize=12)
    plt.ylabel('Средний балл ЕГЭ', fontsize=12)
    plt.title('Средний балл ЕГЭ по городам', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.tight_layout()
    plt.savefig('src/data/average_ege_by_city.png', dpi=300)
    plt.close()

    # Сортируем города по убыванию средней зарплаты
    sorted_city_salary = grouped_city.sort_values('salary', ascending=False)

    # Создаем график средней зарплаты по городам
    plt.figure(figsize=(12, 8))
    barplot_salary = sns.barplot(data=sorted_city_salary, x='city', y='salary')
    plt.xlabel('Город', fontsize=12)
    plt.ylabel('Зарплата', fontsize=12)
    plt.title('Средняя зарплата по городам', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.tight_layout()
    plt.savefig('src/data/average_salary_by_city.png', dpi=300)
    plt.close()

def plot_salary_histogram():
    # Получаем данные
    df = get_data()

    # Создаем гистограмму распределения зарплаты
    plt.figure(figsize=(12, 8))  # Увеличиваем размер графика для лучшей видимости
    histplot = sns.histplot(data=df, x='salary', kde=True)
    plt.xlabel('Зарплата', fontsize=12)  # Увеличиваем размер шрифта метки оси x
    plt.ylabel('Количество', fontsize=12)  # Увеличиваем размер шрифта метки оси y
    plt.title('Распределение зарплаты', fontsize=14)  # Увеличиваем размер шрифта заголовка
    plt.tight_layout()  # Регулируем расстояние между графиками
    plt.savefig('src/data/salary_histogram.png', dpi=300)  # Увеличиваем dpi для получения более высокого разрешения
    plt.close()
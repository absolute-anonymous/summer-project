import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from models.database import get_db
from models.models import University
import numpy as np

def get_data():
    db = next(get_db())
    q = db.query(University).all()
    # df from db.query where id from column id
    df = pd.DataFrame([[i.name, i.city, i.salary, i.average_ege, i.percent_remaining_students] for i in q]
                        , columns=['name', 'city', 'salary', 'average_ege', 'percent_remaining_students'])
    print(df.head())
    return df


# 1. Гистограмма распределения зарплат
def plot_salary_histogram():
    df = get_data()
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='salary', bins=20)
    plt.title('Salary Histogram')
    plt.savefig('data/salary_histogram.png')
    plt.close()

# 2. Тепловая карта связи среднего балла ЕГЭ и зарплаты
def plot_correlation_heatmap():
    df = get_data()
    plt.figure(figsize=(10, 6))
    sns.heatmap(data=df[['average_ege', 'salary']].corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap: Average EGE and Salary')
    plt.savefig('data/correlation_heatmap.png')
    plt.close()

# 3. Группировка данных по городам и визуализация среднего балла и средней зп в зависимости от города
def plot_average_ege_salary_by_city():
    df = get_data()
    grouped_city = df.groupby('city').mean().reset_index()
    plt.figure(figsize=(12, 8))
    barplot_ege = sns.barplot(data=grouped_city, x='city', y='average_ege')
    plt.xlabel('City', fontsize=12)
    plt.ylabel('Average EGE', fontsize=12)
    plt.title('Average EGE by City', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('data/average_ege_by_city.png', dpi=300)
    plt.close()

    plt.figure(figsize=(12, 8))
    barplot_salary = sns.barplot(data=grouped_city, x='city', y='salary')
    plt.xlabel('City', fontsize=12)
    plt.ylabel('Salary', fontsize=12)
    plt.title('Average Salary by City', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('data/average_salary_by_city.png', dpi=300)
    plt.close()



# 4. Нормализация значений средней зарплаты и визуализация
def plot_salary_histogram():
    df = get_data()

    plt.figure(figsize=(12, 8))  # Increase the figure size for better visibility
    histplot = sns.histplot(data=df, x='salary', kde=True)
    plt.xlabel('Salary', fontsize=12)  # Increase the font size of x-axis label
    plt.ylabel('Count', fontsize=12)  # Increase the font size of y-axis label
    plt.title('Distribution of Salary', fontsize=14)  # Increase the font size of the title
    plt.tight_layout()  # Adjust the spacing between subplots
    plt.savefig('data/salary_histogram.png', dpi=300)  # Increase the dpi for higher resolution
    plt.close()


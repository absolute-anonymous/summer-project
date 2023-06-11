import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

from models.database import create_all_tables, get_db, drop_all_tables
from models.models import University
from scrapers.scraper import scrape_data
from visualization.graphics import (
    plot_salary_histogram,
    plot_average_ege_salary_by_city
)
from visualization.geo import visualize_data

app = FastAPI()

@app.get('/files/{file_name}')
def get_file(file_name: str):
    if file_name not in os.listdir('src/data'):
        raise HTTPException(status_code=404, detail='Файл не найден')
    return FileResponse(f'src/data/{file_name}')

@app.get('/files')
def get_files():
    files = os.listdir('src/data')
    return {'files': files}

if __name__ == '__main__':
    create_all_tables()  # Создаем все таблицы в базе данных
    scrape_data()  # Собираем данные с веб-сайта
    time.sleep(3)  # Ждем 3 секунды для завершения сбора данных

    plot_salary_histogram()  # Создаем гистограмму зарплаты
    plot_average_ege_salary_by_city()  # Создаем графики среднего балла ЕГЭ и зарплаты по городам

    visualize_data()  # Создаем географическую визуализацию данных

    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
from models.database import get_db
from models.models import University

def scrape_data():
    browser = webdriver.Chrome()
    ref = 'https://students.superjob.ru/reiting-vuzov/ekonomicheskie/'
    browser.get(ref)
    time.sleep(2)
    browser.execute_script("window.scrollTo(0, 4000)")
    time.sleep(3)
    soup = BeautifulSoup(browser.page_source, features="lxml")
    table = soup.find('table', class_="UniversityRating_table")

    db = next(get_db())
    for row in table.find_all('tr', class_='ng-scope'):
        columns = row.find_all('td')

        name = columns[2].find('div', class_='UniversityRating_table_vuz_name').text.strip()
        city = columns[2].find('span', class_='UniversityRating_table_vuz_city').text.strip()
        salary = columns[3].find('span', class_='ng-binding').text.strip()
        ege = columns[4].text.strip()
        remaining = columns[5].find('span', class_='ng-binding').text.strip()

        ege = ege.replace('*', '')
        ege = ege.replace(',', '.')
        if re.match(r'^-?\d+(?:\.\d+)?$', ege):
            ege = float(ege)
        else:
            ege = None
        

        salary = int(''.join(salary.split()))
        remaining = int(''.join(remaining.split()))

        university = University(
            name=name,
            city=city,
            salary=salary,
            average_ege=ege,
            percent_remaining_students=remaining
        )
        db.add(university)
    db.commit()

import time
from models.database import create_all_tables, get_db, drop_all_tables
from models.models import University
from scrapers.scraper import scrape_data
from visualization import (
    plot_average_ege_barplot,
    plot_correlation_heatmap,
    plot_average_ege_salary_by_city,
    plot_salary_histogram,
)

if __name__ == '__main__':
    drop_all_tables()

    create_all_tables()  # Create database tables if they don't exist
    scrape_data()  # Scrape data and save to PostgreSQL
    time.sleep(10)  # Wait for 5 seconds to make sure that data is saved

    # Run data visualization functions
    plot_average_ege_barplot()
    plot_correlation_heatmap()
    plot_average_ege_salary_by_city()
    plot_salary_histogram()

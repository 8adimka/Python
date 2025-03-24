HeadHunter Searcher Project - Quick search for current vacancies across the entire HeadHunters database via API.
You can identify companies you are interested in(config.py), set parameters(api_client.py) and receive a selection of vacancies.
You can use this selection in your other pipe-lines.

Project Structure
Head_hunter_DB_search_project/
│
├── dto/                      # Data Transfer Objects package
│   ├── __init__.py           # Package initialization
│   └── models.py             # DTO classes (Employer, Vacancy)
│
├── __init__.py               # Root package initialization
├── api_client.py             # HeadHunterAPI class for HH.ru API interactions
├── db_manager.py             # DBManager class for PostgreSQL operations
├── services.py               # DataCollector service for data processing
├── config.py                 # Configuration parameters (DATABASE_CONFIG, COMPANIES)
├── main.py                   # Main application entry point
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── print_data.py             # Show and work with results from DataBase
│
└── volumes/                  # Database volume for Docker
    └── HH_database_vacancies.db  # PostgreSQL data files

Prerequisites
Python 3.9+

Docker (for containerized PostgreSQL)

PostgreSQL client tools (optional)

Installation and Setup
Clone the repository:

git clone <repository_url>
cd Head_hunter_DB_search_project
Create and activate virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/MacOS
# or
venv\Scripts\activate     # Windows
Install dependencies:

pip install -r requirements.txt
Database Setup with Docker
Create Docker volume directory:

mkdir -p volumes/HH_database_vacancies.db

Run PostgreSQL container:

docker run --name hh_vacancies_db \
  -e POSTGRES_DB=HH_vacancies \
  -e POSTGRES_USER=v \
  -e POSTGRES_PASSWORD=123 \
  -p 5432:5432 \
  -v /home/v/Python/Head_hunter_DB_search_project/volumes/HH_vacancies.db:/var/lib/postgresql/data \
  -d postgres:13


Verify container is running:

docker ps


Configuration
Create .env file:

cat > .env <<EOF
DB_NAME=HH_database_vacancies
DB_USER=v
DB_PASSWORD=123
DB_HOST=localhost
DB_PORT=5432
EOF
Optional: Modify config.py if you need to change company list or other settings.

Running the Application
Populate the database:

python main.py
Expected output:

Начало сбора данных...
Обработка компании: Яндекс...
Добавлено 23 вакансий для Яндекс
Обработка компании: Сбер...
Добавлено 15 вакансий для Сбер
...
Сбор данных завершен!
Using the DBManager
After data collection, you can use DBManager methods directly:

from db_manager import DBManager

with DBManager() as manager:
    # Get companies and vacancies count
    print(manager.get_companies_and_vacancies_count())
    
    # Get average salary
    print(f"Average salary: {manager.get_avg_salary():.2f} RUB")
    
    # Search for Python vacancies
    print(manager.get_vacancies_with_keyword("python"))
Troubleshooting
Connection issues:

Verify PostgreSQL container is running

Check .env file values match Docker container settings

Test connection with:

psql -h localhost -U v -d HH_database_vacancies
Permission issues:

Ensure your user has write permissions to volumes directory

sudo chown -R $USER:$USER volumes/


Docker cleanup:
If you need to start fresh:

docker stop hh_vacancies_db
docker rm hh_vacancies_db
rm -rf volumes/HH_database_vacancies.db/*

from db_manager import DBManager
from config import DATABASE_CONFIG

# Подключаемся к БД
with DBManager(DATABASE_CONFIG) as db:
    # 1. Список всех компаний и количество вакансий
    print("Компании и количество вакансий:")
    for company in db.get_companies_and_vacancies_count():
        print(f"{company['name']}: {company['vacancies_count']}")

    # 2. Все вакансии с деталями
    print("\nВсе вакансии:")
    for vacancy in db.get_all_vacancies():
        print(f"{vacancy['company_name']} - {vacancy['vacancy_name']}")
        print(f"Зарплата: {vacancy['salary_from']}-{vacancy['salary_to']} {vacancy['salary_currency']}")
        print(f"Ссылка: {vacancy['url']}\n")

    # 3. Вакансии с зарплатой выше средней
    avg_salary = db.get_avg_salary()
    print(f"\nСредняя зарплата: {avg_salary:.2f} RUB")
    print("Вакансии с зарплатой выше средней:")
    for vacancy in db.get_vacancies_with_higher_salary():
        print(f"{vacancy['company_name']}: {vacancy['vacancy_name']}")

    # 4. Поиск по ключевому слову
    keyword = "python"
    print(f"\nВакансии по ключевому слову '{keyword}':")
    for vacancy in db.get_vacancies_with_keyword(keyword):
        print(f"{vacancy['company_name']}: {vacancy['vacancy_name']}")

# def interactive_menu():
#     """Интерактивное меню для работы с данными"""
#     with DBManager(DATABASE_CONFIG) as db:
#         while True:
#             print("\n" + "="*50)
#             print("Меню работы с вакансиями")
#             print("1. Показать все компании и количество вакансий")
#             print("2. Показать все вакансии")
#             print("3. Показать среднюю зарплату")
#             print("4. Показать вакансии с зарплатой выше средней")
#             print("5. Поиск вакансий по ключевому слову")
#             print("0. Выход")
            
#             choice = input("Выберите пункт меню: ")
            
#             if choice == "1":
#                 print("\nКомпании и количество вакансий:")
#                 for company in db.get_companies_and_vacancies_count():
#                     print(f"{company['name']}: {company['vacancies_count']}")
            
#             elif choice == "2":
#                 print("\nВсе вакансии:")
#                 for vacancy in db.get_all_vacancies():
#                     print(f"\n{vacancy['company_name']} - {vacancy['vacancy_name']}")
#                     print(f"Зарплата: {vacancy['salary_from']}-{vacancy['salary_to']} {vacancy['salary_currency']}")
#                     print(f"Ссылка: {vacancy['url']}")
            
#             elif choice == "3":
#                 avg = db.get_avg_salary()
#                 print(f"\nСредняя зарплата: {avg:.2f} RUB")
            
#             elif choice == "4":
#                 print("\nВакансии с зарплатой выше средней:")
#                 for vacancy in db.get_vacancies_with_higher_salary():
#                     print(f"{vacancy['company_name']}: {vacancy['vacancy_name']}")
            
#             elif choice == "5":
#                 keyword = input("Введите ключевое слово: ")
#                 print(f"\nРезультаты поиска по '{keyword}':")
#                 for vacancy in db.get_vacancies_with_keyword(keyword):
#                     print(f"{vacancy['company_name']}: {vacancy['vacancy_name']}")
            
#             elif choice == "0":
#                 break
#             else:
#                 print("Неверный ввод, попробуйте снова")

# if __name__ == "__main__":
#     # Если нужно просто собрать данные
#     # collect_and_analyze_data()
    
#     # Для интерактивной работы
#     interactive_menu()
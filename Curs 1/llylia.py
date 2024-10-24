income = int(input("Введите ваш доход в месяц: "))

necessity_jar = round ((income * 0.55), 1) # Текущие расходы
financial_freedom_jar = round ((income * 0.1), 1)  # Финансовая свобода
education_jar = round ((income * 0.1), 1)  # Образование
savings_jar = round ((income * 0.1), 1) # Резервный фонд
play_jar = round ((income * 0.1), 1) # Развлечения
give_jar = round ((income * 0.05), 1) # Благотворительность и подарки

necessity_lost = necessity_jar - 750 - 100

print(f"Текущие расходы {necessity_jar}")
print(f"Остатки по текущим расходам за вычетом 750 евро за квартиру и 100 евро на коммуналку -> {necessity_lost}")
print(f"Финансовая свобода {financial_freedom_jar}")
print(f"Образование {education_jar}")
print(f"Резервный фонд {savings_jar}")
print(f"Развлечения {play_jar}")
print(f"Благотворительность и подарки {give_jar}")
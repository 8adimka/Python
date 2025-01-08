import math

def ticket_price(age):

	if 0 <= age < 7 or age >= 60:
		return "Бесплатно"
	elif 7 <=  age < 18:
		return "100 рублей"
	elif 18 <= age < 25:
		return "200 рублей"
	elif 25 <= age < 60:
		return  "300 рублей" 
	else:
		return "Ошибка"
	
def get_circle_square(radius):

	if type(radius) not in [int, float]:
		raise TypeError("Должно быть int или float больше 0")

	if radius < 0:
		raise ValueError("Должно быть int или float больше 0")

	return round(radius ** 2 * math.pi, 2)

def get_verbal_grade(grade):
    if type(grade) != int: raise TypeError("Должно быть целое между 2 и 5")
    if grade < 2 or grade > 5: raise ValueError("Должно быть между 2 и 5")

    if grade == 2:
        return "Плохо"

    elif grade == 3:
        return "Удовлетворительно"

    elif grade == 4:
        return "Хорошо"

    elif grade == 5:
        return "Отлично"
	
def get_period(hour):

    if type(hour) != int: raise TypeError("Должно быть int")
    if hour < 0 or hour > 24: raise ValueError("Допустимое значение 0-24")

    if hour < 7:
        return "ночь"
    elif hour < 12:
        return "утро"
    elif hour < 18:
        return "день"   
    else:
        return "вечер"

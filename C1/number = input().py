stars = input('Введите оценку звездочками - ')
number_stars = stars.count('*')
if number_stars == 5:
	print("Прекрасная поездка!")
elif number_stars == 4:
  print("Всё в порядке")
elif number_stars == 3: 
  print("Средненько")
elif number_stars == 2:
  print("Очень плохо")
else:
	print("Ужасно")
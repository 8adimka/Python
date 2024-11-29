import json
import os

students_json = [
	{ 
		"pk": 1,
		"full_name":  "Jane Snake",
		"skills": ["Python", "Go", "Linux"]
	},
	{ 
		"pk": 2,
		"full_name":  "Sheri Torres",
		"skills": ["Java", "Swift", "Fortran", "Basic"]
	},
	{ 
		"pk": 3,
		"full_name":  "Burt Stein",
		"skills": ["Planning", "Negotiation", "Management", "Sales"]
	},
	{ 
		"pk": 4,
		"full_name":  "Bauer Adkins",
		"skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"]
	}
]

professions_json = [
	{
		"pk": 1,
		"title": "Backend",
		"skills": ["Python", "Linux", "Docker", "SQL", "Flask"]
  },
	{
		"pk": 2,
		"title": "Frontend",
		"skills": ["HTML", "CSS", "React", "JavaScript"]
  },
	{
		"pk": 3,
		"title": "Testing",
		"skills": ["Windows", "MacOS", "SQL", "Jira"]
  }
]

students_json_path = os.path.join ('C:\\', 'Users', 'm8adi', 'Desktop', 'Python', 'Curs 2.Lecture 2', 'students_json.json')
professions_json_path = os.path.join ('C:\\', 'Users', 'm8adi', 'Desktop', 'Python', 'Curs 2.Lecture 2', 'professions_json.json')


with open (students_json_path, 'w') as file:
    json.dump (students_json, file)

with open (professions_json_path, 'w') as file:
    json.dump (professions_json, file)
    
while True:
    user_student_number = input ('Введите номер студента\n->')
    with open (students_json_path) as file:
        students = json.load(file)
        user_student = 'zero'
        for student in students:
            if student["pk"] == int(user_student_number):
                user_student = student
    if  user_student == 'zero':
        print('У нас нет такого студента')
        break

    print (f'Студент {user_student["full_name"]}\nЗнает {user_student["skills"]}')
    
    user_profession_imput = input (f'Выберите специальность для оценки студента {user_student["full_name"]}\n->')
    with open (professions_json_path) as file:        
        professions = json.load(file)
        user_profession = 'zero'
        for profession in professions:
            if str(profession["title"]).lower() == user_profession_imput.lower():
                user_profession = profession
    if  user_profession == 'zero':
        print ('У нас нет такой специальности')
        break

    languages_known = set(user_profession["skills"]).intersection(set(user_student["skills"]))
    languages_do_not_known = set(user_profession["skills"]).difference(set(user_student["skills"]))

    suitability = round(len(languages_known)*100/len(user_profession["skills"]))

    print (f'Пригодность {suitability}%\n{user_student["full_name"]} знает', end= ' ')
    for language in languages_known:
        print (language, end=' ')
    print (f'\n{user_student["full_name"]} не знает', end=' ')
    for language in languages_do_not_known:
        print (language, end=' ')
    break




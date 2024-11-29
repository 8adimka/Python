import os
import json

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

def get_path (file_name):
    return os.path.join ('C:\\', 'Users', 'm8adi', 'Desktop', 'Python', 'Curs 2.Lecture 2', f'{file_name}')

def load_data_to_file (file_name, data):
    '''Выгружает выбранные данные в файл с произвольным названием'''
    file_path = get_path (file_name)
    with open (file_path, 'w') as file:
        json.dump (data, file)

def load_data_from_file (file_name):
    '''Загружает данные из файла по его названию и возвращает их'''
    file_path = get_path (file_name)
    with open (file_path) as file:
        return json.load(file)
    
def find_student (students):
    '''Находим и возвращаем студента по номеру от ввода пользователя'''
    user_input = input('Введите номер студента\n->')
    if user_input.isdigit():
        for student in students:
            if student["pk"] == int(user_input):
                return student
    return None

def find_profession (professions, student):
    '''Находим и возвращаем искомую профессию от ввода пользователя'''
    user_input = input(f'Выберите специальность для оценки студента {student["full_name"]}\n->')
    for profession in professions:
        if profession["title"].lower() == user_input.lower():
            return profession
    return None

def get_statistics (student, profession):
    '''Расчитывает и выводит статистику'''
    languages_known = set(profession["skills"]).intersection(set(student["skills"]))
    languages_do_not_known = set(profession["skills"]).difference(set(student["skills"]))
    suitability = round(len(languages_known)*100/len(profession["skills"]))

    print (f'Пригодность {suitability}%')
    if languages_known!=set():
        print (f'{student["full_name"]} знает {" ".join(list (languages_known))}')

    if languages_do_not_known!=set():
        print (f'{student["full_name"]} не знает {" ".join(languages_do_not_known)}')


def main ():
    load_data_to_file ('students_json.json', students_json)
    load_data_to_file ('professions_json.json', professions_json)

    students = load_data_from_file ('students_json.json')
    professions = load_data_from_file ('professions_json.json')

    student = find_student (students)
    if student==None:
        print ('У нас нет такого студента')
    else:
        print (f'Студент {student["full_name"]}\nЗнает {" ".join(student["skills"])}')
        profession = find_profession (professions, student)
        if profession==None:
            print ('У нас нет такой специальности')
        else:
            get_statistics (student, profession)

main()


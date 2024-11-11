# def get_unique_names (names):
#     names_set = set (names)
#     return list (names_set)

# names = ["Yvor", "Wendell", "Hogan", "Sadella", "Yvor", "Sadella", "Hogan"]
# unique_names = get_unique_names(names)

# print(unique_names)



users = [{
  "id": 1,
  "first_name": "Anthia",
  "url": "https://weather.com/aliquet/at/feugiat/non/pretium.jsp",
  "color": "Yellow"
}, {
  "id": 2,
  "first_name": "Tobit",
  "url": "http://pen.io/sapien/cursus/vestibulum/proin/eu/mi/nulla.json",
  "color": "Teal"
}, {
  "id": 3,
  "first_name": "Pace",
  "url": "http://ucsd.edu/justo/morbi/ut/odio/cras/mi.json",
  "color": "Yellow"
}, {
  "id": 4,
  "first_name": "Andreas",
  "url": "https://ifeng.com/morbi/vestibulum/velit.png",
  "color": "Maroon"
}, {
  "id": 5,
  "first_name": "Anthia",
  "url": "https://google.com/eu/orci.aspx",
  "color": "Teal"
}, {
  "id": 6,
  "first_name": "Tobit",
  "url": "https://google.com/eu/orci.aspx",
  "color": "Yellow"
}]

# def get_names_from_user_list(users):
#     names_list = []
#     for user in users:
#         names_list.append (user['first_name'])
    
#     unique_names = []

#     for name in names_list:
#         if name not in unique_names:
#             unique_names.append (name)
#             print (name)
#     return unique_names

# get_names_from_user_list(users)



# def get_names_from_user_list(users):
#     unique_names = set()  # Используем set для автоматического исключения дубликатов
#     for user in users:
#         unique_names.add(user['first_name'])
    
#     # Печатаем каждое уникальное имя
#     for name in unique_names:
#         print(name)

# # Вызов функции
# get_names_from_user_list(users)



# import json

# raw_json = {"name":"Алиска-сосиска", "is_online":True, "status":None}

# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 2\first_JSON.json', 'w') as file:
#     json.dump (raw_json, file)

# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 2\first_JSON.json', 'r') as file:
#     print (json.load(file))



# def get_ids(users):
#     return [user["id"] for user in users]

# print(get_ids(users))



# def filter_yellow_only(animals):
#     for user in animals:
#         if user["color"] == "Yellow":
#             print (f'{user["first_name"]} favorit color is yelloy!')

# filter_yellow_only (users)



# def get_names_sorted(animals):
#     names = [user["first_name"] for user in animals]
#     return sorted (names)

# print (get_names_sorted(users))



comments = [{
  "author": "Werner",
  "time": "2:14 PM",
  "comment": "Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi.",
  "post_id": 3
}, {
  "author": "Raymond",
  "time": "12:48 PM",
  "comment": "Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede.",
  "post_id": 5
}, {
  "author": "Silvio",
  "time": "2:45 PM",
  "comment": "Nullam sit amet turpis elementum ligula vehicula consequat. Morbi a ipsum. Integer a nibh.",
  "post_id": 1
}, {
  "author": "Shelbi",
  "time": "1:29 AM",
  "comment": "Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.",
  "post_id": 5
}, {
  "author": "Barnabas",
  "time": "2:28 PM",
  "comment": "Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum.",
  "post_id": 5
}, {
  "author": "Mariellen",
  "time": "6:51 AM",
  "comment": "Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris.",
  "post_id": 1
}, {
  "author": "Brandon",
  "time": "1:29 AM",
  "comment": "Sed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus.",
  "post_id": 2
}]

# def get_comments_by_post_id(comments, post_id):
#     return [comment for comment in comments if comment["post_id"] == post_id]

# dict_com = get_comments_by_post_id(comments, 1)
# for com in dict_com:
#     print (com["comment"])



# first = [1,2,3,4,5]
# second = [4,5,6,7]

# def count_common (first, second):
#     first_set = set(first)
#     second_set = set(second)
#     return len(first_set.intersection(second_set))

# print (count_common (first, second))



# first = [4,5,6,7]
# second = [1,2,3,4,5,6,7]
# def count_unique(first,second):
#     return set(first).difference(set(second))
    
# result = count_unique(first,second)
# print(result)



tasks = [
   "сходить в магазин" , 
   "купить гвозди", 
   "полить сельдерей",
   "украсить елку",
   "нарисовать снежинку",
   "найти открытки"
]

emp_1 = ["купить гвозди", "найти открытки"]
emp_2 = ["полить сельдерей","сходить в магазин"]
emp_3 = ["найти открытки","купить гвозди"]

done_set = set(emp_1+emp_2+emp_3)
print (set(tasks).difference(done_set))

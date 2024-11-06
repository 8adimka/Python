from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/card')
def user_card():
    # Данные пользователя
    user_data = {
        "username": "alexy_001",
        "email": "alexy@skyeng.ru",
        "phone": "+1555223311"
    }
    # Передача данных в шаблон
    return render_template('user_card.html', **user_data)



@app.route('/city')
def cites ():
    c_dict = {
        1: "Самара",
        2: "Краснодар",
        3: "Сочи",
        4: "Новосибирск",
        5: "Вышгород"
        }
    return render_template('city.html', c_dict = c_dict)



ws = [
    "платина", "стена", "халат", "блокнот", "косилка", 
    "автобус", "базар", "биосфера", "грелка"
]
@app.route('/search/')
def search():
    query = request.args.get('s', '') # Получаем именованный ('s') input из HTML-документа
    results = []

    if query: 
        results = [word for word in ws if query.lower() in word.lower()] # Приводим к нижнему регистру для нечувствительности к регистру

    return render_template('search.html', results=results if query else None)



@app.route('/form/')
def user_form():
    username = request.args.get('username', '')
    level = request.args.get('level', '')

    if username or level:
        with open (r'C:\Users\m8adi\Desktop\Python\C3L2\records.txt', 'a', encoding='utf-8') as file:
            file.write (f'username : {username}, level : {level}\n')
    
    return render_template('user_form.html')


DATA_BASE = {'v': 'Killer1911!', 'm8adimka': 'Killer1911!'}
@app.route('/', methods=['GET', 'POST'])
def user_password():
    username = request.form.get('username', '').lower()
    password = request.form.get('password', '')

    if username in DATA_BASE and DATA_BASE[username] == password:
        results = username
    else:
        results = False

    return render_template('user_password.html', results=results)

# @app.route('/', methods=['GET', 'POST'])
# def user_password():
#     results = None
#     if request.method == 'POST':
#         username = request.form.get('username', '').lower()  # Получаем username из формы, приводим к нижнему регистру
#         password = request.form.get('password', '')  # Получаем password из формы

#         # Проверка данных в базе
#         if username in DATA_BASE and DATA_BASE[username] == password:
#             results = username  # Если данные корректны, сохраняем имя пользователя
#         else:
#             results = False  # Если данные неверны, указываем доступ запрещен

#     return render_template('user_password.html', results=results)

if __name__ == "__main__":
    app.run()

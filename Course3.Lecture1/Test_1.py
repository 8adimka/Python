from flask import Flask
app = Flask (__name__)

# from flask import Response
# import json
# words_2 = ["@кот", "@хлеб", "не", "ешь", "@подумай", "теперь", "ешь"]
# @app.route('/mentions/')
# def get_mentions ():
#     mentions = [word[1:] for word in words_2 if word[0]=='@']
#     return Response (json.dumps(mentions, ensure_ascii=False), content_type='application/json; charset=utf-8')

num_list = [23, 16, 144, 72, 90, 11, 5]
@app.route('/<num>/')
def get_num (num):
    if num.lower() == 'first':
        return str(num_list[0])
    elif num.lower() == 'last':
        return str(num_list[-1])
    elif num.lower() == 'sum':
        return str(sum(num_list))
    else:
        return 'Неизвестный запрос'

content = "Кот - это не хлеб, подумай, не ешь его, разработчик! Ай, ну я же просил"
@app.route('/')
def page_index ():
    return content
@app.route("/profile/")
def page_profile():
    return "Профиль пользователя"
@app.route("/feed/")
def page_feed():
    return "Лента пользователя"
@app.route("/messages/")
def page_messages():
    return "Сообщения пользователя"

@app.route('/hello/')
def hello_page():
    return 'hello'
@app.route('/bye/')
def bye_page():
    return 'bye'
@app.route('/seeyou/')
def seeyou_page():
    return 'seeyou'

import random
@app.route('/random/')
def random_num():
    return f'{random.randint(0, 10)}'

words_1 = {"one":"один", "two": "два", "three": "три"}
@app.route('/numb/<numero>/')
def num_camb (numero):
    new_num = words_1 [numero]
    return str (new_num)

words_2 = ["@кот", "@хлеб", "не", "ешь", "@подумай", "теперь", "ешь"]
@app.route('/mentions/')
def get_mentions ():
    mentions = [word[1:] for word in words_2 if word[0]=='@']
    return ', '.join(mentions)

@app.route('/words/')
def words_count ():
    str_without_sym = content.translate(str.maketrans('','','-,!'))
    str_without_sym_1 = str_without_sym.replace ('  ', ' ')
    str_list = str_without_sym_1.split(' ')
    return str (len(str_list))

@app.route('/spaces/')
def spaces_count ():
    return str (content.count(' '))

@app.route('/letters/')
def letters_count ():
    str_without_sym = content.translate(str.maketrans('','',' -,!'))
    str_list = list(str_without_sym)
    return str (len(str_list))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)








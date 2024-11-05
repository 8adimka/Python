from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def user_card():
    # Данные пользователя
    user_data = {
        "username": "alexy_001",
        "email": "alexy@skyeng.ru",
        "phone": "+1555223311"
    }
    # Передача данных в шаблон
    return render_template('user_card.html', **user_data)

if __name__ == '__main__':
    app.run()
    
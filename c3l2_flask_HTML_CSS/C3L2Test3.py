from flask import Flask, render_template, request
import requests

u_dict = [{"username": "alexy_001", "email": "alexy@skyeng.ru", "phone": "+1555223311"},
          {"username": "gimly_002", "email": "gimly@skyeng.ru", "phone": "+1512312311"},
          {"username": "pepin_001", "email": "pepin@smail.com", "phone": "+1559999999"}]

app = Flask (__name__)

@app.route ('/contacts/')
def dict_page ():
    return render_template('test3_dict.html', u_dict=u_dict)

@app.route ('/', methods=['GET', 'POST'])
def reg_page ():

    return render_template ('test3_reg.html')

@app.route ('/add/')
def add_page():
    telephone = request.args.get('telephone', '')
    if telephone:
        with open ('/home/v/Python/C3L2/records.txt', 'a', encoding='utf-8') as file:
            file.write (f"{telephone}\n")

    extra = request.args.get('extra', '')
    while extra:
        with open ('/home/v/Python/C3L2/records.txt', 'a', encoding='utf-8') as file:
            file.write (f"{extra}\n")
        extra = request.args.get('extra', '')
    return render_template ('test3_add.html')

@app.route ('/adress/')
def adress_page ():
    town = request.args.get('town', '')
    street = request.args.get('street', '')
    house = request.args.get('house', '')
    additions = request.args.get('additions', '')
    if town or street or house or additions:
        with open ('/home/v/Python/C3L2/records.txt', 'a', encoding='utf-8') as file:
            file.write (f"Город - {town}\nУлица - {street}\nДом - {house}\nДоп. - {additions}")
    return render_template ('test3_adress.html')

if __name__ == ('__main__'):
    app.run (debug=True)

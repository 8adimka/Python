from flask import Flask, render_template, request
import random

app = Flask (__name__)

@app.route('/python')
def python_page ():
    return 'это язык который мы учим!'
@app.route('/java')
def java_page ():
    return 'а это мы не учим'
@app.route('/php')
def php_page ():
    return 'а это что такое вообще?'

@app.route('/rl')
def get_random_letter ():
    alphabet = "ABCDEFGHIKLMNOPQRSTVXYZ"
    return random.choice(alphabet)

if __name__ == '__main__':
    app.run()


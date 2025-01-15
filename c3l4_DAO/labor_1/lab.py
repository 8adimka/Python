from config import Config
import os
import dotenv

from flask import Flask

app = Flask(__name__)

print(os.environ)
print(os.environ.get('USER'))

dotenv.load_dotenv(override=True)
if os.environ.get("APP_CONFIG") == "testing": #Параметр "APP_CONFIG" - устанавливается в файле .env в папке проекта (этот файл лучше убрать в .gitignore)
    app.config.from_pyfile('config/testing_config.py')
else:
    app.config.from_pyfile('config/work_config.py')
user = os.environ.get('USER')
print(user)
print(os.environ)

config = Config ()
print (config.file_path)

file_path = Config().file_path
print (file_path)




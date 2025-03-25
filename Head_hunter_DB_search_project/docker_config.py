import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

DATABASE_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

COMPANIES = [
    # Текущие компании
    {'id': 1740, 'name': 'Яндекс'},
    {'id': 3529, 'name': 'Сбер'},
    {'id': 78638, 'name': 'Тинькофф'},
    {'id': 2748, 'name': 'Ростелеком'},
    {'id': 41862, 'name': 'ВКонтакте'},
    {'id': 3776, 'name': 'МТС'},
    {'id': 1373, 'name': 'Авито'},
    {'id': 87021, 'name': 'Wildberries'},
    {'id': 4934, 'name': 'Билайн'},
    {'id': 907345, 'name': 'Ozon'},
    
    # Запрошенные компании
    {'id': 3388, 'name': 'Газпромбанк'},
    {'id': 54979, 'name': 'Росатом'},
    {'id': 80, 'name': 'Альфа-Банк'},
    
    # Международные ИТ-компании (офисы в России)
    {'id': 15478, 'name': 'Microsoft Россия'},
    {'id': 2870783, 'name': 'LATOKEN'},
    {'id': 407, 'name': 'IBM Россия'},
    {'id': 1122462, 'name': 'SAP СНГ'},
    
    # Другие крупные российские ИТ-компании
    {'id': 41862, 'name': 'VK (бывш. Mail.ru Group)'},
    {'id': 2324020, 'name': 'Ростелеком СолаРам'},
    {'id': 6093775, 'name': 'СберТех'},
    {'id': 4504679, 'name': 'Яндекс.Технологии'},

    {'id': 407, 'name': 'IBM'},
    {'id': 15478, 'name': 'Microsoft'},
    {'id': 1122462, 'name': 'SAP'},
    {'id': 4770322, 'name': 'DCloud'},
    {'id': 2381, 'name': 'Softline'},
    
    # Кибербезопасность
    {'id': 1057, 'name': 'Kaspersky Lab'},
    {'id': 64174, 'name': 'Positive Technologies'},
    
    {'id': 5201237, 'name': 'ITACWT'},
    {'id': 6075298, 'name': 'Likesoft'},
    {'id': 1111058, 'name': 'Hi, Rockits!'}
]

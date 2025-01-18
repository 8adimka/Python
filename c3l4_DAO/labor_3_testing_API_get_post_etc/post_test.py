import pytest
from post import app

def test_json():
    data = {"name": "Alice"}
    response = app.test_client().post('/', json=data, follow_redirects=True) #Еcли вы отправляете запрос, а в представлении установлен редирект,
    #то нужно разрешить редиректы, иначе запрос уткнется в 308-й статус-код.
    # Чтобы разрешить редиректы, добавьте к запросу follow_redirects=True
    
    assert response.json == {"name_received" : "Alice"}
    assert response.status_code == 200

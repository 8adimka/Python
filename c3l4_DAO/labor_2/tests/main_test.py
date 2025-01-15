class TestMain:

    def test_root_status(self, test_client):
        """ Проверяем, получается ли нужный статус-код и """
        response = test_client.get('/', follow_redirects=True)
        assert response.status_code == 200, "Статус-код всех постов неверный"

    def test_root_content(self, test_client):
        response = test_client.get('/', follow_redirects=True)
        html = response.data.decode('utf-8')  # Преобразуем байты в строку
        assert "Это главная страница" in html, "Контент страницы неверный"
        assert "В вакансии!" in html, "Контент страницы неверный"
        
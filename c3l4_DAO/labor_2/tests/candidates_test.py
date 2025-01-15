class TestCandidates:

    def test_all_candidates_status(self, test_client):
        """ Проверяем при запросе кандидатов нужный статус-код """
        response = test_client.get('/candidates', follow_redirects=True)
        assert response.status_code == 200, "Статус-код запроса кандидатов не ок"

    def test_single_candidate_status(self, test_client):
        """ Проверяем при запросе одного кандидата нужный статус-код """
        response = test_client.get('/candidates/1', follow_redirects=True)
        assert response.status_code == 200, "Статус код запроса кандидата не ок"
        
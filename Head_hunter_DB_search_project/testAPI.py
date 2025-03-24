from api_client import HeadHunterAPI


if __name__ == "__main__":
    api = HeadHunterAPI()
    # Тестовый запрос
    employer = api.get_employer(1740)  # Яндекс
    print(employer)

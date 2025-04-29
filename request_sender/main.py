import random
from request_client import RequestClient
import time
import logging
from settings import CHECK_INTERVAL, DEBUG_MODE, MAX_RETRIES  # Добавлен MAX_RETRIES

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

def main():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            client = RequestClient()
            logging.info(f"Попытка {retries + 1}/{MAX_RETRIES}. Программа запущена.")
            
            try:
                # Загрузка начальной страницы с повторными попытками
                if not client.load_initial_page():
                    retries += 1
                    logging.warning(f"Не удалось загрузить начальную страницу. Попытка {retries}/{MAX_RETRIES}")
                    client.restart_browser()
                    time.sleep(random.randint(10, 30))  # Случайная задержка
                    continue
                
                # Последовательность шагов
                steps = [
                    ("Выбор провинции", client.select_province, ["Alicante"], "province_selection_error"),
                    ("Выбор trámite", client.select_tramite, ["POLICIA- EXPEDICIÓN/RENOVACIÓN DE DOCUMENTOS DE SOLICITANTES DE ASILO"], "tramite_selection_error"),
                    ("Отправка информации", client.submit_info_page, [], "info_page_error"),
                    ("Заполнение данных", client.fill_personal_data, [], "personal_data_error")
                ]
                
                for step_name, step_func, args, error_screenshot in steps:
                    logging.info(f"Выполняется шаг: {step_name}")
                    if not step_func(*args):
                        retries += 1
                        if DEBUG_MODE:
                            client.save_error_screenshot(error_screenshot)
                        logging.warning(f"Ошибка на шаге '{step_name}'. Попытка {retries}/{MAX_RETRIES}")
                        client.restart_browser()
                        time.sleep(random.randint(10, 30))
                        break
                else:
                    # Все шаги выполнены успешно
                    result = client.check_slots()
                    
                    if result["status"] == "slots_available":
                        logging.critical("НАЙДЕНЫ СВОБОДНЫЕ МЕСТА!")
                        client.send_telegram_alert("СРОЧНО: Доступны citas!", result.get("html_path"))
                        return  # Успешное завершение
                    elif result["status"] == "blocked":
                        logging.critical("ОБНАРУЖЕНА БЛОКИРОВКА!")
                        if DEBUG_MODE:
                            client.save_error_screenshot("blocked_page")
                        retries += 1
                        time.sleep(random.randint(30, 60))  # Увеличенная задержка при блокировке
                    else:
                        logging.info(f"Нет мест. Повторная проверка через {CHECK_INTERVAL} сек...")
                        time.sleep(CHECK_INTERVAL)
                        retries = 0  # Сброс счетчика при успешном цикле
                        
            except Exception as e:
                logging.error(f"Критическая ошибка: {str(e)}")
                retries += 1
                if DEBUG_MODE:
                    client.save_error_screenshot(f"critical_error_{retries}")
                client.restart_browser()
                time.sleep(random.randint(30, 60))

        except KeyboardInterrupt:
            logging.info("Прервано пользователем.")
            return
            
    logging.error(f"Достигнуто максимальное количество попыток ({MAX_RETRIES}). Программа остановлена.")

if __name__ == "__main__":
    main()
    
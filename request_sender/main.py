from request_client import RequestClient
import time
import logging
from settings import CHECK_INTERVAL_SECONDS, DEBUG_MODE

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
    client = RequestClient()
    try:
        logging.info("Программа запущена. Нажмите Ctrl+C для остановки.")
        while True:
            try:
                logging.info("Начинаем новую проверку...")
                
                if not client.load_initial_page():
                    raise Exception("Не удалось загрузить начальную страницу")
                
                if not client.select_province("Alicante"):
                    if DEBUG_MODE:
                        client.save_error_screenshot("province_selection_error")
                    raise Exception("Ошибка выбора провинции")
                
                if not client.select_tramite("POLICIA- EXPEDICIÓN/RENOVACIÓN DE DOCUMENTOS DE SOLICITANTES DE ASILO"):
                    if DEBUG_MODE:
                        client.save_error_screenshot("tramite_selection_error")
                    raise Exception("Ошибка выбора trámite")
                
                if not client.submit_info_page():
                    if DEBUG_MODE:
                        client.save_error_screenshot("info_page_error")
                    raise Exception("Ошибка на странице информации")
                
                if not client.fill_personal_data():
                    if DEBUG_MODE:
                        client.save_error_screenshot("personal_data_error")
                    raise Exception("Ошибка заполнения данных")
                
                result = client.check_slots()
                
                if result["status"] == "slots_available":
                    logging.critical("НАЙДЕНЫ СВОБОДНЫЕ МЕСТА!")
                    client.send_telegram_alert("СРОЧНО: Доступны citas!", result.get("html_path"))
                    break
                elif result["status"] == "blocked":
                    logging.critical("ОБНАРУЖЕНА БЛОКИРОВКА! Программа остановлена.")
                    if DEBUG_MODE:
                        client.save_error_screenshot("blocked_page")
                    break
                
                logging.info(f"Нет мест. Повторная проверка через {CHECK_INTERVAL_SECONDS} сек...")
                time.sleep(CHECK_INTERVAL_SECONDS)
                
            except Exception as e:
                logging.error(f"Ошибка в основном цикле: {str(e)}")
                if DEBUG_MODE:
                    client.save_error_screenshot("main_loop_error")
                client.restart_browser()
                time.sleep(10)

    except KeyboardInterrupt:
        logging.info("Прервано пользователем.")
    finally:
        if not DEBUG_MODE:
            client.close()
        else:
            logging.info("Режим отладки: браузер остается открытым")

if __name__ == "__main__":
    main()

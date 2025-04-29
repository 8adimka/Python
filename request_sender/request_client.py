import os
import time
import random
import logging
import uuid
import requests
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, PERSONAL_DATA, WAIT_TIMEOUT, DEBUG_MODE

class RequestClient:
    def __init__(self):
        self.driver = self._init_driver()
        self.base_url = "https://icp.administracionelectronica.gob.es"
        self.current_url = ""
        self.random_delay = lambda: time.sleep(random.uniform(0.5, 2.5))  # Более короткие случайные задержки

    def _init_driver(self):
        options = uc.ChromeOptions()
        
        # Настройки профиля
        if DEBUG_MODE:
            # В режиме отладки используем постоянный профиль
            options.add_argument("--user-data-dir=/home/v/.config/selenium-profile")
        else:
            # В продакшене используем новый профиль для каждой сессии
            options.add_argument(f"--user-data-dir=/tmp/chrome_profile_{uuid.uuid4()}")
        
        # Общие настройки
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        
        # Случайный User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        ]
        options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # Инициализация драйвера
        driver = uc.Chrome(
            options=options,
            headless=False,
            use_subprocess=True
        )
        
        # Установка случайного размера окна
        width = random.randint(1200, 1400)
        height = random.randint(800, 1000)
        driver.set_window_size(width, height)
        
        return driver

    def _human_like_movement(self, element=None):
        """Имитация человеческих движений мыши"""
        try:
            if element:
                # Плавное перемещение к элементу
                self.driver.execute_script("""
                    const element = arguments[0];
                    const rect = element.getBoundingClientRect();
                    const centerX = rect.left + rect.width/2;
                    const centerY = rect.top + rect.height/2;
                    
                    const mouseMove = (fromX, fromY, toX, toY, steps) => {
                        const dx = (toX - fromX) / steps;
                        const dy = (toY - fromY) / steps;
                        
                        for (let i = 0; i < steps; i++) {
                            window.dispatchEvent(new MouseEvent('mousemove', {
                                clientX: fromX + dx * i,
                                clientY: fromY + dy * i,
                                bubbles: true
                            }));
                        }
                    };
                    
                    mouseMove(
                        window.innerWidth/2, window.innerHeight/2,
                        centerX, centerY,
                        10 + Math.floor(Math.random() * 10)
                    );
                """, element)
            
            # Случайная прокрутка
            scroll_type = random.choice(["up", "down", "page"])
            if scroll_type == "up":
                self.driver.execute_script("window.scrollBy(0, -window.innerHeight/2);")
            elif scroll_type == "down":
                self.driver.execute_script("window.scrollBy(0, window.innerHeight/2);")
            else:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * Math.random());")
            
            self.random_delay()
            
        except Exception as e:
            logging.warning(f"Ошибка при имитации движений: {str(e)}")

    def load_initial_page(self):
        try:
            # Очистка cookies перед началом
            if not DEBUG_MODE:
                self.driver.delete_all_cookies()
            
            self.driver.get(f"{self.base_url}/icpco/acOpcDirect")
            self.random_delay()
            
            # Имитация активности пользователя
            self._human_like_movement()
            
            return not self._is_blocked()
            
        except Exception as e:
            logging.error(f"Ошибка загрузки начальной страницы: {str(e)}")
            self.save_error_screenshot("initial_page_load_error")
            return False

    def select_province(self, province_name):
        try:
            # Ожидание загрузки страницы
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
    lambda d: (
        "no hay citas disponibles" in d.page_source.lower() or
        "disponibilidad de citas" in d.page_source.lower() or
        self._is_blocked()
    )
)
            self._human_like_movement()

            # Проверка на блокировку
            if self._is_blocked():
                return False

            # Находим элемент select
            select_element = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.NAME, "form"))
            )
            self._human_like_movement(select_element)
            
            # Выбор провинции
            select = Select(select_element)
            select.select_by_visible_text(province_name)
            self.random_delay()

            # Нажатие кнопки Aceptar
            accept_button = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnAceptar"))
            )
            self._human_like_movement(accept_button)
            accept_button.click()
            self.random_delay()

            # Ожидание перехода
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.url_contains("/icpco/citar?p=")
            )
            self.current_url = self.driver.current_url
            
            return not self._is_blocked()
            
        except Exception as e:
            logging.error(f"Ошибка выбора провинции: {str(e)}")
            self.save_error_screenshot("province_selection_error")
            return False

    def _is_blocked(self):
        """Проверяет, заблокирован ли доступ"""
        blocked_texts = [
            "acceso denegado", "blocked", "detected unusual traffic",
            "error de seguridad", "distributed denial-of-service",
            "cloudflare", "captcha", "security check"
        ]
        page_text = self.driver.page_source.lower()
        return any(text in page_text for text in blocked_texts)

    def save_error_screenshot(self, prefix="error"):
        """Сохраняет скриншот и HTML страницы при ошибке"""
        os.makedirs("errors", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        screenshot_path = os.path.join("errors", f"{prefix}_{timestamp}.png")
        self.driver.save_screenshot(screenshot_path)
        logging.info(f"Сохранен скриншот ошибки: {screenshot_path}")
        
        html_path = os.path.join("errors", f"{prefix}_{timestamp}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        logging.info(f"Сохранен HTML ошибки: {html_path}")
        
        return screenshot_path, html_path

    def select_tramite(self, tramite_name):
        try:
            if not self.current_url:
                self.driver.get(f"{self.base_url}/icpco/citar?p=3&locale=es")
                self._human_like_movement()
            
            if self._is_blocked():
                logging.error("Обнаружена блокировка при выборе trámite")
                return False
            
            select_element = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "tramiteGrupo[1]"))
            )
            self._human_like_movement(select_element)
            
            select = Select(select_element)
            select.select_by_visible_text(tramite_name)
            self.random_delay()

            accept_button = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnAceptar"))
            )
            self._human_like_movement(accept_button)
            accept_button.click()
            self.random_delay()

            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.url_contains("/icpco/acInfo")
            )
            self.current_url = self.driver.current_url
            
            if self._is_blocked():
                logging.error("Обнаружена блокировка после выбора trámite")
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"Ошибка выбора trámite: {str(e)}")
            self.save_error_screenshot("tramite_selection_error")
            return False
        
    def submit_info_page(self):
        try:
            if self._is_blocked():
                logging.error("Обнаружена блокировка на странице информации")
                return False
                
            submit_button = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnEntrar"))
            )
            self._human_like_movement(submit_button)
            submit_button.click()
            self.random_delay()

            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.url_contains("/icpco/acEntrada")
            )
            self.current_url = self.driver.current_url
            
            if self._is_blocked():
                logging.error("Обнаружена блокировка после отправки info страницы")
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"Ошибка отправки info страницы: {str(e)}")
            self.save_error_screenshot("info_page_submit_error")
            return False

    def fill_personal_data(self):
        try:
            if self._is_blocked():
                logging.error("Обнаружена блокировка при заполнении данных")
                return False
                
            fields = {
                "txtIdCitado": PERSONAL_DATA["txtIdCitado"],
                "txtDesCitado": PERSONAL_DATA["txtDesCitado"],
                "txtAnnoCitado": PERSONAL_DATA["txtAnnoCitado"],
            }
            
            for field_id, value in fields.items():
                elem = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                    EC.presence_of_element_located((By.ID, field_id))
                )
                self._human_like_movement(elem)
                elem.clear()
                self.random_delay()
                
                # Имитация человеческого ввода
                for i, char in enumerate(value):
                    elem.send_keys(char)
                    if i % 3 == 0:  # Случайные паузы
                        time.sleep(random.uniform(0.05, 0.2))
            
            country_select = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "txtPaisNac"))
            )
            self._human_like_movement(country_select)
            
            select = Select(country_select)
            select.select_by_visible_text(PERSONAL_DATA["txtPaisNac"])
            self.random_delay()

            submit_button = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnAceptar"))
            )
            self._human_like_movement(submit_button)
            submit_button.click()
            self.random_delay()

            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.url_contains("/icpco/acValidarEntrada")
            )
            self.current_url = self.driver.current_url
            
            if self._is_blocked():
                logging.error("Обнаружена блокировка после заполнения данных")
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"Ошибка заполнения данных: {str(e)}")
            self.save_error_screenshot("personal_data_fill_error")
            return False
    
    def check_slots(self):
        try:
            if self._is_blocked():
                logging.error("Обнаружена блокировка при проверке слотов")
                return {"status": "blocked"}
                
            submit_button = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnEnviar"))
            )
            self._human_like_movement(submit_button)
            submit_button.click()
            self.random_delay()

            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                lambda d: "no hay citas disponibles" in d.page_source.lower() or 
                         "disponibilidad de citas" in d.page_source.lower() or
                         self._is_blocked()
            )
            
            if self._is_blocked():
                logging.error("Обнаружена блокировка при проверке слотов")
                return {"status": "blocked"}
            elif "no hay citas disponibles" in self.driver.page_source.lower():
                return {"status": "no_slots"}
            else:
                html_path = self._save_page_source()
                return {"status": "slots_available", "html_path": html_path}
                
        except Exception as e:
            logging.error(f"Ошибка проверки слотов: {str(e)}")
            self.save_error_screenshot("slots_check_error")
            return {"status": "error", "message": str(e)}

    def _save_page_source(self):
        os.makedirs("snapshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cita_available_{timestamp}.html"
        filepath = os.path.join("snapshots", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        
        return filepath

    def send_telegram_alert(self, message, html_path=None):
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": f"🚨 *{message}*\n\nСсылка: {self.driver.current_url}",
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": True
                },
                timeout=10
            )
            
            if html_path and os.path.exists(html_path):
                with open(html_path, 'rb') as doc:
                    requests.post(
                        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument",
                        files={"document": doc},
                        data={"chat_id": TELEGRAM_CHAT_ID, "caption": "Сохраненная страница с доступными citas"},
                        timeout=15
                    )
        except Exception as e:
            logging.error(f"Ошибка отправки в Telegram: {str(e)}")

    def restart_browser(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logging.error(f"Ошибка при закрытии браузера: {str(e)}")
        finally:
            time.sleep(3)  # Пауза перед перезапуском
            self.driver = self._init_driver()
            self.current_url = ""
            if not DEBUG_MODE:
                self.driver.delete_all_cookies()

    def close(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logging.error(f"Ошибка при закрытии браузера: {str(e)}")

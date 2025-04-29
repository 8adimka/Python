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
        self.random_delay = lambda: time.sleep(random.uniform(0.5, 3.0))

    def _init_driver(self):
        options = uc.ChromeOptions()
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        
        width = random.randint(1200, 1400)
        height = random.randint(800, 1000)
        options.add_argument(f"--window-size={width},{height}")
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"
        ]
        options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        if DEBUG_MODE:
            options.add_argument("--user-data-dir=/home/v/.config/selenium-profile")
        else:
            options.add_argument(f"--user-data-dir=/tmp/chrome_profile_{uuid.uuid4()}")
        
        driver = uc.Chrome(
            options=options,
            headless=False,
            use_subprocess=True
        )
        
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                window.navigator.chrome = {
                    runtime: {},
                };
            """
        })
        
        return driver

    def _handle_error_page(self):
        """Обработка страницы с ошибкой"""
        try:
            # Проверяем, есть ли кнопка Aceptar на странице с ошибкой
            accept_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "btnSubmit"))
            )
            self._human_like_movement(accept_button)
            accept_button.click()
            time.sleep(random.uniform(1, 3))
            
            # Проверяем, перешли ли мы на главную страницу
            if "icpco/index" in self.driver.current_url:
                return True
        except:
            pass
        return False

    def _human_like_movement(self, element=None):
        try:
            if element:
                self.driver.execute_script("""
                    const elem = arguments[0];
                    const rect = elem.getBoundingClientRect();
                    const targetX = rect.left + rect.width/2;
                    const targetY = rect.top + rect.height/2;
                    
                    const steps = 15 + Math.floor(Math.random() * 10);
                    const fromX = window.innerWidth/2 + (Math.random() * 200 - 100);
                    const fromY = window.innerHeight/2 + (Math.random() * 200 - 100);
                    
                    for (let i = 0; i <= steps; i++) {
                        const x = fromX + (targetX - fromX) * Math.pow(i/steps, 0.5);
                        const y = fromY + (targetY - fromY) * Math.pow(i/steps, 0.5);
                        
                        window.dispatchEvent(new MouseEvent('mousemove', {
                            clientX: x,
                            clientY: y,
                            bubbles: true
                        }));
                    }
                """, element)
            
            actions = [
                lambda: self.driver.execute_script("window.scrollBy(0, arguments[0]);", random.randint(-200, 200)),
                lambda: time.sleep(random.uniform(0.2, 1.5)),
                lambda: self.driver.execute_script("""
                    const x = Math.random() * window.innerWidth;
                    const y = Math.random() * window.innerHeight;
                    document.elementsFromPoint(x, y).forEach(el => {
                        el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                    });
                """)
            ]
            
            for _ in range(random.randint(1, 3)):
                random.choice(actions)()
            
        except Exception as e:
            logging.warning(f"Ошибка при имитации движений: {str(e)}")

    def _is_blocked(self):
        blocked_indicators = [
            "Se ha producido un error en el sistema",
            "Error 0301",
            "Cod. Oper.:",
            "Por favor inténtelo de nuevo",
            "blocked",
            "access denied",
            "distributed denial-of-service"
        ]
        
        try:
            page_text = self.driver.page_source.lower()
            if any(indicator.lower() in page_text for indicator in blocked_indicators):
                try:
                    error_code = self.driver.find_element(By.XPATH, "//*[contains(text(),'Cod. Oper.:')]").text
                    logging.error(f"Обнаружена блокировка. Код ошибки: {error_code}")
                except:
                    logging.error("Обнаружена блокировка (без кода ошибки)")
                return True
        except:
            pass
        
        return False

    def load_initial_page(self):
        try:
            # Пытаемся загрузить целевую страницу
            self.driver.get(f"{self.base_url}/icpco/acOpcDirect")
            time.sleep(random.uniform(1, 3))
            
            # Проверяем, не попали ли мы на страницу с ошибкой
            if self._is_blocked():
                # Если это страница с ошибкой, пробуем обработать её
                if self._handle_error_page():
                    logging.info("Успешно обработали страницу с ошибкой")
                    return True
                return False
            
            # Принятие cookies, если требуется
            try:
                cookie_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Aceptar cookies') or contains(.,'Acepto')]"))
                )
                self._human_like_movement(cookie_button)
                cookie_button.click()
                time.sleep(random.uniform(0.5, 1.5))
            except:
                pass
                
            return True
            
        except Exception as e:
            logging.error(f"Ошибка загрузки начальной страницы: {str(e)}")
            self.save_error_screenshot("initial_page_load_error")
            return False

    def save_error_screenshot(self, prefix="error"):
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

    # Остальные методы остаются без изменений (select_province, select_tramite и т.д.)
    def select_province(self, province_name):
        try:
            time.sleep(random.uniform(0.5, 2.0))
            
            # Ожидание загрузки страницы
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            if self._is_blocked():
                return False

            # Находим элемент select
            select_element = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.NAME, "form"))
            )
            self._human_like_movement(select_element)
            
            # Имитация человеческого выбора
            select = Select(select_element)
            time.sleep(random.uniform(0.3, 0.7))
            select.select_by_visible_text(province_name)
            time.sleep(random.uniform(0.5, 1.5))

            # Нажимаем кнопку подтверждения
            accept_button = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnAceptar"))
            )
            self._human_like_movement(accept_button)
            accept_button.click()
            time.sleep(random.uniform(1, 3))

            # Ожидание перехода на следующую страницу
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.url_contains("/icpco/citar?p=")
            )
            self.current_url = self.driver.current_url
            
            # Проверка на блокировку после действия
            return not self._is_blocked()
            
        except Exception as e:
            logging.error(f"Ошибка выбора провинции: {str(e)}")
            self.save_error_screenshot("province_selection_error")
            return False

    def select_tramite(self, tramite_name):
        try:
            time.sleep(random.uniform(0.5, 2.0))
            
            if not self.current_url:
                self.driver.get(f"{self.base_url}/icpco/citar?p=3&locale=es")
                self._human_like_movement()
            
            if self._is_blocked():
                logging.error("Обнаружена блокировка при выборе trámite")
                return False
            
            # Ожидание и выбор trámite
            select_element = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "tramiteGrupo[1]"))
            )
            self._human_like_movement(select_element)
            
            select = Select(select_element)
            time.sleep(random.uniform(0.5, 1.0))
            select.select_by_visible_text(tramite_name)
            time.sleep(random.uniform(0.7, 1.5))

            # Подтверждение выбора
            accept_button = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnAceptar"))
            )
            self._human_like_movement(accept_button)
            accept_button.click()
            time.sleep(random.uniform(1, 3))

            # Ожидание перехода
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.url_contains("/icpco/acInfo")
            )
            self.current_url = self.driver.current_url
            
            return not self._is_blocked()
            
        except Exception as e:
            logging.error(f"Ошибка выбора trámite: {str(e)}")
            self.save_error_screenshot("tramite_selection_error")
            return False
        
    def submit_info_page(self):
        try:
            time.sleep(random.uniform(0.5, 2.0))
            
            if self._is_blocked():
                logging.error("Обнаружена блокировка на странице информации")
                return False
                
            # Нажатие кнопки отправки
            submit_button = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnEntrar"))
            )
            self._human_like_movement(submit_button)
            submit_button.click()
            time.sleep(random.uniform(1, 3))

            # Ожидание перехода
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.url_contains("/icpco/acEntrada")
            )
            self.current_url = self.driver.current_url
            
            return not self._is_blocked()
            
        except Exception as e:
            logging.error(f"Ошибка отправки info страницы: {str(e)}")
            self.save_error_screenshot("info_page_submit_error")
            return False

    def fill_personal_data(self):
        try:
            time.sleep(random.uniform(0.5, 2.0))
            
            if self._is_blocked():
                logging.error("Обнаружена блокировка при заполнении данных")
                return False
                
            # Словарь с полями для заполнения
            fields = {
                "txtIdCitado": PERSONAL_DATA["txtIdCitado"],
                "txtDesCitado": PERSONAL_DATA["txtDesCitado"],
                "txtAnnoCitado": PERSONAL_DATA["txtAnnoCitado"],
            }
            
            # Заполнение текстовых полей с имитацией печати
            for field_id, value in fields.items():
                elem = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                    EC.presence_of_element_located((By.ID, field_id))
                )
                self._human_like_movement(elem)
                elem.clear()
                time.sleep(random.uniform(0.2, 0.5))
                
                # Имитация человеческого ввода
                for char in value:
                    elem.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
                    if random.random() > 0.8:  # Случайные паузы
                        time.sleep(random.uniform(0.2, 0.4))
            
            # Выбор страны из выпадающего списка
            country_select = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "txtPaisNac"))
            )
            self._human_like_movement(country_select)
            
            select = Select(country_select)
            time.sleep(random.uniform(0.3, 0.7))
            select.select_by_visible_text(PERSONAL_DATA["txtPaisNac"])
            time.sleep(random.uniform(0.5, 1.0))

            # Подтверждение данных - ИЗМЕНЕНИЕ ЗДЕСЬ: btnAceptar → btnEnviar
            submit_button = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnEnviar"))
            )
            self._human_like_movement(submit_button)
            submit_button.click()
            time.sleep(random.uniform(1, 3))

            # Ожидание перехода
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.url_contains("/icpco/acValidarEntrada")
            )
            self.current_url = self.driver.current_url
            
            return not self._is_blocked()
            
        except Exception as e:
            logging.error(f"Ошибка заполнения данных: {str(e)}")
            self.save_error_screenshot("personal_data_fill_error")
            return False
    
    def check_slots(self):
        try:
            time.sleep(random.uniform(0.5, 2.0))
            
            if self._is_blocked():
                logging.error("Обнаружена блокировка при проверке слотов")
                return {"status": "blocked"}
                
            # Нажатие кнопки проверки слотов
            submit_button = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnEnviar"))
            )
            self._human_like_movement(submit_button)
            submit_button.click()
            time.sleep(random.uniform(1, 3))

            # Ожидание результатов проверки
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
            self.driver.quit()
            time.sleep(random.uniform(3, 7))  # Увеличенная задержка перед перезапуском
        except Exception as e:
            logging.error(f"Ошибка при закрытии браузера: {str(e)}")
        finally:
            self.driver = self._init_driver()
            self.current_url = ""
            if not DEBUG_MODE:
                self.driver.delete_all_cookies()

    def close(self):
        try:
            self.driver.quit()
        except Exception as e:
            logging.error(f"Ошибка при закрытии браузера: {str(e)}")

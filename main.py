from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webium import BasePage, Find, Finds
from webium.driver import get_driver


wait = WebDriverWait(get_driver(), 10)

class TinkoffPage(BasePage):
    """Объект главной страницы
    payments {WebElement} - ссылка на "Платежи"
    """

    url = "https://www.tinkoff.ru/"
    payments = Find(by=By.LINK_TEXT, value="Платежи")


class PaymentsPage(BasePage):
    '''Объект страницы платежи

    search_input {WebElemnt} - Поле для поиска по названию или ИНН
    communal_payment {WebElemnt} - ссылка на выбор категории "ЖКХ"
    proposal_list {WebElemnt} - список совпадений, при вводе значений в search_input
    '''

    search_input = Find(
        by=By.CSS_SELECTOR, value="input[placeholder*='Название или ИНН получателя']"
        )
    communal_payment = Find(by=By.CSS_SELECTOR, value="div[aria-label='ЖКХ'")
    proposal_list = Finds(by=By.CSS_SELECTOR, value="div[data-qa-file='GridColumn']")

    def proposal_list_text(self):
        """Возвращает текст элементов из списка совпадений

        Returns:
            [List]
        """
        return [provider.text for provider in self.proposal_list]

    def stateless_input(self, name):
        """Поиск по названию/ИНН. После ввода в поискову строку, ожидает появление списка совпадений

        Arguments:
            name {str} -- [Название/ИНН]
        """

        self.search_input.send_keys(name)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-qa-file='GridColumn']")))


class CommunalPage(BasePage):
    """Объект страницы коммунатльные платежи

    current_region {WebElement} - установленный регион
    service_provider {WebElement} - первый поставщик услуг
    list_provider {WebElement} - список всех поставщиков услуг
    """

    current_region = Find(by=By.CSS_SELECTOR, value="span[class*='region']")
    service_provider = Find(by=By.CSS_SELECTOR, value="li:first-child[data-qa-file='UIMenuItemProvider']")
    list_provider = Finds(by=By.CSS_SELECTOR, value="li[data-qa-file='UIMenuItemProvider']")

    def get_region(self, city):
        """Получение WebElementа с указанным регионом

        Arguments:
            city {str} -- Название региона

        Returns:
            [WebElemnt]
        """

        return Find(by=By.XPATH, value=".//*[text()='{}']/..".format(city), context=self)

    def set_region(self, city):
        """Задание указанного региона и ожидание перехода на страницу с поставщиками услуг

        Arguments:
            city {str} -- название региона
        """

        self.current_region.click()
        self.get_region(city).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"li:first-child[data-qa-file='UIMenuItemProvider']")))

    def list_provider_text(self):
        """Получение списка название поставщиков услуг

        Returns:
            List -- список названий
        """

        return [provider.text for provider in self.list_provider]


class ZhkuMoskvaPage(BasePage):
    """Объект страницы ЖКУ-Москва

    payment_url {WebElement} - url текущей страницы
    payment {WebElement} - вкладка оплата
    payer_code {WebElement} - поле "Код плательщика"
    period {WebElement} - поле "Период оплаты"
    voluntary_insurance {WebElement} - поле "Сумма добровольного страхования"
    summa {WebElement} - поле "Сумма платежа"
    button {WebElement} - кнопка отправки формы
    error_messages {WebElement} - список сообщений о не валидности данных
    without_commission {WebElement} - кнопка без комиссии
    with_commission {WebElement} - кнопка с комиссией
    card_number {WebElement} - номер карты
    """

    payment_url = "https://www.tinkoff.ru/zhku-moskva/oplata/?tab=pay"
    payment = Find(by=By.CSS_SELECTOR, value="a[href='/zhku-moskva/oplata/']")
    payer_code = Find(by=By.ID, value="payerCode")
    period = Find(by=By.ID, value="period")
    voluntary_insurance = Find(
        by=By.CSS_SELECTOR,
        value="div[data-qa-file='StatelessInput'] input[data-qa-file='StatelessInput']"
    )
    summa = Find(
        by=By.CSS_SELECTOR,
        value="div[data-qa-file='FormFieldSet'] input[data-qa-file='StatelessInput']"
        )
    without_commission = Find(by=By.XPATH, value="//*[.='без комиссии']")
    with_commission = Find(by=By.XPATH, value="//*[.='без регистрации']")
    card_number = Find(by=By.CSS_SELECTOR, value="input[name='cardNumber']")
    button = Find(by=By.CSS_SELECTOR, value="button[data-qa-file='UIButton']")
    error_messages = Finds(by=By.CSS_SELECTOR, value="div[data-qa-file='UIFormRowError']")

    def error_messages_text(self):
        """Получени текста ошибок
        
        Returns:
            List -- список текстов ошибок
        """

        return [message.text for message in self.error_messages]

    def submit_form(self, payer_code="", period="", voluntary_insurance="", summa="", registration=False, card=""):
        """Отправка формы оплаты

        Keyword Arguments:
            payer_code {str} -- код плательщика (default: {""})
            period {str} -- период оплаты (default: {""})
            voluntary_insurance {str} -- сумма добровольного страхования (default: {""})
            summa {str} -- сумма платежа (default: {""})
        """

        self.payer_code.send_keys(payer_code)
        self.period.send_keys(period)
        self.voluntary_insurance.send_keys(voluntary_insurance)
        self.summa.send_keys(summa)
        self.button.click()
        if summa != "":
            if registration:
                self.without_commission.click()
            else:
                self.with_commission.click()
                #self.card_number.send_keys(card) TODO: Не отправляется значение "is not reachable by keyboard" если делать ожидание вылетает по timeout
                self.button.click()


    def click_payment(self):
        """Переход на вкладку "Оплата" с ожиданием появления формы
        """

        self.payment.click()
        wait.until(EC.element_to_be_clickable((By.ID,"period")))

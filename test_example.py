from webium.driver import get_driver

from main import CommunalPage, PaymentsPage, TinkoffPage, ZhkuMoskvaPage


def test_payment_form():
    tinkoff_page = TinkoffPage()
    tinkoff_page.open()
    tinkoff_page.payments.click()

    payment_page = PaymentsPage()
    payment_page.communal_payment.click()

    communal_page = CommunalPage()
    if communal_page.current_region.text != "Москве":
        communal_page.set_region("г. Москва")
    communal_page.service_provider.click()
    provider_name = communal_page.service_provider.text

    zhku_moskva = ZhkuMoskvaPage()
    zhku_moskva.click_payment()
    zhku_moskva.submit_form(payer_code="111")
    assert ["Поле неправильно заполнено",
            "Поле обязательное",
            "Поле обязательное"] == zhku_moskva.error_messages_text()

    tinkoff_page.payments.click()
    payment_page.stateless_input(provider_name)
    assert "ЖКУ-Москва" in payment_page.proposal_list_text()[0]

    payment_page.proposal_list[0].click()
    zhku_moskva.click_payment()
    assert get_driver().current_url == zhku_moskva.payment_url

    tinkoff_page.payments.click()
    payment_page.communal_payment.click()
    communal_page.set_region("г. Санкт-Петербург")
    assert provider_name not in communal_page.list_provider_text()


def teardown_module(module):
    get_driver().quit()

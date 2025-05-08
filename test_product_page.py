import pytest
from .pages.main_page import MainPage
from .pages.product_page import ProductPage
from selenium.webdriver.common.by import By

links = [
    f"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer{n}" 
    if n != 7 else pytest.param(
        f"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer{n}", 
        marks=pytest.mark.xfail(reason="Known bug in promo offer7"))
    for n in range(10)
]

@pytest.mark.parametrize('link', links)
def test_guest_can_add_product_to_basket(browser, link):
    link = 'http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/'
    page = ProductPage(browser, link)
    page.open()
    page.should_be_add_to_busket_button()
    page.add_product_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_correct_product_added()
    page.should_be_correct_basket_price()
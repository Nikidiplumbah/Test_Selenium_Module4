import pytest
from .pages.main_page import MainPage
from .pages.base_page import BasePage
from .pages.login_page import LoginPage
from .pages.product_page import ProductPage
from selenium.webdriver.common.by import By
from .pages.basket_page import BasketPage
import time

links = [
    f"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer{n}" 
    if n != 7 else pytest.param(
        f"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer{n}", 
        marks=pytest.mark.xfail(reason="Known bug in promo offer7"))
    for n in range(10)
]

@pytest.mark.login
class TestUserAddToBasketFromProductPage():
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        login_link = "http://selenium1py.pythonanywhere.com/accounts/login/"
        login_page = LoginPage(browser, login_link)
        login_page.open()
        email = str(time.time()) + "@fakemail.org"
        password = "Password12345!"
        login_page.register_new_user(email, password)
        login_page.should_be_authorized_user()
        
    def test_user_cant_see_success_message(self, browser):
        link = "http://selenium1py.pythonanywhere.com/catalogue/the-city-and-the-stars_95/"
        page = ProductPage(browser, link)
        page.open()
        assert page.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Success message is displayed for new user without adding product"
    
    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser):
        link = "http://selenium1py.pythonanywhere.com/catalogue/the-city-and-the-stars_95/"
        page = ProductPage(browser, link)
        page.open()
        page.add_product_to_basket()
        page.solve_quiz_and_get_code()
        page.should_be_correct_product_added()
        page.should_be_correct_basket_price()

@pytest.mark.need_review    
def test_guest_can_add_product_to_basket(browser):
    link = 'http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/'
    page = ProductPage(browser, link)
    page.open()
    page.should_be_add_to_busket_button()
    page.add_product_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_correct_product_added()
    page.should_be_correct_basket_price()
        
def test_guest_cant_see_success_message(browser):
    link ='http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/'
    page = ProductPage(browser, link)
    page.open()
    page.should_not_be_success_message()
    

def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    link ='http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/'
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket()
    page.should_not_be_success_message()  


@pytest.mark.xfail(reason="Success message doesn't disappear after adding to basket")
def test_message_disappeared_after_adding_product_to_basket(browser):
    link ='http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/'
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket()
    page.success_message_should_disappear()
    
def test_guest_should_see_login_link_on_product_page(browser):
    link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
    page = ProductPage(browser, link)
    page.open()
    page.should_be_login_link()

@pytest.mark.need_review    
def test_guest_can_go_to_login_page_from_product_page(browser):
    link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
    page = ProductPage(browser, link)
    page.open()
    page.go_to_login_page()

@pytest.mark.need_review    
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
    page = ProductPage(browser, link)
    page.open()
    page.go_to_basket_page()
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_empty_basket()
    basket_page.should_see_empty_basket_message()
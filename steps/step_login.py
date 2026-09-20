import time
from pytest_bdd import given, when, then
from pages.LoginPage import LoginPage
from pages.HomePage import HomePage
from config.config import app_url, test_username, test_password


@given("user is on the login page")
def open_login_page(browser):
    browser.get(app_url)


@when("user enters credentials")
def enter_credentials(browser):
    login_page = LoginPage(browser)
    login_page.enter_user_id(test_username)
    login_page.enter_password(test_password)


@when("user clicks login button")
def click_login(browser):
    login_page = LoginPage(browser)
    login_page.click_login_button()
    time.sleep(2)


@then("user should be logged in successfully")
def verify_login_success(browser):
    home_page = HomePage(browser)
    assert home_page.is_dashboard_loaded(), "Dashboard did not load after login"


@then("user should verify the home page URL")
def verify_home_page_url(browser):
    home_page = HomePage(browser)
    current_url = home_page.get_current_url()
    assert "A25R1" in current_url, f"Expected home page URL to contain 'A25R1', but got: {current_url}"


@when("user clicks logout button")
def click_logout(browser):
    home_page = HomePage(browser)
    home_page.click_logout_button()
    time.sleep(2)


@then("user should be logged out")
def verify_logout(browser):
    login_page = LoginPage(browser)
    assert login_page.element_exists(login_page.user_id_field), "Not on login page after logout"



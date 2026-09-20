from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class LoginPage(BasePage):
    """OnniProject AM25R1 Login Page Object"""
    user_id_field = (By.ID, "txtUser")
    password_field = (By.ID, "txtPass")
    login_button = (By.ID, "btnLogin")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def enter_user_id(self, user_id: str):
        """Enter user id in the user id field"""
        self.send_keys(self.user_id_field, user_id)
    
    def enter_password(self, password: str):
        """Enter password in the password field"""
        self.send_keys(self.password_field, password)
    
    def click_login_button(self):
        """Click on Login button"""
        self.click(self.login_button)
    
    def login(self, user_id: str, password: str):
        """Complete login flow"""
        self.enter_user_id(user_id)
        self.enter_password(password)
        self.click_login_button()

from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class HomePage(BasePage):
    """OnniProject AM25R1 Home Page Object"""
    logout_button = (By.XPATH, "//a[contains(@href, 'Logout') or contains(@href, 'logout') or contains(text(), 'Logout') or contains(text(), 'logout')]")
    main_content = (By.XPATH, "//div[@id='content' or contains(@class, 'main')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_dashboard_loaded(self) -> bool:
        """Check if dashboard has loaded successfully"""
        try:
            current_url = self.get_current_url()
            if "Main" in current_url or "A25R1" in current_url:
                return True
            return False
        except:
            return False
    
    def get_current_url(self) -> str:
        """Get the current URL"""
        return self.driver.current_url
    
    def click_logout_button(self):
        """Click on logout button"""
        try:
            self.click(self.logout_button)
        except Exception as e:
            print(f"⚠️ Could not find logout button with standard XPath, trying alternative...")
            # If standard logout button not found, try to navigate to login page
            self.navigate_to_url(self.driver.current_url.replace("Main", "Login"))



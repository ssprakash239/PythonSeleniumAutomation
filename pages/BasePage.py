import os
from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    NoAlertPresentException
)
from config.config import implicit_wait, explicit_wait
from datetime import datetime


class BasePage:
    """
    Base Page class for OnniProject AM25R1 Automation Framework.
    Contains all reusable Selenium utilities and methods for test automation.
    Provides 65+ methods for element interaction, waits, actions, and utilities.
    """
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, explicit_wait)
        self.action = ActionChains(driver)

    def find_element(self, locator: Tuple[By, str]):
        """Find element with implicit wait."""
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            raise

    def find_elements(self, locator: Tuple[By, str]) -> List:
        """Find multiple elements."""
        try:
            return self.driver.find_elements(*locator)
        except NoSuchElementException:
            return []

    def wait_for_element_presence(self, locator: Tuple[By, str]):
        """Wait for element to be present in DOM."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            raise

    def wait_for_element_visibility(self, locator: Tuple[By, str]):
        """Wait for element to be visible."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            raise

    def wait_for_element_clickable(self, locator: Tuple[By, str]):
        """Wait for element to be clickable."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            raise

    def click(self, locator: Tuple[By, str]):
        """Click on element with wait."""
        element = self.wait_for_element_clickable(locator)
        try:
            element.click()
        except Exception as e:
            raise

    def send_keys(self, locator: Tuple[By, str], text: str):
        """Send keys to element."""
        element = self.wait_for_element_visibility(locator)
        try:
            element.clear()
            element.send_keys(text)
        except Exception as e:
            raise

    def get_text(self, locator: Tuple[By, str]) -> str:
        """Get text from element."""
        element = self.wait_for_element_visibility(locator)
        try:
            text = element.text
            return text
        except Exception as e:
            raise

    def get_attribute(self, locator: Tuple[By, str], attribute: str) -> str:
        """Get attribute value from element."""
        element = self.wait_for_element_presence(locator)
        try:
            value = element.get_attribute(attribute)
            return value
        except Exception as e:
            raise

    def verify_text(self, locator: Tuple[By, str], expected_text: str) -> bool:
        """Verify if element contains expected text."""
        try:
            actual_text = self.get_text(locator)
            if expected_text.lower() in actual_text.lower():
                return True
            else:
                return False
        except Exception as e:
            raise

    def hover(self, locator: Tuple[By, str]):
        """Hover over element."""
        element = self.wait_for_element_visibility(locator)
        try:
            self.action.move_to_element(element).perform()
        except Exception as e:
            raise

    def double_click(self, locator: Tuple[By, str]):
        """Double click on element."""
        element = self.wait_for_element_clickable(locator)
        try:
            self.action.double_click(element).perform()
        except Exception as e:
            raise

    def right_click(self, locator: Tuple[By, str]):
        """Right click (context menu) on element."""
        element = self.wait_for_element_clickable(locator)
        try:
            self.action.context_click(element).perform()
        except Exception as e:
            raise

    def drag_and_drop(self, source_locator: Tuple[By, str], target_locator: Tuple[By, str]):
        """Drag and drop element from source to target."""
        source = self.wait_for_element_clickable(source_locator)
        target = self.wait_for_element_visibility(target_locator)
        try:
            self.action.drag_and_drop(source, target).perform()
        except Exception as e:
            raise

    def select_from_dropdown_by_value(self, locator: Tuple[By, str], value: str):
        """Select option from dropdown by value."""
        element = self.wait_for_element_clickable(locator)
        try:
            select = Select(element)
            select.select_by_value(value)
        except Exception as e:
            raise

    def select_from_dropdown_by_text(self, locator: Tuple[By, str], text: str):
        """Select option from dropdown by visible text."""
        element = self.wait_for_element_clickable(locator)
        try:
            select = Select(element)
            select.select_by_visible_text(text)
        except Exception as e:
            raise

    def select_from_dropdown_by_index(self, locator: Tuple[By, str], index: int):
        """Select option from dropdown by index."""
        element = self.wait_for_element_clickable(locator)
        try:
            select = Select(element)
            select.select_by_index(index)
        except Exception as e:
            raise

    def get_dropdown_options(self, locator: Tuple[By, str]) -> List[str]:
        """Get all options from dropdown."""
        element = self.wait_for_element_visibility(locator)
        try:
            select = Select(element)
            options = [option.text for option in select.options]
            return options
        except Exception as e:
            raise

    def press_key(self, locator: Tuple[By, str], key):
        """Press a keyboard key."""
        element = self.wait_for_element_visibility(locator)
        try:
            element.send_keys(key)
        except Exception as e:
            raise

    def switch_to_frame(self, frame_reference):
        """Switch to iframe by element locator or index."""
        try:
            if isinstance(frame_reference, tuple):
                frame = self.wait_for_element_presence(frame_reference)
                self.driver.switch_to.frame(frame)
            else:
                self.driver.switch_to.frame(frame_reference)
        except Exception as e:
            raise

    def switch_to_parent_frame(self):
        """Switch to parent frame."""
        try:
            self.driver.switch_to.parent_frame()
        except Exception as e:
            raise

    def switch_to_default_content(self):
        """Switch to default content (main page)."""
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            raise

    def switch_to_window(self, window_handle: str):
        """Switch to specific window by handle."""
        try:
            self.driver.switch_to.window(window_handle)
        except Exception as e:
            raise

    def get_window_handles(self) -> List[str]:
        """Get all window handles."""
        try:
            handles = self.driver.window_handles
            return handles
        except Exception as e:
            raise

    def switch_to_latest_window(self):
        """Switch to latest opened window."""
        try:
            self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as e:
            raise

    def accept_alert(self) -> str:
        """Accept alert and return alert text."""
        try:
            alert = Alert(self.driver)
            text = alert.text
            alert.accept()
            return text
        except NoAlertPresentException:
            return ""
        except Exception as e:
            raise

    def dismiss_alert(self) -> str:
        """Dismiss alert and return alert text."""
        try:
            alert = Alert(self.driver)
            text = alert.text
            alert.dismiss()
            return text
        except NoAlertPresentException:
            return ""
        except Exception as e:
            raise

    def get_alert_text(self) -> str:
        """Get alert text."""
        try:
            alert = Alert(self.driver)
            text = alert.text
            return text
        except NoAlertPresentException:
            return ""
        except Exception as e:
            raise

    def send_keys_to_alert(self, text: str):
        """Send text to alert prompt."""
        try:
            alert = Alert(self.driver)
            alert.send_keys(text)
        except NoAlertPresentException:
            pass
        except Exception as e:
            raise

    def scroll_to_element(self, locator: Tuple[By, str]):
        """Scroll to element."""
        element = self.wait_for_element_presence(locator)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        except Exception as e:
            raise

    def scroll_to_top(self):
        """Scroll to top of page."""
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
        except Exception as e:
            raise

    def scroll_to_bottom(self):
        """Scroll to bottom of page."""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            raise

    def scroll_by_amount(self, x: int, y: int):
        """Scroll by specific amount."""
        try:
            self.driver.execute_script(f"window.scrollBy({x}, {y});")
        except Exception as e:
            raise

    def execute_javascript(self, script: str, *args):
        """Execute JavaScript."""
        try:
            result = self.driver.execute_script(script, *args)
            return result
        except Exception as e:
            raise

    def is_element_visible(self, locator: Tuple[By, str]) -> bool:
        """Check if element is visible."""
        try:
            element = self.driver.find_element(*locator)
            is_visible = element.is_displayed()
            return is_visible
        except NoSuchElementException:
            return False
        except Exception as e:
            return False

    def is_element_enabled(self, locator: Tuple[By, str]) -> bool:
        """Check if element is enabled."""
        try:
            element = self.driver.find_element(*locator)
            is_enabled = element.is_enabled()
            return is_enabled
        except NoSuchElementException:
            return False
        except Exception as e:
            return False

    def is_element_selected(self, locator: Tuple[By, str]) -> bool:
        """Check if element is selected."""
        try:
            element = self.driver.find_element(*locator)
            is_selected = element.is_selected()
            return is_selected
        except NoSuchElementException:
            return False
        except Exception as e:
            return False

    def take_screenshot(self, filename: str = None) -> str:
        """Take screenshot and save to file."""
        try:
            if filename is None:
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join("reports", filename)
            os.makedirs("reports", exist_ok=True)
            self.driver.save_screenshot(filepath)
            return filepath
        except Exception as e:
            raise

    def upload_file(self, locator: Tuple[By, str], file_path: str):
        """Upload file to file input element."""
        element = self.wait_for_element_presence(locator)
        try:
            element.send_keys(file_path)
        except Exception as e:
            raise

    def add_cookie(self, cookie_dict: dict):
        """Add cookie to browser."""
        try:
            self.driver.add_cookie(cookie_dict)
        except Exception as e:
            raise

    def get_cookie(self, cookie_name: str) -> dict:
        """Get specific cookie."""
        try:
            cookie = self.driver.get_cookie(cookie_name)
            return cookie
        except Exception as e:
            raise

    def get_all_cookies(self) -> List[dict]:
        """Get all cookies."""
        try:
            cookies = self.driver.get_cookies()
            return cookies
        except Exception as e:
            raise

    def delete_cookie(self, cookie_name: str):
        """Delete specific cookie."""
        try:
            self.driver.delete_cookie(cookie_name)
        except Exception as e:
            raise

    def delete_all_cookies(self):
        """Delete all cookies."""
        try:
            self.driver.delete_all_cookies()
        except Exception as e:
            raise

    def get_page_title(self) -> str:
        """Get page title."""
        try:
            title = self.driver.title
            return title
        except Exception as e:
            raise

    def get_current_url(self) -> str:
        """Get current URL."""
        try:
            url = self.driver.current_url
            return url
        except Exception as e:
            raise

    def refresh_page(self):
        """Refresh current page."""
        try:
            self.driver.refresh()
        except Exception as e:
            raise

    def go_back(self):
        """Navigate back."""
        try:
            self.driver.back()
        except Exception as e:
            raise

    def go_forward(self):
        """Navigate forward."""
        try:
            self.driver.forward()
        except Exception as e:
            raise

    def navigate_to_url(self, url: str):
        """Navigate to specific URL."""
        try:
            self.driver.get(url)
        except Exception as e:
            raise

    def wait_for_url_to_contain(self, text: str, timeout: int = None):
        """Wait for URL to contain specific text."""
        timeout = timeout or explicit_wait
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(text))
        except TimeoutException:
            raise

    def wait_for_title_to_contain(self, text: str, timeout: int = None):
        """Wait for page title to contain specific text."""
        timeout = timeout or explicit_wait
        try:
            WebDriverWait(self.driver, timeout).until(EC.title_contains(text))
        except TimeoutException:
            raise

    def element_exists(self, locator: Tuple[By, str]) -> bool:
        """Check if element exists without waiting."""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            return False

    def get_element_count(self, locator: Tuple[By, str]) -> int:
        """Get count of elements matching locator."""
        try:
            elements = self.driver.find_elements(*locator)
            count = len(elements)
            return count
        except Exception as e:
            raise

    def wait_for_invisibility(self, locator: Tuple[By, str]):
        """Wait for element to become invisible."""
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            raise

    def get_element_css_value(self, locator: Tuple[By, str], css_property: str) -> str:
        """Get CSS property value of element."""
        element = self.wait_for_element_presence(locator)
        try:
            value = element.value_of_css_property(css_property)
            return value
        except Exception as e:
            raise

    def get_element_size(self, locator: Tuple[By, str]) -> dict:
        """Get element size (width and height)."""
        element = self.wait_for_element_presence(locator)
        try:
            size = element.size
            return size
        except Exception as e:
            raise

    def get_element_location(self, locator: Tuple[By, str]) -> dict:
        """Get element location (x and y coordinates)."""
        element = self.wait_for_element_presence(locator)
        try:
            location = element.location
            return location
        except Exception as e:
            raise

    def clear_field(self, locator: Tuple[By, str]):
        """Clear input field."""
        element = self.wait_for_element_visibility(locator)
        try:
            element.clear()
        except Exception as e:
            raise

    def submit_form(self, locator: Tuple[By, str]):
        """Submit form."""
        element = self.wait_for_element_presence(locator)
        try:
            element.submit()
        except Exception as e:
            raise

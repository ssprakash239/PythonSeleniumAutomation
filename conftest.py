import pytest
from selenium import webdriver
from config.config import browser_name, implicit_wait

# All pytest/pytest-bdd hooks (console step logging, Extent Report data, failure screenshots) live in utils/hooks.py
pytest_plugins = ["utils.hooks"]

# Set which tagged scenarios to run when this file is executed directly (Run/Debug 'conftest').
# Examples: "smoke", "regression", "sanity", "smoke or sanity", "regression and not sanity", or "" for all.
MARKER_TO_RUN = "smoke"


@pytest.fixture(scope="function")
def browser():
    driver = None
    browser_type = browser_name.lower().strip()
    
    try:
        if browser_type == "chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            # Selenium 4.6+ has built-in Selenium Manager
            driver = webdriver.Chrome(options=chrome_options)
        else:
            raise ValueError(f"Unsupported browser: {browser_type}")
        
        driver.implicitly_wait(implicit_wait)
        yield driver
    
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    # Lets PyCharm's "Run 'conftest'" / "Debug 'conftest'" context menu execute the suite directly:
    # Run = normal execution, Debug = same run with breakpoints active across the project.
    import sys
    args = sys.argv[1:]
    if MARKER_TO_RUN:
        args = args + ["-m", MARKER_TO_RUN]
    sys.exit(pytest.main(args))




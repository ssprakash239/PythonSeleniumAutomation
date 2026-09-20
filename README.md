# OnniProject_AM25R1_Automation - Automation Testing Framework

A comprehensive BDD (Behavior Driven Development) automation testing framework built with Python, Selenium, and Pytest for testing the OnniProject AM25R1 application.

## Project Overview

This framework is designed to test OnniProject AM25R1 (https://eadev.onni.com/A25R1/Frames/Login.aspx) using:
- **Python 3.8+**: Programming language
- **Selenium 4.14.0**: Web automation library
- **Pytest 7.4.3**: Test framework
- **pytest-bdd**: BDD plugin for pytest
- **Extent Report**: Custom self-contained HTML execution report (generated per run)
- **WebDriver Manager**: Automatic driver management

## Framework Structure

```
OnniProject_AM25R1_Automation/
├── features/                  # BDD feature files (Gherkin syntax)
│   └── login.feature         # Login and logout scenarios
├── steps/                     # Step definitions for BDD scenarios
│   └── step_login.py         # Step implementations
├── pages/                     # Page Object Model classes
│   ├── BasePage.py           # Base class with all Selenium utilities
│   ├── LoginPage.py          # Login page object
│   └── HomePage.py           # Home page object
├── config/                    # Configuration management
│   ├── config.py             # Config reader
│   └── data.properties       # Configuration parameters
├── utils/                     # Shared utilities
│   └── extent_report.py      # Extent-style HTML report generator
├── reports/                   # Test reports and results
│   └── extent-reports/       # Generated Extent HTML reports (one per run)
├── conftest.py               # Pytest fixtures and configuration
├── pytest.ini                # Pytest settings
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Step 1: Clone/Extract Project
```bash
cd WelcomeScreen
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Application Settings
`config/data.properties` is committed as a **blank template** (no URL/credentials in source control).
Before running tests, fill in your own values locally — **do not commit real values back**:
- **APP_URL**: Application URL to test (e.g. `https://eadev.onni.com/A25R1/Frames/Login.aspx?ReturnUrl=%2fA25R1%2f`)
- **BROWSER**: Browser type - chrome (default: chrome)
- **IMPLICIT_WAIT**: Implicit wait in seconds (default: 10)
- **EXPLICIT_WAIT**: Explicit wait in seconds (default: 20)
- **TEST_USERNAME**: Test user for the application
- **TEST_PASSWORD**: Test password for the application

## Running Tests

### Run All Tests
```bash
pytest --verbose
```

### Run Specific Feature File
```bash
pytest features/login.feature -v
```

### Run Tests in Parallel
```bash
pytest -n 4 --verbose
```

### Run with Different Browser
Edit `config/data.properties` and change `BROWSER=edge` or `BROWSER=firefox`, then run:
```bash
pytest --verbose
```

## Test Scenarios

### Login and Verify Home Page URL Test
- Navigate to OnniProject AM25R1 login page
- Enter valid username (APIAccess)
- Enter valid password (@*M*s95#gY7&e*B3n)
- Click Login button
- Verify home page URL contains "A25R1"
- Click logout button
- Verify user is logged out

## BasePage Utilities

The `BasePage.py` class provides comprehensive Selenium utilities:

### Basic Element Interactions
- `click(locator)` - Click on element
- `send_keys(locator, text)` - Enter text in field
- `get_text(locator)` - Get element text
- `get_attribute(locator, attribute)` - Get element attribute
- `verify_text(locator, expected_text)` - Verify text match

### Waits
- `wait_for_element_presence(locator)` - Wait for element in DOM
- `wait_for_element_visibility(locator)` - Wait for element visibility
- `wait_for_element_clickable(locator)` - Wait for element clickability
- `wait_for_invisibility(locator)` - Wait for element invisibility
- `wait_for_url_to_contain(text)` - Wait for URL change
- `wait_for_title_to_contain(text)` - Wait for title change

### Actions (Advanced User Interactions)
- `hover(locator)` - Hover over element
- `double_click(locator)` - Double click element
- `right_click(locator)` - Right click (context menu)
- `drag_and_drop(source, target)` - Drag and drop

### Dropdowns
- `select_from_dropdown_by_value(locator, value)` - Select by value
- `select_from_dropdown_by_text(locator, text)` - Select by visible text
- `select_from_dropdown_by_index(locator, index)` - Select by index
- `get_dropdown_options(locator)` - Get all dropdown options

### Window & Frame Management
- `switch_to_window(handle)` - Switch to window
- `switch_to_latest_window()` - Switch to latest window
- `get_window_handles()` - Get all window handles
- `switch_to_frame(frame_ref)` - Switch to iframe
- `switch_to_parent_frame()` - Switch to parent frame
- `switch_to_default_content()` - Switch to main content

### JavaScript & Scroll
- `execute_javascript(script, *args)` - Execute JavaScript
- `scroll_to_element(locator)` - Scroll to element
- `scroll_to_top()` - Scroll to page top
- `scroll_to_bottom()` - Scroll to page bottom
- `scroll_by_amount(x, y)` - Scroll by pixel amount

### Alerts
- `accept_alert()` - Accept alert
- `dismiss_alert()` - Dismiss alert
- `get_alert_text()` - Get alert text
- `send_keys_to_alert(text)` - Send text to alert

### Element State Checks
- `is_element_visible(locator)` - Check visibility
- `is_element_enabled(locator)` - Check enabled state
- `is_element_selected(locator)` - Check selected state
- `element_exists(locator)` - Check element existence
- `get_element_count(locator)` - Get element count

### Navigation & Page Management
- `navigate_to_url(url)` - Navigate to URL
- `refresh_page()` - Refresh page
- `go_back()` - Navigate back
- `go_forward()` - Navigate forward
- `get_page_title()` - Get page title
- `get_current_url()` - Get current URL

### Other Utilities
- `take_screenshot(filename)` - Take screenshot
- `upload_file(locator, file_path)` - Upload file
- `add_cookie(cookie_dict)` - Add cookie
- `get_cookie(name)` - Get cookie
- `delete_cookie(name)` - Delete cookie
- `delete_all_cookies()` - Delete all cookies
- `get_element_size(locator)` - Get element size
- `get_element_location(locator)` - Get element location
- `get_element_css_value(locator, property)` - Get CSS value
- `clear_field(locator)` - Clear input field
- `submit_form(locator)` - Submit form

## Logging

The framework includes comprehensive logging:
- **Console Logs**: INFO level messages shown in console during execution
- **File Logs**: DEBUG level detailed logs saved in `logs/` directory with timestamp
- **Format**: `YYYY-MM-DD HH:MM:SS - Logger Name - Level - Message`

All logs are automatically created and stored per test run.

## Test Reports

### Extent Report
An HTML Extent-style report is generated automatically at the end of every test run — no extra flags needed.

- Location: `reports/extent-reports/`
- File name: `<BrowserName>_ExtentReport_<YYYYMMDD>_<HHMM>.html` (e.g. `Chrome_ExtentReport_20260920_1715.html`)
- Every run creates a new, uniquely timestamped file — previous reports are never overwritten.
- Contents: overall execution summary (total/pass/fail/skip counts with a donut chart), browser used, execution start/end time and total duration, plus a per-test results table with status and duration.

### Screenshots
Test screenshots are automatically saved in `reports/` folder when:
- Test fails
- Manually called in step definition using `take_screenshot(filename)`

## Configuration Details

### data.properties File
- **APP_URL**: Application URL to test
- **BROWSER**: Browser to use (chrome/edge/firefox)
- **IMPLICIT_WAIT**: Implicit wait timeout (seconds)
- **EXPLICIT_WAIT**: Explicit wait timeout (seconds)
- **FLUENT_WAIT_POLLING_INTERVAL**: Fluent wait polling interval (milliseconds)
- **TEST_USERNAME**: Username for login tests
- **TEST_PASSWORD**: Password for login tests
- **LOG_FILE_PATH**: Directory for log files

## Page Object Model (POM)

### LoginPage
- **username_field**: Username input field
- **password_field**: Password input field
- **login_button**: Login submit button
- **error_message**: Error message display element
- **Methods**:
  - `enter_username(username)` - Enter username
  - `enter_password(password)` - Enter password
  - `click_login_button()` - Click login
  - `login(username, password)` - Complete login flow
  - `is_error_displayed()` - Check for errors
  - `get_error_message()` - Get error message text

### HomePage
- **dashboard_heading**: Dashboard heading
- **user_profile_icon**: User profile icon
- **logout_button**: Logout button
- **Methods**:
  - `is_dashboard_loaded()` - Verify dashboard
  - `get_page_title_text()` - Get page title
  - `verify_home_page_title(expected_title)` - Verify title
  - `click_user_profile()` - Click profile
  - `logout()` - Perform logout

## Future Enhancements

- [ ] Add more test scenarios for additional modules (HR, PIM, Admin, etc.)
- [ ] Implement parameterized testing for multiple data sets
- [ ] Add performance testing utilities
- [ ] Implement API testing alongside UI testing
- [ ] Add visual regression testing
- [ ] Implement continuous integration (CI/CD) pipeline
- [ ] Add data-driven testing with external data sources
- [ ] Create custom HTML reports

## Troubleshooting

### Issue: WebDriver Not Found
**Solution**: Ensure `webdriver-manager` is installed. It automatically downloads appropriate drivers.

### Issue: Element Not Found
**Solution**: 
- Verify element locators are correct
- Check if element is visible and in viewport
- Use explicit waits instead of implicit waits
- Check if element is inside iframe (switch to frame first)

### Issue: Tests Timeout
**Solution**: Increase `EXPLICIT_WAIT` value in `data.properties`

## Best Practices

1. **Use Page Object Model**: Keep element locators and methods in page classes
2. **Use Explicit Waits**: Prefer explicit waits over implicit waits
3. **DRY Principle**: Reuse BasePage utilities instead of duplicating code
4. **Meaningful Assertions**: Use clear assertion messages
5. **Clean Logs**: Review logs to understand test execution flow
6. **Screenshot on Failure**: Enable screenshot capture for debugging
7. **Parameterize Tests**: Use multiple test data sets for comprehensive testing
8. **Maintain Tests**: Update locators/tests when UI changes
9. **Version Control**: Commit framework code to Git
10. **Documentation**: Keep README and code comments updated

## Support & Contribution

For issues, feature requests, or contributions, please refer to project documentation and coding standards.

---

**Framework Version**: 1.0  
**Last Updated**: September 2026  
**Project Name**: OnniProject_AM25R1_Automation  
**Maintained By**: QA Automation Team

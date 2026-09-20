import configparser
import os

config = configparser.RawConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'data.properties')
config.read(config_path)

app_url = config.get('APPLICATION', 'APP_URL')
browser_name = config.get('BROWSER', 'BROWSER')
implicit_wait = config.getint('WAITS', 'IMPLICIT_WAIT')
explicit_wait = config.getint('WAITS', 'EXPLICIT_WAIT')
fluent_wait_polling_interval = config.getint('WAITS', 'FLUENT_WAIT_POLLING_INTERVAL')

test_username = config.get('CREDENTIALS', 'TEST_USERNAME')
test_password = config.get('CREDENTIALS', 'TEST_PASSWORD')

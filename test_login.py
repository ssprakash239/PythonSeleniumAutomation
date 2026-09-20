import pytest
from pytest_bdd import scenarios
from steps.step_login import *  # noqa

scenarios('login.feature')


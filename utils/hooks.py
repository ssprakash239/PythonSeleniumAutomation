"""Centralized pytest/pytest-bdd hooks: console step logging, Extent Report data collection, and failure screenshots."""
import logging
import time
from datetime import datetime

import pytest
from config.config import browser_name
from utils.extent_report import generate_extent_report

logger = logging.getLogger("bdd_steps")

_test_results = []
_test_steps = {}       # nodeid -> list of per-step result dicts, for the Extent Report
_step_start_time = {}  # nodeid -> perf_counter() when the current step started
_session_start_time = None


def pytest_configure(config):
    global _session_start_time
    _session_start_time = datetime.now()


def pytest_bdd_before_scenario(request, feature, scenario):
    logger.info("=" * 60)
    logger.info(f"SCENARIO STARTED: {scenario.name}")
    logger.info("=" * 60)


def pytest_bdd_after_scenario(request, feature, scenario):
    logger.info(f"SCENARIO FINISHED: {scenario.name}")
    logger.info("=" * 60)


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    _step_start_time[request.node.nodeid] = time.perf_counter()
    logger.info(f"STEP STARTED : {step.keyword} {step.name}")


def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    nodeid = request.node.nodeid
    duration = time.perf_counter() - _step_start_time.pop(nodeid, time.perf_counter())
    _test_steps.setdefault(nodeid, []).append({
        "keyword": step.keyword,
        "name": step.name,
        "status": "Passed",
        "duration": duration,
        "message": "",
    })
    logger.info(f"STEP PASSED  : {step.keyword} {step.name}")


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    nodeid = request.node.nodeid
    duration = time.perf_counter() - _step_start_time.pop(nodeid, time.perf_counter())
    _test_steps.setdefault(nodeid, []).append({
        "keyword": step.keyword,
        "name": step.name,
        "status": "Failed",
        "duration": duration,
        "message": str(exception),
        "screenshot": _capture_screenshot(request),
    })
    logger.error(f"STEP FAILED  : {step.keyword} {step.name} -> {exception}")


def _capture_screenshot(request):
    """Grab a base64 screenshot of the current browser state for embedding in the Extent Report."""
    try:
        driver = request.getfixturevalue("browser")
        return driver.get_screenshot_as_base64()
    except Exception as exc:
        logger.warning(f"Could not capture failure screenshot: {exc}")
        return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Record each test's outcome (with its BDD steps) so the Extent Report can summarize results."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "setup" and rep.outcome in ("skipped", "failed"):
        _test_results.append({
            "name": item.name,
            "status": "Skipped" if rep.outcome == "skipped" else "Failed",
            "duration": rep.duration,
            "message": str(rep.longrepr) if rep.longrepr else "",
            "steps": _test_steps.pop(item.nodeid, []),
        })
    elif rep.when == "call":
        _test_results.append({
            "name": item.name,
            "status": "Passed" if rep.outcome == "passed" else "Failed",
            "duration": rep.duration,
            "message": str(rep.longrepr) if rep.failed else "",
            "steps": _test_steps.pop(item.nodeid, []),
        })


def pytest_sessionfinish(session, exitstatus):
    session_end_time = datetime.now()
    report_path = generate_extent_report(
        test_results=_test_results,
        browser_name=browser_name,
        start_time=_session_start_time,
        end_time=session_end_time,
    )
    print(f"\nExtent Report generated: {report_path}")

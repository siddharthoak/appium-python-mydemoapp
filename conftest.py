import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

load_dotenv()

APP_PACKAGE = "com.saucelabs.mydemoapp.android"
APP_ACTIVITY = "com.saucelabs.mydemoapp.android.view.activities.SplashActivity"


def _local_config() -> tuple[str, dict]:
    """Android Studio emulator, or a real device over USB, with `appium`
    already running (`npm install -g appium && appium`). The app only needs
    installing (via ANDROID_APP_PATH) the first time — after that,
    appPackage/appActivity alone relaunch it without a reinstall."""
    server_url = os.environ["APPIUM_SERVER_URL"]
    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": os.environ.get("ANDROID_DEVICE_NAME", "emulator-5554"),
        "appium:appPackage": APP_PACKAGE,
        "appium:appActivity": APP_ACTIVITY,
        "appium:noReset": True,
    }
    app_path = os.environ.get("ANDROID_APP_PATH")
    if app_path and os.path.exists(app_path):
        caps["appium:app"] = os.path.abspath(app_path)
        caps["appium:noReset"] = False
    return server_url, caps


def _saucelabs_config() -> tuple[str, dict]:
    """Sauce Labs real device cloud. Upload the APK to Sauce Storage once
    (`saucectl` or the REST API — see README), then point
    SAUCE_APP_STORAGE_FILE at that filename. Real devices are shared/ephemeral
    per session, so there's no appPackage/appActivity relaunch shortcut here
    the way there is locally — the app capability always (re)installs it."""
    region = os.environ.get("SAUCE_REGION", "us-west-1")
    server_url = f"https://ondemand.{region}.saucelabs.com:443/wd/hub"
    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": os.environ.get("SAUCE_DEVICE_NAME", "Google Pixel .*"),
        "appium:platformVersion": os.environ.get("SAUCE_PLATFORM_VERSION", "13"),
        "appium:app": os.environ["SAUCE_APP_STORAGE_FILE"],
        "sauce:options": {
            "username": os.environ["SAUCE_USERNAME"],
            "accessKey": os.environ["SAUCE_ACCESS_KEY"],
            "build": "appium-python-mydemoapp",
            "name": "My Demo App — Android suite",
        },
    }
    return server_url, caps


def _browserstack_config() -> tuple[str, dict]:
    """BrowserStack App Automate. Upload the APK via BrowserStack's app
    upload REST API once (see README), then set BROWSERSTACK_APP_ID to the
    app_url/bs:// id that upload call returns."""
    server_url = "https://hub-cloud.browserstack.com/wd/hub"
    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:app": os.environ["BROWSERSTACK_APP_ID"],
        "bstack:options": {
            "userName": os.environ["BROWSERSTACK_USERNAME"],
            "accessKey": os.environ["BROWSERSTACK_ACCESS_KEY"],
            "deviceName": os.environ.get("BROWSERSTACK_DEVICE_NAME", "Google Pixel 8"),
            "osVersion": os.environ.get("BROWSERSTACK_OS_VERSION", "14.0"),
            "projectName": "appium-python-mydemoapp",
        },
    }
    return server_url, caps


_PROVIDERS = {
    "local": _local_config,
    "saucelabs": _saucelabs_config,
    "browserstack": _browserstack_config,
}


@pytest.fixture(scope="function")
def driver():
    provider = os.environ.get("MOBILE_TEST_PROVIDER", "local").lower()
    if provider not in _PROVIDERS:
        raise ValueError(
            f"Unknown MOBILE_TEST_PROVIDER '{provider}' — must be one of {list(_PROVIDERS)}"
        )

    server_url, raw_caps = _PROVIDERS[provider]()
    # Relying on this fixture's own `finally: drv.quit()` to end a remote
    # session is not enough on its own — if the test process is hard-killed
    # (e.g. a subprocess-level timeout in whatever's running pytest), that
    # `finally` block never executes, and a remote device session can be
    # left running indefinitely, burning paid minutes and blocking any
    # concurrency-limited account from starting a new session at all (hit
    # exactly this in practice). newCommandTimeout is the server-side half
    # of that safety net: the remote session ends itself once no new
    # command arrives within this window, regardless of what happens to the
    # local client process. Applies uniformly to all providers since it's
    # part of the base Appium spec, not a provider extension.
    raw_caps.setdefault("appium:newCommandTimeout", 60)
    options = UiAutomator2Options()
    options.load_capabilities(raw_caps)

    drv = webdriver.Remote(server_url, options=options)
    drv.implicitly_wait(15)
    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Most flows (catalog, cart, checkout) need a logged-in session first."""
    from pages.login_page import LoginPage

    login_page = LoginPage(driver)
    login_page.login_as_standard_user()
    return driver

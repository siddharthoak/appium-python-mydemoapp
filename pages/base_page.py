from appium.webdriver.common.appiumby import AppiumBy

APP_PACKAGE = "com.saucelabs.mydemoapp.android"


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def _el(self, resource_id: str):
        return self.driver.find_element(AppiumBy.ID, f"{APP_PACKAGE}:id/{resource_id}")

    def _els(self, resource_id: str):
        return self.driver.find_elements(AppiumBy.ID, f"{APP_PACKAGE}:id/{resource_id}")

    # menu_header_layout.xml — included in activity_main.xml's header, so
    # present on every screen, not specific to any one fragment/page.
    def open_cart(self):
        self._el("cartRL").click()

    def cart_badge_count(self) -> int:
        badges = self._els("cartTV")
        return int(badges[0].text) if badges else 0

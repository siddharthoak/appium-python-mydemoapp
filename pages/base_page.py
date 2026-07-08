from appium.webdriver.common.appiumby import AppiumBy

APP_PACKAGE = "com.saucelabs.mydemoapp.android"


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def _el(self, resource_id: str):
        return self.driver.find_element(AppiumBy.ID, f"{APP_PACKAGE}:id/{resource_id}")

    def _els(self, resource_id: str):
        return self.driver.find_elements(AppiumBy.ID, f"{APP_PACKAGE}:id/{resource_id}")

    def _el_scroll_to(self, resource_id: str):
        """Like _el(), but scrolls the nearest scrollable container until
        the element is actually in view first — confirmed live that a plain
        find_element(By.ID) can fail to find an element on this app's
        product detail screen (fragment_product_detail.xml's cartBt) even
        though its root is a real ScrollView, not a lazily-inflating
        RecyclerView. Same UiScrollable pattern already proven necessary for
        the Login menu drawer; using it as the default for any element that
        might render below an initially-visible viewport, rather than
        re-diagnosing this per screen."""
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiScrollable(new UiSelector().scrollable(true))"
            f'.scrollIntoView(new UiSelector().resourceId("{APP_PACKAGE}:id/{resource_id}"))',
        )

    # menu_header_layout.xml — included in activity_main.xml's header, so
    # present on every screen, not specific to any one fragment/page.
    def open_cart(self):
        self._el("cartRL").click()

    def cart_badge_count(self) -> int:
        badges = self._els("cartTV")
        return int(badges[0].text) if badges else 0

    def open_menu(self):
        """menuIV — the hamburger icon in the shared header, opens the
        navigation drawer (Login/Logout, Cart, About, etc.)."""
        self._el("menuIV").click()

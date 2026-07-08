from appium.webdriver.common.appiumby import AppiumBy

from .base_page import BasePage


class CatalogPage(BasePage):
    """fragment_product_catalog.xml (productRV) + item_products.xml (titleTV/priceTV)."""

    def product_titles(self) -> list[str]:
        return [e.text for e in self._els("titleTV")]

    def select_product(self, product_name: str):
        # productRV is a scrollable RecyclerView with no per-row resource-id
        # unique enough to select by — a text-based UiSelector query is the
        # standard, robust way to pick one specific item out of a list like
        # this in Appium/UiAutomator2.
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{product_name}")',
        ).click()

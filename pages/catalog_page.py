from appium.webdriver.common.appiumby import AppiumBy

from .base_page import APP_PACKAGE, BasePage


class CatalogPage(BasePage):
    """fragment_product_catalog.xml (productRV) + item_products.xml (titleTV/priceTV)."""

    def product_titles(self) -> list[str]:
        return [e.text for e in self._els("titleTV")]

    def select_product(self, product_name: str):
        # Confirmed against ProductsAdapter.java's real onBindViewHolder:
        # only productIV (the product image) has a click listener attached —
        # titleTV and priceTV are plain, non-interactive TextViews. Tapping
        # titleTV directly (this method's original implementation) succeeds
        # mechanically (the element exists and is tappable) but never
        # navigates anywhere, since nothing is listening for that tap —
        # confirmed live: a NoSuchElementException immediately afterward on
        # the product detail screen's cartBt, because that screen was never
        # reached. fromParent() finds productIV among this specific row's
        # siblings, using the title text purely as a landmark to pick the
        # right row out of the scrollable list — same reason a bare
        # UiSelector on productIV alone wouldn't work, since that resource-id
        # repeats across every row.
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{product_name}")'
            f'.fromParent(new UiSelector().resourceId("{APP_PACKAGE}:id/productIV"))',
        ).click()

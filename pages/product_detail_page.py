from .base_page import BasePage


class ProductDetailPage(BasePage):
    """fragment_product_detail.xml — cartBt/plusIV/minusIV/noTV are the real
    resource-ids for the add-to-cart action and quantity stepper."""

    def quantity(self) -> int:
        return int(self._el_scroll_to("noTV").text)

    def increase_quantity(self, times: int = 1):
        for _ in range(times):
            self._el_scroll_to("plusIV").click()

    def decrease_quantity(self, times: int = 1):
        for _ in range(times):
            self._el_scroll_to("minusIV").click()

    def add_to_cart(self):
        # Confirmed live: this section (addToCartLL, containing cartBt/
        # plusIV/minusIV/noTV) can render below the initially-visible
        # viewport on fragment_product_detail.xml's ScrollView — a plain
        # find_element(By.ID) failed with "no such element" despite the
        # element being genuinely present in a real ScrollView (not a
        # lazily-inflating RecyclerView), so this needs the same
        # scroll-into-view treatment as the Login menu drawer.
        self._el_scroll_to("cartBt").click()

    def price_text(self) -> str:
        return self._el("priceTV").text

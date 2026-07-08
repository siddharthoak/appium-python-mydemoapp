from .base_page import BasePage


class ProductDetailPage(BasePage):
    """fragment_product_detail.xml — cartBt/plusIV/minusIV/noTV are the real
    resource-ids for the add-to-cart action and quantity stepper."""

    def quantity(self) -> int:
        return int(self._el("noTV").text)

    def increase_quantity(self, times: int = 1):
        for _ in range(times):
            self._el("plusIV").click()

    def decrease_quantity(self, times: int = 1):
        for _ in range(times):
            self._el("minusIV").click()

    def add_to_cart(self):
        self._el("cartBt").click()

    def price_text(self) -> str:
        return self._el("priceTV").text

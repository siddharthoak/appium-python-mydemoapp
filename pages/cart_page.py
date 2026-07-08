from .base_page import BasePage


class CartPage(BasePage):
    """fragment_cart.xml — itemsTV/totalPriceTV/cartBt (checkout) at the cart
    level; item_my_cart.xml's removeBt for a per-row remove action."""

    def is_empty(self) -> bool:
        return len(self._els("noItemTitleTV")) > 0

    def item_count_text(self) -> str:
        return self._el("itemsTV").text

    def total_price_text(self) -> str:
        return self._el("totalPriceTV").text

    def remove_first_item(self):
        # item_my_cart.xml's removeBt has no per-row-unique resource-id in
        # this app, so this removes whichever row currently renders first —
        # fine for the single-item scenarios this reference repo covers;
        # a name-scoped removal would need a UiSelector query scoped to the
        # specific row's container, left out to keep this focused.
        self._el("removeBt").click()

    def proceed_to_checkout(self):
        self._el("cartBt").click()

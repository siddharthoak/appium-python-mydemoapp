from .base_page import BasePage


class CheckoutPage(BasePage):
    """fragment_checkout_info.xml — fullNameET/address1ET/.../paymentBtn are
    the real resource-ids for the shipping-info step."""

    def fill_shipping_info(
        self,
        full_name: str,
        address1: str,
        city: str,
        state: str,
        zip_code: str,
        country: str,
        address2: str = "",
    ):
        self._el("fullNameET").send_keys(full_name)
        self._el("address1ET").send_keys(address1)
        if address2:
            self._el("address2ET").send_keys(address2)
        self._el("cityET").send_keys(city)
        self._el("stateET").send_keys(state)
        self._el("zipET").send_keys(zip_code)
        self._el("countryET").send_keys(country)

    def tap_to_payment(self):
        self._el("paymentBtn").click()

    def full_name_error_text(self) -> str:
        return self._el("fullNameErrorTV").text

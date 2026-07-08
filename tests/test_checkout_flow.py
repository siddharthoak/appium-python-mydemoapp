from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from pages.product_detail_page import ProductDetailPage


def _add_first_product_and_open_cart(driver):
    catalog_page = CatalogPage(driver)
    products = catalog_page.product_titles()
    catalog_page.select_product(products[0])

    detail_page = ProductDetailPage(driver)
    detail_page.add_to_cart()
    detail_page.open_cart()


def test_complete_checkout_with_valid_shipping_info(logged_in_driver):
    _add_first_product_and_open_cart(logged_in_driver)

    cart_page = CartPage(logged_in_driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.fill_shipping_info(
        full_name="Jane Doe",
        address1="123 Main St",
        city="Anytown",
        state="CA",
        zip_code="94105",
        country="USA",
    )
    checkout_page.tap_to_payment()


def test_checkout_requires_full_name(logged_in_driver):
    _add_first_product_and_open_cart(logged_in_driver)

    cart_page = CartPage(logged_in_driver)
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.fill_shipping_info(
        full_name="",
        address1="123 Main St",
        city="Anytown",
        state="CA",
        zip_code="94105",
        country="USA",
    )
    checkout_page.tap_to_payment()

    assert checkout_page.full_name_error_text() != ""

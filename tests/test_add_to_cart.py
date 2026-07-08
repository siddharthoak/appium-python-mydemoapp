from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.product_detail_page import ProductDetailPage


def test_add_single_product_to_cart(logged_in_driver):
    catalog_page = CatalogPage(logged_in_driver)
    products = catalog_page.product_titles()
    assert products, "Catalog returned no products to select from"

    catalog_page.select_product(products[0])

    detail_page = ProductDetailPage(logged_in_driver)
    detail_page.add_to_cart()
    assert detail_page.cart_badge_count() == 1

    detail_page.open_cart()
    cart_page = CartPage(logged_in_driver)
    assert "1" in cart_page.item_count_text()


def test_increase_quantity_before_adding_to_cart(logged_in_driver):
    catalog_page = CatalogPage(logged_in_driver)
    products = catalog_page.product_titles()
    catalog_page.select_product(products[0])

    detail_page = ProductDetailPage(logged_in_driver)
    assert detail_page.quantity() == 1
    detail_page.increase_quantity(times=2)
    assert detail_page.quantity() == 3


def test_remove_product_clears_cart(logged_in_driver):
    catalog_page = CatalogPage(logged_in_driver)
    products = catalog_page.product_titles()
    catalog_page.select_product(products[0])

    detail_page = ProductDetailPage(logged_in_driver)
    detail_page.add_to_cart()
    detail_page.open_cart()

    cart_page = CartPage(logged_in_driver)
    cart_page.remove_first_item()
    assert cart_page.is_empty()

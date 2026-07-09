from pages.catalog_page import CatalogPage
from pages.product_detail_page import ProductDetailPage


def test_add_product_and_verify_cart_badge(logged_in_driver):
    catalog_page = CatalogPage(logged_in_driver)
    products = catalog_page.product_titles()
    assert products, "Catalog returned no products to select from"

    catalog_page.select_product(products[0])

    detail_page = ProductDetailPage(logged_in_driver)
    detail_page.add_to_cart()
    assert detail_page.cart_badge_count() == 1
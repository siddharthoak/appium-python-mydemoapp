from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


def test_login_and_verify_products_page(driver):
    login_page = LoginPage(driver)
    login_page.navigate_via_menu()
    login_page.enter_username("bod@example.com")
    login_page.enter_password("10203040")
    login_page.tap_login()

    # After a successful login, the app should navigate to the Catalog/Products page.
    # We verify this by checking if product titles are present.
    catalog_page = CatalogPage(driver)
    assert len(catalog_page.product_titles()) > 0, "Expected products to be displayed after successful login"
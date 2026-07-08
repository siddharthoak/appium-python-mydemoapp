from pages.login_page import LoginPage


def test_login_with_standard_credentials(driver):
    login_page = LoginPage(driver)
    login_page.login_as_standard_user()

    # A successful login lands on the product catalog — its title bar is
    # the simplest available signal that the login actually went through.
    from pages.catalog_page import CatalogPage

    catalog_page = CatalogPage(driver)
    assert len(catalog_page.product_titles()) > 0


def test_login_with_blank_username_shows_error(driver):
    login_page = LoginPage(driver)
    login_page.enter_password("any-password")
    login_page.tap_login()

    assert login_page.username_error_text() != ""


def test_login_with_blank_password_shows_error(driver):
    login_page = LoginPage(driver)
    login_page.enter_username("any-username")
    login_page.tap_login()

    assert login_page.password_error_text() != ""

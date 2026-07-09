from pages.catalog_page import CatalogPage


def test_catalog_loads_without_login(driver):
    catalog_page = CatalogPage(driver)
    products = catalog_page.product_titles()
    assert products, "Catalog returned no products, indicating it might not have loaded correctly."
    assert len(products) > 0, "Expected at least one product to be displayed on the catalog page."
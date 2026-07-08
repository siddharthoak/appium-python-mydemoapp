# My Demo App (Android) — Appium-Python Test Suite

Reference Page Object Model test suite for [Sauce Labs' "My Demo App" Android
app](https://github.com/saucelabs/my-demo-app-android) — a real, actively-maintained
open-source app purpose-built for Appium demos, and the mobile counterpart to the
`saucedemo-playwright-python` web repo alongside this one: same login → catalog →
cart → checkout shape, but native mobile locators/gestures instead of web DOM ones.

Package under test: `com.saucelabs.mydemoapp.android`. All resource-ids referenced in
`pages/` were confirmed against the app's real layout XML source, not guessed.

## Structure

```
pages/
  base_page.py          # shared resource-id helper + the cart icon (present on every screen)
  login_page.py
  catalog_page.py        # product list
  product_detail_page.py # add-to-cart, quantity stepper
  cart_page.py
  checkout_page.py       # shipping-info step
tests/
  test_login.py
  test_add_to_cart.py
  test_checkout_flow.py
conftest.py              # provider-dispatch driver fixture — see below
```

## Conventions

- **Locators**: `resource-id` first (`AppiumBy.ID`, package-qualified — `BasePage._el`
  handles the prefix), since every real UI element in this app has one. A `UiSelector`
  text query is used only where resource-ids repeat across list items with no way to
  disambiguate one row from another (`CatalogPage.select_product`).
- **Page objects**: one class per screen, methods are user actions
  (`login()`, `add_to_cart()`), not raw locator getters — same rule as the web repo.
- **Cart icon**: lives in `BasePage`, not `CartPage` — it's part of a shared header
  included on every screen (`menu_header_layout.xml`), not something scoped to one page.

## Running — configurable execution target

Unlike the web repo (which just needs a real browser), Appium needs an actual Android
device or emulator somewhere. This repo doesn't hardcode where that is — set
`MOBILE_TEST_PROVIDER` in `.env` (copy `.env.example`) to pick one:

```bash
pip install -r requirements.txt
cp .env.example .env   # then edit .env for your chosen provider
pytest -v
```

### `local` — Android Studio emulator, or a real device over USB

1. Start an emulator (Android Studio > Device Manager) or plug in a real device with
   USB debugging on.
2. Install the app once: download the APK from the
   [releases page](https://github.com/saucelabs/my-demo-app-android/releases) into
   `./apps/`, set `ANDROID_APP_PATH` in `.env`, run once — after that you can drop
   `ANDROID_APP_PATH` and the app just relaunches via `appPackage`/`appActivity`.
3. Start Appium: `npm install -g appium && appium` (default `http://localhost:4723`).
4. `MOBILE_TEST_PROVIDER=local`, `pytest -v`.

### `saucelabs` — Sauce Labs real device cloud

1. Upload the APK to Sauce Storage (one-time):
   ```bash
   curl -u "$SAUCE_USERNAME:$SAUCE_ACCESS_KEY" \
     -X POST "https://api.us-west-1.saucelabs.com/v1/storage/upload" \
     -F "payload=@./apps/my-demo-app-android.apk" \
     -F "name=my-demo-app-android.apk"
   ```
2. `MOBILE_TEST_PROVIDER=saucelabs`, fill in `SAUCE_*` vars in `.env`, `pytest -v`.

### `browserstack` — BrowserStack App Automate

1. Upload the APK (one-time), capture the `app_url` (`bs://...`) it returns:
   ```bash
   curl -u "$BROWSERSTACK_USERNAME:$BROWSERSTACK_ACCESS_KEY" \
     -X POST "https://api-cloud.browserstack.com/app-automate/upload" \
     -F "file=@./apps/my-demo-app-android.apk"
   ```
2. `MOBILE_TEST_PROVIDER=browserstack`, set `BROWSERSTACK_APP_ID` to that `app_url`,
   fill in the rest of the `BROWSERSTACK_*` vars, `pytest -v`.

Cloud providers (`saucelabs`/`browserstack`) always reference the uploaded app by id —
there's no `appPackage`/`appActivity` relaunch shortcut there, since a cloud device is
ephemeral per session and doesn't already have the app installed the way a persistent
local emulator does.
# appium-python-mydemoapp

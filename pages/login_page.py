from appium.webdriver.common.appiumby import AppiumBy

from .base_page import BasePage

# Real, confirmed literal values from strings.xml (bod_example_com /
# password1TV's static android:text) — used directly rather than tapping the
# on-screen preset rows (username1TV/password1TV etc.). Tapping those looked
# more robust in theory ("don't hardcode credentials that might change
# between app versions") but turned out less robust in practice: on a
# real/cloud device's screen size those rows can sit below the fold, and a
# plain (non-Recycler) ScrollView's off-screen content isn't always present
# in UiAutomator2's queryable hierarchy — confirmed via a live
# NoSuchElementException against Sauce Labs' Android emulator. nameET/
# passwordET are always on-screen near the top of the form regardless of
# scroll position, so typing directly into them has no such fragility.
STANDARD_USERNAME = "bod@example.com"
STANDARD_PASSWORD = "10203040"


class LoginPage(BasePage):
    """fragment_login.xml — nameET/passwordET/loginBtn are the real
    resource-ids in saucelabs/my-demo-app-android's source.

    Confirmed against MainActivity.java's real onCreate/init logic: this app
    has no login wall at all — Product Catalog is unconditionally the
    default landing fragment (`setFragment(FRAGMENT_PRODUCT_CATAlOG, ...)`
    whenever no explicit fragment request is passed in), regardless of
    login state. LoginFragment is only reached deliberately, via the
    hamburger-menu drawer's "Log In" entry (setMenu() in MainActivity.java
    adds a menu item with that exact string, R.string.login = "Log In",
    only when not already logged in) — never automatically on launch.
    navigate_via_menu() below is the one genuine, correct way to reach this
    screen; earlier assumptions in this test suite about landing here
    automatically were wrong and have been removed.
    """

    def navigate_via_menu(self):
        self.open_menu()
        # setMenu() in MainActivity.java builds an 11-item list (Products,
        # Webview, QR, Geolocation, Drawing, About, Reset State, Fingerprint,
        # Virtual USB, Crash app, then Login/Logout last) inside menuRV, a
        # RecyclerView — unlike a plain ScrollView, a RecyclerView doesn't
        # inflate rows it hasn't scrolled to at all, so a bare
        # find_element(text="Log In") can never see it: confirmed live, a
        # plain UiSelector text query polled its full timeout and found
        # nothing. UiScrollable's scrollIntoView is the standard UiAutomator2
        # answer — it scrolls the nearest scrollable container until the
        # target text is actually present, then returns it.
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector().text("Log In"))',
        ).click()

    def enter_username(self, username: str):
        self._el("nameET").send_keys(username)

    def enter_password(self, password: str):
        self._el("passwordET").send_keys(password)

    def tap_login(self):
        self._el("loginBtn").click()

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.tap_login()

    def login_as_standard_user(self):
        self.login(STANDARD_USERNAME, STANDARD_PASSWORD)

    def username_error_text(self) -> str:
        return self._el("nameErrorTV").text

    def password_error_text(self) -> str:
        return self._el("passwordErrorTV").text

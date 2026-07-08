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
    resource-ids in saucelabs/my-demo-app-android's source."""

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

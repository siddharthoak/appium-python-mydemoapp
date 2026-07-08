from .base_page import BasePage


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

    def login_as_preset_user(self, index: int = 1):
        """Tap a preset username/password row (username1TV/password1TV, ...)
        instead of typing literal credentials — the app's own login screen
        offers these as tap-to-fill shortcuts, and using them avoids
        hardcoding credential strings that could change between app
        versions."""
        self._el(f"username{index}TV").click()
        self._el(f"password{index}TV").click()
        self.tap_login()

    def username_error_text(self) -> str:
        return self._el("nameErrorTV").text

    def password_error_text(self) -> str:
        return self._el("passwordErrorTV").text

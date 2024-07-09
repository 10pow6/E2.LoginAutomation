import configparser

from textual.app import App, ComposeResult
from textual.widgets import Static, RichLog , Header, Footer

from screens.login import Login

class E2TUI(App):
    CSS_PATH = "main.css"
    BINDINGS = [("q","quit","Quit the app"),("d", "toggle_dark", "Toggle dark mode"),("w","debug_mode","Debug Mode")]
    config = configparser.ConfigParser()


    def compose(self) -> ComposeResult:
        yield RichLog(highlight=False, markup=True)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

        yield Static()
        

    def action_debug_mode(self) -> None:
        self.app.pop_screen()

    def on_mount(self) -> None:
        self.install_screen(Login(), name="Login")
        self.push_screen(Login())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = E2TUI()
    app.run()
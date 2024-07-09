from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header,Footer,Static,Markdown
#from textual.containers import Vertical
import configparser


class CoreNav(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        yield Profile(classes="box",id="profile")

class Profile(Static):
    border_title="Profile"

    def compose(self) -> ComposeResult:
        yield Markdown("# Profile Name")
        yield Static("Networth: $$$")
        yield Static("Spent: $$$")
        yield Static("Total Tiles: ###")
        yield Static("ESNC: ###")
        yield Static("PESNC: ###")
        yield Static("ETHR: ###")
        yield Markdown("---")


class CoreNavTest(App):
    CSS_PATH = "../main.css"
    BINDINGS = [("q","quit","Quit the app"),("d", "toggle_dark", "Toggle dark mode")]
    config = configparser.ConfigParser()
    

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

        yield Static()

    def on_mount(self) -> None:
        self.install_screen(CoreNav(), name="CoreNav")
        self.push_screen(CoreNav())       

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = CoreNavTest()
    app.run()
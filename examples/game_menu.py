from textual.app import App, ComposeResult, RenderResult
from textual.events import Key
from textual.widget import Widget
from textual.widgets import Button, Header, Label, Input, Static, Footer, TabbedContent, TabPane, RadioButton, RadioSet, Markdown
from textual.reactive import reactive
from textual.containers import Horizontal, Vertical,Container
from textual.screen import Screen


MAIN_TITLE = """
             _                 _                     _____                      
    /\      | |               | |                   / ____|                     
   /  \   __| |_   _____ _ __ | |_ _   _ _ __ ___  | |  __  __ _ _ __ ___   ___ 
  / /\ \ / _` \ \ / / _ \ '_ \| __| | | | '__/ _ \ | | |_ |/ _` | '_ ` _ \ / _ \\
 / ____ \ (_| |\ V /  __/ | | | |_| |_| | | |  __/ | |__| | (_| | | | | | |  __/
/_/    \_\__,_| \_/ \___|_| |_|\__|\__,_|_|  \___|  \_____|\__,_|_| |_| |_|\___|
                                                                                
    
    """
class Center( Container ):
    DEFAULT_CSS = """
    Center {
        height: auto;
        width: 100%;
        align: center middle;
    }
    """

class startScreenButton(Widget):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("Start Game", classes="startScreenBtn"),
            Button("Continue Game", classes="startScreenBtn"),
            Button("Create New Character", classes="startScreenBtn"),
            Button("Exit", classes="startScreenBtn")
        )
   
class StartScreen(Widget):
    def compose(self) -> ComposeResult:
        yield Center(Static(MAIN_TITLE,id="words", classes="box"))
        yield Center(startScreenButton(classes="box"))

class MainApp(App):
    CSS_PATH = "game_menu.css"
    SCREENS = {}
    BINDINGS = [("m", "push_screen('MenuScreen')", "Menu"),
                ("q", "quit", "Quit")
    ]

    TITLE = "Adventure Game"

    def compose(self) -> ComposeResult:
        
        yield Header(show_clock=True)
        yield StartScreen()
        yield Footer()
        
if __name__ == "__main__":
    app = MainApp()
    app.run()
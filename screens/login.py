import os

from textual.app import ComposeResult
from textual.screen import Screen
from textual.reactive import reactive
from textual.containers import Horizontal,Vertical
from textual.widgets import Button, Header, Footer, Static, Label, ListView, ListItem, RichLog, Header, Footer, Input

from components.helpers import helpers
from components.playwright.loginflow import playwright_flows
from components.ascii import ASCIIEarth

CONFIG_DIR="configs"

def read_content( file_name:str ):
    with open(file_name, 'r') as file:
        data = file.read()
    return data


class AsciiArt(Static):
    """A Ascii Art widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets of a asciiart."""
        yield Label(ASCIIEarth.generate_ascii())

class DynamicLabel(Static):
    value = reactive("")

    def compose(self) -> ComposeResult:
        """Create child widgets of a urlbar."""
        yield Label(self.value)

    def watch_value( self ) -> None:
        if self.value is not None:
            self.update( self.value )   

class ConfigBox(Label):
    config_contents = reactive("")

    def __init__( self, **kwargs:any ) -> None:
        super().__init__()

    def watch_config_contents( self ) -> None:
        if self.config_contents is not None:
            self.update( self.config_contents )

class SettingDisplay(Static):
    border_title="Config contents"

    def compose(self) -> ComposeResult:
        yield Vertical(ConfigBox())


class ConfigListItem(ListItem):
    file_name = ""

    def __init__( self, value: str  ) -> None:
        """Initialise the input."""
        
        self.file_name = value
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.file_name)

    
class SettingSelector(Static):
    configs = ListView()
    border_title="Target site"

    def compose(self) -> ComposeResult:
        yield self.configs
        
    
    def on_list_view_selected(self,event ) -> None:
        config_box = self.app.query_one("Login #settings-display ConfigBox")
        config_file = CONFIG_DIR + "/" + event.item.file_name
        data = read_content(config_file)
        self.app.config.read_string(data)
        config_box.config_contents = data

        url_bar = self.app.query_one("Login #url-bar")
        url_bar.value =  self.app.config["TARGET"]["SITE"]

        text_log_msg = ["<Reading Config File: " + config_file + ">"]
        helpers.fitted_log_msg( tui_context=self, text=text_log_msg )
    

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        path = CONFIG_DIR
        dir_list = os.listdir(path)

        for config_name in dir_list:
            self.configs.append(ConfigListItem(config_name) )
        
        config_box = self.app.query_one("Login #settings-display ConfigBox")
        config_file = CONFIG_DIR + "/" + dir_list[0]
        data = read_content(config_file)
        self.app.config.read_string(data)
        config_box.config_contents = data

        url_bar = self.app.query_one("Login #url-bar")
        url_bar.value =  self.app.config["TARGET"]["SITE"]

        text_log = self.app.query_one("Login #logs")
        text_log_msg = ["<Reading Config File: " + config_file + ">"]
        
        helpers.fitted_log_msg( tui_context=self, text=text_log_msg )
    

class ProcessingInfo(Static):
    border_title="Processing Console"

    def compose(self) -> ComposeResult:
        yield RichLog(highlight=False, markup=True, id="logs")


class LoginBox(Static):
    border_title="E2 Login Details"
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label("Username",classes="form-label"),
            Input(placeholder="",id="username"),
            classes="login-box"
        )
        yield Horizontal(
            Label("Password",classes="form-label"),
            Input(placeholder="",password=True,id="password"),
            classes="login-box"
        )
        yield Horizontal(
            Label("OTP     ",classes="form-label"),
            Input(placeholder="",password=True,id="otp"),
            classes="login-box"
        )
        yield Horizontal(
            Button("Login", variant="primary",classes="login-box",id="login"),
            Button("Proceed", variant="primary",classes="login-box",id="proceed",disabled=True),
        )
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login":
            event.button.disabled = True
            settings_selector = self.app.query_one("Login #settings-selector")
            settings_selector.disabled=True

            username = self.app.query_one("Login #username").value
            password = self.app.query_one("Login #password").value
            otp = self.app.query_one("Login #otp").value


            text_log = self.app.query_one("Login #logs")
            text_log_msg = ["<Logging in>",
                            "<Utilizing Playwright Library>",
                            "Targeting: " +  self.app.config["TARGET"]["SITE"],
                            "Please wait..."]
            
            helpers.fitted_log_msg( tui_context=self, text=text_log_msg )

            await playwright_flows.execute_e2_login(
                tui_context=self,
                username=username,
                password=password,
                otp=otp,
                target=self.app.config["TARGET"]["SITE"]
            )

            text_log_msg = ["<Completed Login Process>","Click Proceed to Continue"]
            helpers.fitted_log_msg( tui_context=self, text=text_log_msg )
            proceed_button = self.app.query_one("Login #proceed")
            proceed_button.disabled=False

        elif event.button.id == "proceed":
            self.app.pop_screen()





class Login(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()


        yield DynamicLabel( classes="box",id="url-bar")
        yield AsciiArt(classes="box", id="ascii-art")
        yield LoginBox(classes="box",id="login-box")
        yield ProcessingInfo(classes="box",id="processing-info")
        yield SettingSelector(classes="box",id="settings-selector")
        yield SettingDisplay(classes="box",id="settings-display")
from textual.app import App, ComposeResult
from textual.widgets import Static, Markdown, Footer

class ArticleView(Static):
  def __init__(self, text):
    super().__init__()
    self.text = text
  def compose(self):
    yield Markdown(self.text)

    

class MyApp(App):
  BINDINGS = [("q","quit","Quit the app"),("d", "do_something", "Do something")]

  def compose(self):
    # other widgets, not relavant
    yield ArticleView("# Testx")
    yield Footer()

  async def action_do_something(self):
    # get the markdown text from a website
    await self.app.query_one(Markdown).update("Test")

if __name__ == "__main__":
    app = MyApp()
    app.run()
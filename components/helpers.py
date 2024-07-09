import textwrap

class helpers:
    @staticmethod
    def fit_txt( text: str ):
        WIDTH=54

        return textwrap.wrap( text, width=WIDTH,break_long_words=False,subsequent_indent="   ")
    
    @staticmethod
    def fitted_log_msg( tui_context, text:list, color:str="[bold magenta]"  ):
        # I need to parameterize the selector
        text_log = tui_context.app.query_one("Login #logs")
        for line in text:
            for fitted in helpers.fit_txt( line ):
                text_log.write(color + " " + fitted)
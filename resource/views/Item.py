from kivy.uix.button import Button
import html


class Item(Button):
    def __init__(self, id=0, text=''):
        super().__init__()
        self.id = id
        self.text=html.unescape(text)
        self.background_color = (0, 0, 0, 0)




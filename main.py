from kivy.app import App
from resource.views.Views import View

class GalkaApp(App):
    def build(self):
        return View()

if __name__ == '__main__':
    GalkaApp().run()



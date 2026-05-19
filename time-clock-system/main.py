from kivy.config import Config

Config.set("graphics", "width", "480")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class ClockInLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=20, padding=20, **kwargs)
        
        clock_in_button = Button(
            text="Clock In",
            font_size=30
        )
        
        clock_out_button = Button(
            text="Clock Out",
            font_size=30
        )
        
        self.add_widget(clock_in_button)
        self.add_widget(clock_out_button)


class ClockInApp(App):

    def build(self):
        return ClockInLayout()


if __name__ == "__main__":
    ClockInApp().run()
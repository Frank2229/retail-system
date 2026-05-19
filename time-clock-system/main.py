from kivy.config import Config

Config.set("graphics", "width", "480")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from datetime import datetime


class CameraPlaceholder(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.92, 0.92, 0.92, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        self.add_widget(
            Label(
                text="Camera Inactive",
                font_size=28,
                color=(0.35, 0.35, 0.35, 1)
            )
        )

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class TimeClockLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=20, padding=20, **kwargs)
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)
        
        self.header_label = Label(
            text="[b]TIME CLOCK[/b]",
            markup=True,
            font_size=40,
            size_hint=(1, 0.4),
            font_name="fonts/Montserrat-Bold.ttf",
            color=(0, 0, 0, 1)
        )
        
        self.date_label = Label(
            text="DAY, --/--/----",
            font_size=20,
            size_hint=(1, 0.2),
            font_name="Roboto",
            color=(0, 0, 0, 1)
        )
        
        self.time_label = Label(
            text="--:--:--",
            markup=True,
            font_size=40,
            size_hint=(1, 0.2),
            font_name="fonts/Montserrat-Bold.ttf",
            color=(0, 0, 0, 1)
        )
        
        self.camera_window = CameraPlaceholder(
            size_hint=(1, 2.5)
        )
        
        self.status_label = Label(
            text="System Ready",
            font_size=20,
            size_hint=(1, 0.08),
            color=(0.2, 0.2, 0.2, 1),
            bold=True
        )
        
        main_buttons = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(1, 0.35)
        )
        
        self.clock_in_button = Button(
            text="CLOCK-IN",
            font_size=25,
            font_name="fonts/Montserrat-Bold.ttf",
            background_normal="",
            background_color=(0.2, 0.45, 0.85, 1),
            color=(1, 1, 1, 1)
        )
        
        self.clock_out_button = Button(
            text="CLOCK-OUT",
            font_size=25,
            font_name="fonts/Montserrat-Bold.ttf",
            background_normal="",
            background_color=(0.2, 0.75, 0.45, 1),
            color=(1, 1, 1, 1)
        )
        
        self.manager_button = Button(
            text="MANAGER ACCESS",
            font_size=25,
            font_name="fonts/Montserrat-Bold.ttf",
            size_hint=(1, 0.25),
            background_normal="",
            background_color=(0.15, 0.15, 0.15, 1)
        )
        
        self.add_widget(self.header_label)
        self.add_widget(self.date_label)
        self.add_widget(self.time_label)
        self.add_widget(self.camera_window)
        self.add_widget(self.status_label)
        main_buttons.add_widget(self.clock_in_button)
        main_buttons.add_widget(self.clock_out_button)
        self.add_widget(main_buttons)
        self.add_widget(self.manager_button)
        
        Clock.schedule_interval(self.update_time, 1)
        
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def update_time(self, dt):
        current_time = datetime.now().strftime("%I:%M:%S")
        current_period = datetime.now().strftime("%p")
        
        self.date_label.text = datetime.now().strftime("%A, %m/%d/%Y")
        self.time_label.text = (
            f"[size=50]{current_time}[/size] "
            f"[size=25]{current_period}[/size]"
        )


class TimeClockApp(App):

    def build(self):
        return TimeClockLayout()


if __name__ == "__main__":
    TimeClockApp().run()
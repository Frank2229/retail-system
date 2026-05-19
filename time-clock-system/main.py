import psycopg2

from kivy.config import Config

Config.set("graphics", "width", "480")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

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
        
        self.current_punch_type = None
        
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
        
        self.main_buttons = BoxLayout(
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
        self.main_buttons.add_widget(self.clock_in_button)
        self.main_buttons.add_widget(self.clock_out_button)
        self.add_widget(self.main_buttons)
        self.add_widget(self.manager_button)
        
        Clock.schedule_interval(self.update_time, 1)
        
        self.clock_in_button.bind(on_press=self.clock_in)
        self.clock_out_button.bind(on_press=self.clock_out)
        
    def clock_in(self, instance):
        self.show_keypad("clock_in")

    def clock_out(self, instance):
        self.show_keypad("clock_out")
        
    def connect_db(self):

        return psycopg2.connect(
            host="localhost",
            database="retail_system",
            user="postgres",
            password="Musician2229"
    )
        
    def keypad_pressed(self, instance):
        if hasattr(self, "inactivity_event"):
            self.inactivity_event.cancel()

        self.inactivity_event = Clock.schedule_once(
            self.return_to_main_screen,
            10
        )
        
        value = instance.text

        if value == "Clear":
            self.employee_input.text = ""

        elif value == "Enter":
            employee_number = self.employee_input.text
            self.submit_manual_punch(employee_number)

        else:
            self.employee_input.text += value
            
    def reset_status(self, dt):
        self.status_label.text = "System Ready"
        self.status_label.color = (0.2, 0.2, 0.2, 1)
        
    def return_to_main_screen(self, dt):
        self.show_main_screen()
       
    def show_keypad(self, punch_type):
        self.current_punch_type = punch_type

        self.clear_widgets()

        self.add_widget(self.header_label)
        self.add_widget(self.date_label)
        self.add_widget(self.time_label)

        self.employee_input = TextInput(
            text="",
            hint_text="Enter Employee Number",
            font_size=32,
            multiline=False,
            readonly=True,
            halign="center",
            size_hint=(1, 0.12)
        )

        self.add_widget(self.employee_input)

        keypad = GridLayout(
            cols=3,
            spacing=10,
            size_hint=(1, 0.45)
        )

        buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Clear", "0", "Enter"]

        for value in buttons:
            btn = Button(
                text=value,
                font_size=26,
                background_normal="",
                background_color=(0.9, 0.9, 0.9, 1),
                color=(0, 0, 0, 1)
            )
            btn.bind(on_press=self.keypad_pressed)
            keypad.add_widget(btn)

        self.add_widget(keypad)

        self.status_label.text = f"Manual {punch_type.replace('_', ' ').title()}"
        self.add_widget(self.status_label)
        
        self.inactivity_event = Clock.schedule_once(
            self.return_to_main_screen,
            10
        )
        
    def show_main_screen(self):
        self.clear_widgets()

        self.add_widget(self.header_label)
        self.add_widget(self.date_label)
        self.add_widget(self.time_label)
        self.add_widget(self.camera_window)
        self.status_label.text = "System Ready"
        self.add_widget(self.status_label)
        self.add_widget(self.main_buttons)
        self.add_widget(self.manager_button)
        
    def submit_manual_punch(self, employee_number):

        if hasattr(self, "inactivity_event"):
            self.inactivity_event.cancel()

        if employee_number == "":
            self.status_label.text = "Enter Employee Number"
            self.status_label.color = (0.8, 0.1, 0.1, 1)
            return

        try:
            connection = self.connect_db()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT employee_id, first_name
                FROM employees
                WHERE employee_number = %s
                AND employment_status = 'active'
                """,
                (employee_number,)
            )

            employee = cursor.fetchone()

            if employee is None:
                cursor.close()
                connection.close()

                self.show_main_screen()
                self.status_label.text = "Employee Not Found"
                self.status_label.color = (0.8, 0.1, 0.1, 1)

                Clock.schedule_once(self.reset_status, 2)
                return

            employee_id = employee[0]
            first_name = employee[1]

            cursor.execute(
                """
                SELECT punch_type
                FROM employee_time_punches
                WHERE employee_id = %s
                ORDER BY punch_time DESC
                LIMIT 1
                """,
                (employee_id,)
            )

            last_punch = cursor.fetchone()

            if last_punch is not None and last_punch[0] == self.current_punch_type:
                cursor.close()
                connection.close()

                self.show_main_screen()
                self.status_label.text = "Error: duplicate punch"
                self.status_label.color = (0.8, 0.1, 0.1, 1)

                Clock.schedule_once(self.reset_status, 2)
                return

            cursor.execute(
                """
                INSERT INTO employee_time_punches
                (
                    employee_id,
                    terminal_id,
                    punch_type,
                    verification_method,
                    notes
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    employee_id,
                    1,
                    self.current_punch_type,
                    "manual_override",
                    "Manual keypad entry"
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            punch_action = (
                "Clocked In"
                if self.current_punch_type == "clock_in"
                else "Clocked Out"
            )

            self.show_main_screen()
            self.status_label.text = f"{punch_action}: {first_name}"
            self.status_label.color = (0.1, 0.6, 0.2, 1)

            Clock.schedule_once(self.reset_status, 2)

        except Exception as error:
            self.show_main_screen()

            self.status_label.text = "Database Error"
            self.status_label.color = (0.8, 0.1, 0.1, 1)

            print(error)

            Clock.schedule_once(self.reset_status, 2)
     
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
#python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
import random


class TurtleRace(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.colors = ["red", "blue", "green"]
        self.turtles = []
        self.user_bet = None
        self.running = False
        self.timer = None

        # العنوان
        self.title = Label(
            text="Choose your turtle!",
            font_size=28,
            size_hint=(1, None),
            height=70,
            pos=(0, 500)
        )

        self.add_widget(self.title)

        # زرار الألوان
        self.red_button = Button(
            text="RED",
            size_hint=(None, None),
            size=(130, 55),
            pos=(30, 20)
        )

        self.blue_button = Button(
            text="BLUE",
            size_hint=(None, None),
            size=(130, 55),
            pos=(180, 20)
        )

        self.green_button = Button(
            text="GREEN",
            size_hint=(None, None),
            size=(130, 55),
            pos=(330, 20)
        )

        self.red_button.bind(
            on_press=lambda x: self.start_race("red")
        )

        self.blue_button.bind(
            on_press=lambda x: self.start_race("blue")
        )

        self.green_button.bind(
            on_press=lambda x: self.start_race("green")
        )

        self.add_widget(self.red_button)
        self.add_widget(self.blue_button)
        self.add_widget(self.green_button)

    def start_race(self, color):

        if self.running:
            return

        self.user_bet = color
        self.running = True

        self.red_button.disabled = True
        self.blue_button.disabled = True
        self.green_button.disabled = True

        self.title.text = "RACE!"

        self.create_turtles()

        self.timer = Clock.schedule_interval(
            self.move_turtles,
            0.05
        )

    def create_turtles(self):

        self.turtles = []

        y_positions = [330, 230, 130]

        for i, color in enumerate(self.colors):

            if color == "red":
                rgb = (1, 0, 0)
            elif color == "blue":
                rgb = (0, 0, 1)
            else:
                rgb = (0, 1, 0)

            with self.canvas:
                Color(*rgb)

                shape = Ellipse(
                    pos=(20, y_positions[i]),
                    size=(50, 50)
                )

            self.turtles.append({
                "color": color,
                "shape": shape
            })

    def move_turtles(self, dt):

        for turtle in self.turtles:

            x, y = turtle["shape"].pos

            x += random.randint(2, 8)

            turtle["shape"].pos = (x, y)

            # خط النهاية
            if x >= 700:

                Clock.unschedule(self.move_turtles)

                self.timer = None
                self.running = False

                self.show_result(turtle["color"])

                return

    def show_result(self, winning_color):

        if winning_color == self.user_bet:
            self.title.text = "YOU WIN!"
        else:
            self.title.text = "YOU LOSE!"

        self.play_again_button = Button(
            text="PLAY AGAIN",
            font_size=20,
            size_hint=(None, None),
            size=(200, 60),
            pos=(520, 20)
        )

        self.play_again_button.bind(
            on_press=self.play_again
        )

        self.add_widget(self.play_again_button)

    def play_again(self, button):

        # إزالة زر PLAY AGAIN
        self.remove_widget(button)
        self.play_again_button = None

        # إزالة السلاحف فقط
        for turtle in self.turtles:
            self.canvas.remove(
                turtle["shape"]
            )

        self.turtles = []

        # إعادة الحالة
        self.user_bet = None
        self.running = False
        self.timer = None

        self.title.text = "Choose your turtle!"

        # تفعيل الأزرار
        self.red_button.disabled = False
        self.blue_button.disabled = False
        self.green_button.disabled = False


class TurtleRaceApp(App):

    def build(self):
        return TurtleRace()


TurtleRaceApp().run()


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class VideoSearchScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(VideoSearchScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 50, 20, 50]

        with self.canvas.before:
            Color(0.69, 0.94, 0.92, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        self.search_query_panel = TextInput(
            hint_text='Search...',
            multiline=False,
            size_hint=(None, None),
            size=(935, 50),
            pos_hint={'x': 0.0, 'y': 2.0},
            background_color=(1, 1, 1, 1)
        )

        self.search_button = Button(
            text='Search',
            on_press=self.perform_search,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'x': 0.0, 'y': 2.0}, 
            background_color=(0.12, 0.43, 0.94, 1)
        )

        self.add_widget(self.search_query_panel)
        self.add_widget(self.search_button)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def perform_search(self, instance):
        search_query = self.search_query_panel.text
        print(f"Search : {search_query}")

class VideoSearchApp(App):
    def build(self):
        return VideoSearchScreen()

if __name__ == '__main__':
    VideoSearchApp().run()
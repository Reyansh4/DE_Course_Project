from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle


class VideoSearchScreen(Screen):
    def __init__(self, **kwargs):
        super(VideoSearchScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 50, 20, 50])

        with self.layout.canvas.before:
            Color(0.69, 0.94, 0.92, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.layout.bind(size=self._update_rect, pos=self._update_rect)

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

        self.layout.add_widget(self.search_query_panel)
        self.layout.add_widget(self.search_button)
        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def perform_search(self, instance):
        search_query = self.search_query_panel.text
        print(f"Search : {search_query}")
        app = App.get_running_app()
        app.root.current = 'result'


class SearchResultScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchResultScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 50, 20, 50])
        self.layout.add_widget(Label(text="Search Result Screen"))
        self.add_widget(self.layout)


class VideoSearchApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(VideoSearchScreen(name='search'))
        sm.add_widget(SearchResultScreen(name='result'))
        return sm


if __name__ == '__main__':
    VideoSearchApp().run()
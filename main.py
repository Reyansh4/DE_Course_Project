from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.graphics import Color, Rectangle
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage

class VideoSearchScreen(Screen):
    def __init__(self, **kwargs):
        super(VideoSearchScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 50, 20, 50])

        with self.layout.canvas.before:
            Color(0,0,0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        self.search_query_panel = TextInput(
            hint_text='Search...',
            multiline=False,
            size_hint=(None, None),
            size=(935, 50),
            pos_hint={'center_x': 0.5},
            background_color=(1, 1, 1, 1)
        )

        self.search_label = Label(
            text='SEARCH',
            font_size=40,
            halign='center',
            valign='middle'
        )

        self.search_button = Button(
            text='Search',
            on_press=self.perform_search,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5},
            background_color=(0.12, 0.43, 0.94, 1)
        )

        self.layout.add_widget(self.search_label)
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
        sm = app.root
        sm.transition.direction = 'left'
        sm.current = 'result'

class SearchResultScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchResultScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal', padding=[20, 50, 20, 50])

        self.video_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        self.back_button = Button(
            text='Back',
            on_press=self.go_back,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.1},
            background_color=(0.12, 0.43, 0.94, 1)
        )

        video = VideoPlayer(source='traffic.mp4', state='pause', options={'allow_stretch': True})
        video.size_hint_y = 1.0

        self.video_layout.add_widget(self.back_button)
        self.video_layout.add_widget(video)

        self.description_layout = BoxLayout(orientation='vertical', size_hint=(0.2, 1))
        self.description_label = Label(text='Video Description', font_size=20)
        self.description_layout.add_widget(self.description_label)

        images = ['img.jpeg','img.jpeg','img.jpeg']

        bottom_layout = GridLayout(cols=3, size_hint_y=None, height=100)
        for source in images:
            thumbnail = AsyncImage(source=source)
            thumbnail.size_hint = (1, None)
            thumbnail.height = 100
            box = BoxLayout(orientation='horizontal')
            box.add_widget(thumbnail)
            box.bind(size=self._update_rect, pos=self._update_rect)
            bottom_layout.add_widget(box)

        self.layout.add_widget(self.video_layout)
        self.layout.add_widget(self.description_layout)
        self.layout.add_widget(bottom_layout)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0, 0, 0, 1)
            rect = Rectangle(size=instance.size, pos=instance.pos)

    def go_back(self, instance):
        app = App.get_running_app()
        sm = app.root
        sm.transition.direction = 'right'
        sm.current = 'search'

class VideoSearchApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(VideoSearchScreen(name='search'))
        sm.add_widget(SearchResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    VideoSearchApp().run()
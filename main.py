from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from SQL_db_setup import VideoDatabase
from Mongo_db_setup import VideoMongoDatabase

class VideoSearchScreen(Screen):
    def __init__(self, video_db,video_mongo_db,**kwargs):
        super(VideoSearchScreen, self).__init__(**kwargs)
        self.video_db = video_db
        self.video_mongo_db = video_mongo_db
        self.layout = BoxLayout(orientation='vertical', padding=[20, 50, 20, 50])

        with self.layout.canvas.before:
            Color(0, 0, 0, 1)
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

        self.video_description_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1))
        self.back_button = Button(
            text='Back',
            on_press=self.go_back,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.2},
            background_color=(0.12, 0.43, 0.94, 1)
        )
        self.video_description = Label(text='Video Description', font_size=20)

        self.video_description_layout.add_widget(self.back_button)
        self.video_description_layout.add_widget(self.video_description)

        data_from_mongo = [
            {'title': 'Video 2', 'details': 'Details 2', 'info': 'data2',
             'thumbnail': 'https://akm-img-a-in.tosshub.com/indiatoday/images/story/media_bank/202309/second-track-badass-from-thalapathy-vijays-leo-will-release-on-september-28-272346380-16x9.jpg?VersionId=XpzDqWNDkrtBevS0gfdJg3BF6FBvZw9C'},
            {'title': 'Video 1', 'details': 'Details 1', 'info': 'data1',
             'thumbnail': 'https://akm-img-a-in.tosshub.com/indiatoday/images/story/media_bank/202309/second-track-badass-from-thalapathy-vijays-leo-will-release-on-september-28-272346380-16x9.jpg?VersionId=XpzDqWNDkrtBevS0gfdJg3BF6FBvZw9C'},
            {'title': 'Video 3', 'details': 'Details 3', 'info': 'data3',
             'thumbnail': 'https://akm-img-a-in.tosshub.com/indiatoday/images/story/media_bank/202309/second-track-badass-from-thalapathy-vijays-leo-will-release-on-september-28-272346380-16x9.jpg?VersionId=XpzDqWNDkrtBevS0gfdJg3BF6FBvZw9C'}
        ]

        self.thumbnail_layout = GridLayout(cols=1, size_hint=(0.3, 1))
        for i, video_data in enumerate(data_from_mongo):
            thumbnail = AsyncImage(source=video_data['thumbnail'])
            thumbnail.size_hint = (1, None)
            thumbnail.height = 300
            thumbnail.idx = i
            thumbnail.bind(on_touch_down=self.show_info)
            self.thumbnail_layout.add_widget(thumbnail)

        self.title_details_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        for video_data in data_from_mongo:
            info_layout = BoxLayout(orientation='vertical', size_hint_x=0.8)

            title_label = Label(text=video_data['title'])
            info_layout.add_widget(title_label)

            details_label = Label(text=video_data['details'])
            info_layout.add_widget(details_label)

            self.title_details_layout.add_widget(info_layout)

        self.layout.add_widget(self.video_description_layout)
        self.layout.add_widget(self.thumbnail_layout)
        self.layout.add_widget(self.title_details_layout)

        self.add_widget(self.layout)

    def go_back(self, instance):
        app = App.get_running_app()
        sm = app.root
        sm.transition.direction = 'right'
        sm.current = 'search'

    def show_info(self, instance, touch):
        if touch.button == 'left' and instance.collide_point(*touch.pos):
            thumbnail_idx = instance.idx
            data_from_mongo = [
                {'title': 'Video 2', 'details': 'Details 2', 'info': 'data2',
                'thumbnail': 'https://akm-img-a-in.tosshub.com/indiatoday/images/story/media_bank/202309/second-track-badass-from-thalapathy-vijays-leo-will-release-on-september-28-272346380-16x9.jpg?VersionId=XpzDqWNDkrtBevS0gfdJg3BF6FBvZw9C'},
                {'title': 'Video 1', 'details': 'Details 1', 'info': 'data1',
                'thumbnail': 'https://akm-img-a-in.tosshub.com/indiatoday/images/story/media_bank/202309/second-track-badass-from-thalapathy-vijays-leo-will-release-on-september-28-272346380-16x9.jpg?VersionId=XpzDqWNDkrtBevS0gfdJg3BF6FBvZw9C'},
                {'title': 'Video 3', 'details': 'Details 3', 'info': 'data3',
                'thumbnail': 'https://akm-img-a-in.tosshub.com/indiatoday/images/story/media_bank/202309/second-track-badass-from-thalapathy-vijays-leo-will-release-on-september-28-272346380-16x9.jpg?VersionId=XpzDqWNDkrtBevS0gfdJg3BF6FBvZw9C'}
            ]
            
            self.video_description.text = f"Info: {data_from_mongo[thumbnail_idx]['info']}"

class VideoSearchApp(App):
    def build(self):
        sm = ScreenManager()
        video_db =  VideoDatabase(user='root', password='Rey@nsh4', database='Course_Project')
        video_mongo_db = VideoMongoDatabase(database_name='Course_Project')
        search_screen = VideoSearchScreen(video_db=video_db, video_mongo_db=video_mongo_db, name='search')
        result_screen = SearchResultScreen(name='result')
        sm.add_widget(search_screen)
        sm.add_widget(result_screen)
        return sm

if __name__ == '__main__':
    VideoSearchApp().run()
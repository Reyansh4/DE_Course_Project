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
from Neo_db_setup import VideoGraphDatabase

class VideoSearchScreen(Screen):
    def __init__(self, video_db, video_mongo_db, neo_var, **kwargs):
        super(VideoSearchScreen, self).__init__(**kwargs)
        self.video_db = video_db
        self.video_mongo_db = video_mongo_db
        self.neo_db = neo_var
        self.id = 'search_screen'
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
            on_press=self.search_process,
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

    def perform_search(self):
        search_query = self.search_query_panel.text
        print(f"Search : {search_query}")
        return search_query

    def search_process(self, search_query=None):
        search_query = self.perform_search()
        mongo_var = VideoMongoDatabase(database_name='Course_Project')
        result = mongo_var.perform_search(search_query)
        sql_var = VideoDatabase(user="root", password="Rey@nsh4", database="Course_Project")
        primary_video_id = []
        primary_video_id = result[0]['videoInfo']['id']
        Neo_var = VideoGraphDatabase(uri="bolt://localhost:7687", user="neo4j", password="Rey@nsh4")
        other_video_ids = []
        other_video_ids = Neo_var.get_most_connected_videos(primary_video_id)
        req_video_ids = []
        req_video_ids.append(primary_video_id)
        data_from_mongo = {}
        for i in range(0, len(other_video_ids)):
            req_video_ids.append(other_video_ids[i])
        for vid in req_video_ids:
            info = mongo_var.get_info(vid)
            stats_count = sql_var.performing_search(vid)
            engagement_count = sql_var.performing_search_2(vid)
            combined_data = {**info, **stats_count, **engagement_count}
            data_from_mongo[vid] = combined_data
        app = App.get_running_app()
        sm = app.root
        sm.transition.direction = 'left'
        sm.current = 'result'
        #print("The Keys in the dictionary", list(data_from_mongo.keys()))
        result_screen = sm.get_screen('result')
        result_screen.update_data(data_from_mongo)

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

        self.thumbnail_layout = GridLayout(cols=1, size_hint=(0.3, 1))

        self.layout.add_widget(self.video_description_layout)
        self.layout.add_widget(self.thumbnail_layout)

        self.add_widget(self.layout)

        self.data_from_mongo ={}

    def go_back(self, instance):
        app = App.get_running_app()
        sm = app.root
        sm.transition.direction = 'right'
        sm.current = 'search'
        self.data_from_mongo = {}

    def show_info(self, instance, touch):
        if touch.button == 'left' and instance.collide_point(*touch.pos):
            thumbnail_idx = instance.idx
            try:
                video_id = list(self.data_from_mongo.keys())[thumbnail_idx]
                video_data = self.data_from_mongo[video_id]
                
                if 'videoInfo' in video_data:
                    video_info = video_data['videoInfo']
                    if 'snippet' in video_info:
                        snippet = video_info['snippet']
                        thumbnail_url = snippet.get('thumbnails', {}).get('high', {}).get('url', '')
                        title = snippet.get('title', '')
                        kind = video_info.get('kind', '')
                        etag = video_info.get('etag', '')
                        channel_id = snippet.get('channelId', '')
                        published_at = snippet.get('publishedAt', '')
                        live_broadcast_content = snippet.get('liveBroadcastContent', '')
                        channel_title = snippet.get('channelTitle', '')
                        cat_id = snippet.get('categoryId', '')
                        commentCount = video_data.get('commentCount', {})
                        viewCount = video_data.get('viewCount', {})
                        favoriteCount = video_data.get('favoriteCount', {})
                        dislikeCount = video_data.get('dislikeCount', {})
                        likeCount = video_data.get('likeCount', {})
                        engagement = video_data.get('engagement', {})
                        engagement_ratio = video_data.get('engagement_ratio', {})
                        clash_of_tastes = video_data.get('clash_of_tastes', {})
                        self.video_description.text = (
                            f"Title: {title}\n"
                            f"Published_at: {published_at}\n"
                            f"Broadcast: {live_broadcast_content}\n"
                            f"Channel: {channel_title}\n"
                            f"Kind: {kind}\n"
                            f"Channel_id: {channel_id}\n"
                            f"Category_id: {cat_id}\n"
                            f"Etag: {etag}\n"
                            f"ID: {video_id}\n"
                            f"URL: {thumbnail_url}\n"
                            "Statistics:\n"
                            f"commentcount: {commentCount}\n"
                            f"viewcount: {viewCount}\n"
                            f"favoriteCount: {favoriteCount}\n"
                            f"dislikeCount: {dislikeCount}\n"
                            f"likeCount: {likeCount}\n"
                            f"engagement: {engagement}\n"
                            f"engagement_ratio: {engagement_ratio}\n"
                            f"clash_of_tastes: {clash_of_tastes}"
                        )
                    else:
                        print("Error: 'snippet' key not found in video_info")
                else:
                    print(f"Error: 'videoInfo' key not found in data_from_mongo at index {thumbnail_idx}")
            except (IndexError, KeyError) as e:
                print(f"Error: {e}. Couldn't find 'videoInfo' in data_from_mongo at index {thumbnail_idx}")

    def update_data(self, data_from_mongo):
        #print("Dictionary imported from other place", data_from_mongo)
        self.thumbnail_layout.clear_widgets()
        self.video_description.text = ""
        self.data_from_mongo = data_from_mongo
        for i, video_id in enumerate(self.data_from_mongo):
            video_data = self.data_from_mongo[video_id]
            thumbnail_url = video_data['videoInfo']['snippet']['thumbnails']['high']['url']
            thumbnail = AsyncImage(source=thumbnail_url)
            thumbnail.size_hint = (1, None)
            thumbnail.height = 300
            thumbnail.idx = i
            thumbnail.bind(on_touch_down=self.show_info)
            self.thumbnail_layout.add_widget(thumbnail)
            info_layout = BoxLayout(orientation='vertical', size_hint_x=0.8)
            self.add_widget(info_layout)

class VideoSearchApp(App):
    def build(self):
        sm = ScreenManager()
        video_db = VideoDatabase(user='root', password='Rey@nsh4', database='Course_Project')
        video_mongo_db = VideoMongoDatabase(database_name='Course_Project')
        neo_var = VideoGraphDatabase(uri="bolt://localhost:7687", user="neo4j", password="Rey@nsh4")
        search_screen = VideoSearchScreen(video_db=video_db, video_mongo_db=video_mongo_db, neo_var=neo_var, name='search')
        result_screen = SearchResultScreen(name='result')
        sm.add_widget(search_screen)
        sm.add_widget(result_screen)
        return sm

if __name__ == '__main__':
    VideoSearchApp().run()
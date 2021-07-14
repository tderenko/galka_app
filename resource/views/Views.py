from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from resource.models.Galka import Galka
from resource.views.Item import Item
from kivy.uix.button import Button
from kivy.uix.label import Label
from resource.services.Pagination import Pagination
import html
import re

Window.size = (480, 853)


class View(GridLayout):
    def __init__(self):
        super(View, self).__init__()
        self.content = BoxLayout()
        self.content.orientation = 'vertical'
        self.current_cat = 33
        self.per_page = 20
        self.categories = Galka().get_categories()
        self.posts = list()
        self.build_posts(cat_id=self.current_cat)
        self.show_menu = False
        self.news_items.add_widget(self.content)

    def build_posts(self, cat_id=None, load=True, current_page=1):
        self.content.clear_widgets()

        if load:
            cat_id = cat_id if cat_id else self.current_cat
            self.posts = Galka().get_posts(cat_id=cat_id, page=current_page, per_page=self.per_page)

        for post in self.posts['posts']:
            article = Item(id=post['id'], text=post['title']['rendered'])
            article.bind(on_release=self.build_post)
            article.size_hint_y = None
            article.size = (200, 70)
            self.content.add_widget(article)

        pagination = Pagination(data={
            'total': int(self.posts['total']),
            'limit': int(self.posts['per_page']),
            'currentPage': int(self.posts['page'])
        }).run()
        self.pagi_section.clear_widgets()
        for page in pagination['pages']:
            but = Item(id=page['page'], text=str(page['label']))
            if page['class'] == 'current':
                but.background_color = (0.1, 0.9, 0.9, 1)
            else:
                but.background_color = (0.4, 0.7, 0.2, 1)
            but.bind(on_release=self.select_pagination)
            self.pagi_section.add_widget(but)


    def build_category(self):
        self.pagi_section.clear_widgets()
        self.content.clear_widgets()
        for category in self.categories:
            cat = Item(id=category['id'], text=category['name'])
            cat.background_color = (0.1, 1, 1, 1)
            cat.bind(on_release=self.select_category)
            self.content.add_widget(cat)

    def build_post(self, post):
        self.pagi_section.clear_widgets()
        self.content.clear_widgets()
        post_data = Galka().get_post(id=post.id)
        self.content.add_widget(Button(text="Return Back!", on_release=self.return_back, background_color=(1, 1, 0.5, 1), size_hint=(0.5, None), height=40, halign='center'))
        self.content.add_widget(Label(text=html.unescape(post_data['title']['rendered']), color=(0.5, 1, 0.5, 1), size_hint=(1, 0.1)))
        text = Label(text=re.sub(re.compile('<.*?>'), '', html.unescape(post_data['content']['rendered'])))
        text.bind(size=text.setter('text_size'))
        self.content.add_widget(text)

    def click_menu(self):
        self.show_menu = not self.show_menu
        if self.show_menu:
            self.build_category()
        else:
            self.build_posts(load=False)

    def select_category(self, cat):
        self.show_menu = False
        if self.current_cat == cat.id:
            self.build_posts(load=False)
        else:
            self.current_cat = cat.id
            self.build_posts()

    def select_pagination(self, pagination):
        self.build_posts(current_page=pagination.id)

    def return_back(self, value):
        self.build_posts(load=False)
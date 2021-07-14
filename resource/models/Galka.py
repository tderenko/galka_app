import requests
import json


class Galka:
    def get_posts(self, cat_id=0, per_page=10, page=1):
        res = requests.get('https://galka.if.ua/wp-json/wp/v2/posts?categories=' + str(cat_id) + '&per_page=' + str(per_page) + '&page=' + str(page) + '&_fields=' + ','.join(['id', 'title', 'date', 'excerpt','_links']))
        return {'posts': json.loads(res.text), 'total': res.headers['X-WP-Total'], 'per_page': per_page, 'page': page}

    def get_categories(self):
        res = requests.get('https://galka.if.ua/wp-json/wp/v2/categories?context=embed')
        return json.loads(res.text)

    def get_post(self, id):
        res = requests.get('https://galka.if.ua/wp-json/wp/v2/posts/' + str(id))
        return json.loads(res.text)
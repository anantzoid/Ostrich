from flask import request, session
from app import webapp
from app.models import Utils

class Cache():
    def __init__(self):
        if webapp.config['APP_ENV'] == 'dev':
            from werkzeug.contrib.cache import SimpleCache
            self.cache = SimpleCache()
        else:
            from werkzeug.contrib.cache import MemcachedCache
            self.cache = MemcachedCache(['127.0.0.1:11211'])

    def get(self, cache_key=''):
        if 'cache' in request.args and request.args.get('cache') == 'clear':
            user_data = session.get('_user', None)
            if user_data and user_data['is_admin']:
                return None
        return self.cache.get(cache_key)

    def set(self, cache_key='', data=None, timeout=1000):
        self.cache.set(cache_key, data, timeout)
        return True

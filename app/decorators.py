from threading import Thread
from functools import wraps
from flask import session
from app import cache

def async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def user_session(func):
    @wraps(func)
    def wrapper(**kwargs):
        user_data = session.get('_user', None)
        kwargs['props'] = {'user': user_data}
        return func(**kwargs)
    return wrapper

         

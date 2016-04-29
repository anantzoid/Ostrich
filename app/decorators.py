from threading import Thread

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def user_session(func):
    def wrapper():
        user_data = session.get('_user', None)
        props = {'user': user_data}
        return func(props)
    return wrapper




from threading import Thread
from functools import wraps
from flask import session, request
from app import webapp

def async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def user_session(func):
    @wraps(func)
    def wrapper(**kwargs):
        from app.models import Utils
        if Utils.getParam(request.args, 'session', default=None):
            user_data = session.get('_user', None)
            if user_data and user_data['user_id'] in Utils.getAdmins():
                session.clear()

        user_data = session.get('_user', None)
        kwargs['props'] = {'user': user_data,
                            'cdn': webapp.config['S3_HOST']+'website/'}
        kwargs['store'] = {'cdn': webapp.config['S3_HOST']+'website/'}
        return func(**kwargs)
    return wrapper

def is_user(func):
    @wraps(func)
    def wrapper(**kwargs):
        from app.models import Utils
        #TODO move it to check app version or some other reliable source
        user_data = session.get('_user', None)
        if (Utils.getParam(request.form, 'ref') == 'web' and
                (user_data is None or
                    (user_data and user_data['user_id'] != Utils.getParam(request.form, 'user_id', 'int')))):
                        return Utils.errorResponse({'status': 'false'}, 'HTTP_STATUS_CODE_CLIENT_ERROR')
        return func(**kwargs)
    return wrapper

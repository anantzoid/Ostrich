from celery import Celery

def createCeleryApp(webapp):
    celery = Celery(__name__, broker=webapp.config['CELERY_BROKER_URL'])
    celery.conf.update(webapp.config)
    Taskbase = celery.Task

    class ContextTask(Taskbase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with webapp.app_context():
                return Taskbase.__call__(self, *args, **kwargs)
    
    celery.Task = ContextTask
    return celery




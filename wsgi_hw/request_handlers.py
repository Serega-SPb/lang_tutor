import datetime

from wsgi_app import add_url_handler


@add_url_handler('/', 'index')
def index(env, context):
    context['Time'] = datetime.datetime.now().time()


@add_url_handler('/about', 'about')
def about(env, context):
    context['Author'] = 'Serega'
    context['Project'] = 'Test project'


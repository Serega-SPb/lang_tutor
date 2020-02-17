from urls import Url
from template_manager import get_page


NOT_FOUND = '<h1> 404 Not Found </h1>'
ERROR = '<h1> 500 Server Error </h1>'


class Status:
    OK = '200 OK'
    NOT_FOUND = '404 Not Found'
    ERROR = '500 Server Error'


def add_url_handler(path, name):
    def wrapper(func):
        Application.urls.append(Url(path, func, name))
        return func
    return wrapper


class Application:

    urls = []

    def __init__(self):
        # import and load urls
        from request_handlers import index, about

    def __call__(self, environ, start_response):

        status = Status.OK
        page = f'<b>Test</b>'
        context = {}

        path = environ['PATH_INFO']
        print(path)
        try:
            url = [u for u in self.urls if u.path == path].pop()
            url(environ, context)
            page = get_page(url.name, context)
            if page is None:
                raise Exception
        except IndexError:
            status = Status.NOT_FOUND
            page = NOT_FOUND
        except Exception as e:
            print(e)
            status = Status.ERROR
            page = ERROR

        start_response(status, [('Content-Type', 'text/html')])
        return iter([page.encode('utf-8')])


def app(environ, start_response):
    return Application()(environ, start_response)


application = Application()

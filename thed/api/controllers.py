from __future__ import unicode_literals
import inspect

from pyramid.view import view_defaults


class Controller(object):
    def __init__(self, context, request):
        super(Controller, self).__init__()
        self.request = request
        self.context = context


class RestController(Controller):
    registry = {}

    @classmethod
    def register(cls, name, **kwargs):

        base_methods = inspect.getmembers(cls, predicate=inspect.ismethod)
        to_exclude = [name for name, _ in base_methods]

        def wrapped(controller):
            cls.registry[name] = controller
            controller = view_defaults(**kwargs)(controller)
            methods = inspect.getmembers(controller, predicate=inspect.ismethod)
            views = [
                (method_name, impl)
                for method_name, impl in methods
                if not method_name.startswith('_')
                and method_name not in to_exclude
            ]
            print views
            # TODO: dynamically register these views with pyramid
            return controller

        return wrapped

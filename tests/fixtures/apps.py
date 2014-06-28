from __future__ import unicode_literals

from pyramid.view import view_config

from thed import api


@api.Resource.nest('foo')
class FooResource(api.Resource):
    pass


@api.RestController.register('foo', context=FooResource)
class FooController(api.RestController):
    @view_config(name='')
    def index(self):
        return api.Response('index foo')

    def show(self, resource_id):
        return api.Response('show foo')

    def undecorated(self):
        pass


@FooResource.nest('bar')
class BarResource(api.Resource):
    pass


@api.RestController.register('bar', context=BarResource)
class BarController(FooController):
    @view_config(name='baz')
    def baz(self):
        return api.Response('index bar')

    @view_config(name='')
    def index(self):
        return api.Response('index bar')


def create(**overrides):
    return api.Application.create(
        {},
        includes=['thed.api.resources'],
        **overrides
    )


def create_integration_app(**overrides):
    def hook(config):
        config.scan()
        print api.RestController.registry
        for resource, controller in api.RestController.registry.iteritems():
            # print resource, controller
            # controller.__view_defaults__.update({'context': context})
            # TODO: dynamically hook up app here...
            pass
            # for name, handler, verb in controller.handlers:
            #     pass

            # for (route, verb), (method, url) in api.RestController.registry:
            #     config.add_route(route, url, request_method=verb)
            #     config.add_view(
            #         method.im_class,
            #         attr=method.im_func.__name__,
            #         route_name=route,
            #         permission=route
            #     )

    return create(hook=hook, **overrides)

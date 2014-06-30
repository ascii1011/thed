from __future__ import unicode_literals

from thed import api

import sample



def create(**overrides):
    return api.Application.create(
        {},
        includes=['thed.api.resources'],
        **overrides
    )


def create_integration_app(**overrides):
    def hook(config):
        config.add_view_predicate('resource', sample.ResourcePredicate)
        config.scan()

        print api.RestController.registry

        # TODO: dynamically hook up app here...
        for resource, controller in api.RestController.registry.iteritems():
            # print resource, controller
            # controller.__view_defaults__.update({'context': context})
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

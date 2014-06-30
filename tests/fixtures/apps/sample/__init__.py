from __future__ import unicode_literals

from pyramid.view import view_config

from thed import api


class ResourcePredicate(object):
    """
    """

    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'val=%s' % (self.val,)

    phash = text

    def __call__(self, context, request):
        return context.entity and isinstance(context.entity, self.val)


class TestModel(object):

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


class SubModel(object):

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


@api.Resource.nest('foo')
class FooResource(api.DBModelBackedResource):

    model_cls = TestModel

    def lookup(self, key):
        if key == 'resource_id':
            return self.model_cls()


@api.RestController.register('foo', context=FooResource)
class FooController(api.RestController):

    @view_config(name='')
    def index(self):
        return api.Response('foo.index')

    @view_config(resource=FooResource.model_cls)
    def show(self):
        return api.Response(str(self.context.entity))


@FooResource.nest('bar')
class BarResource(api.Resource):
    pass


@api.RestController.register('bar', context=BarResource)
class BarController(FooController):

    @view_config(name='baz')
    def baz(self):
        return api.Response('baz.index')

    @view_config(name='')
    def index(self):
        return api.Response('bar.index')


@BarResource.nest('qux')
class QuxResource(api.Resource):
    pass


@api.RestController.register('qux', context=QuxResource)
class QuxController(FooController):

    @view_config(name='')
    def index(self):
        return api.Response('qux.index')


@FooResource.nest('sub')
class SubResource(api.DBModelBackedResource):

    model_cls = SubModel

    def lookup(self, key):
        if key == 'sub_id':
            return self.model_cls()


@api.RestController.register('sub', context=SubResource)
class SubController(FooController):

    @view_config(name='')
    def index(self):
        return api.Response('sub.index')

    @view_config(resource=SubResource.model_cls)
    def show(self):
        return api.Response(
            '{}{}'.format(
                self.context.entity, self.context.parent.parent.entity
            )
        )

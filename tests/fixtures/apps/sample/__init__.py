from __future__ import unicode_literals

from pyramid.view import view_config

from thed import api


class TestModel(object):

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


class SubModel(object):

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


@api.Resource.nest('foo')
class FooResource(api.ModelBackedResource):

    model_cls = TestModel

    def lookup(self, key):
        # in the real world this would be `self.model_cls.query.get(key).one()`
        if key == 'resource_id':
            return self.model_cls()


@api.RestController.register('foo', context=FooResource)
class FooController(api.RestController):

    def index(self):
        return api.Response('foo.index')

    def show(self):
        return api.Response(str(self.context.entity))

    def create(self):
        return api.Response('foo.created')

    def update(self):
        return api.Response('foo.updated')

    def delete(self):
        return api.Response('foo.deleted')


@FooResource.nest('bar')
class BarResource(api.Resource):
    pass


@api.RestController.register('bar', context=BarResource)
class BarController(api.RestController):

    # a custom route
    @view_config(name='baz')
    def baz(self):
        return api.Response('baz.index')

    def index(self):
        return api.Response('bar.index')


@BarResource.nest('qux')
class QuxResource(api.Resource):
    pass


@api.RestController.register('qux', context=QuxResource)
class QuxController(api.RestController):

    def index(self):
        return api.Response('qux.index')


@FooResource.nest('sub')
class SubResource(api.ModelBackedResource):

    model_cls = SubModel

    def lookup(self, key):
        # in the real world this would be `self.model_cls.query.get(key).one()`
        if key == 'sub_id':
            return self.model_cls()


@api.RestController.register('sub', context=SubResource)
class SubController(FooController):

    def index(self):
        return api.Response('sub.index')

    def show(self):
        return api.Response(
            '{}{}'.format(
                self.context.entity, self.context.parent.parent.entity
            )
        )

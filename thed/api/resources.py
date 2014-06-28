from __future__ import unicode_literals
import logging


logger = logging.getLogger(__name__)


class Resource(object):
    endpoint_map = {}

    def __init__(self, request, parent=None, name=None, entity=None):
        self.__name__ = name
        self.__parent__ = parent
        self.request = request
        self.entity = entity

    @classmethod
    def nest(cls, key):
        def wrapped(nested_cls):
            if key in cls.endpoint_map:
                logger.warning(
                    '%s already registered with %s', key,
                    cls.endpoint_map[key]
                )
            cls.endpoint_map[key] = nested_cls
            return nested_cls

        return wrapped

    def _lookup_endpoint_from_map(self, key):
        return self.endpoint_map[key]

    def _create_context_instance(self, cls, key, entity=None):
        if cls is not None:
            return cls(
                request=self.request, parent=self, name=key, entity=entity
            )

    def __getitem__(self, key):
        import ipdb; ipdb.set_trace()
        ctx_cls = self._lookup_endpoint_from_map(key)
        return self._create_context_instance(ctx_cls, key)


class DBModelBackedResource(Resource):
    model_cls = None
    ctx_cls = None

    def lookup(self, key):
        return self.model_cls.query.get(key).one()

    def __getitem__(self, key):
        model = self.lookup(key)
        if not model:
            return super(DBModelBackedResource, self).__getitem__(key)
        return self._create_context_instance(self.ctx_cls, key, entity=model)


def includeme(config):
    config.set_root_factory(Resource)

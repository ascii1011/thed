from __future__ import unicode_literals

from thed import api

import sample


def create(**overrides):
    return api.Application.create(
        {},
        includes=['thed.api.resources', 'thed.api.controllers'],
        **overrides
    )


def create_integration_app(**overrides):
    def hook(config):
        config.add_view_predicate('resource', api.predicates.ResourcePredicate)
        config.scan()

    return create(hook=hook, **overrides)

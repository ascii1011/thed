from __future__ import unicode_literals

from tests.integration import IntegrationTestCase


class APITestCase(IntegrationTestCase):

    def test_it(self):
        self.app.get('/foo/bar/baz')
        self.app.get('/foo/bar')
        self.app.get('/foo')
        self.app.get('/foo/dynamic')



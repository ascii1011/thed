from __future__ import unicode_literals

from tests.integration import IntegrationTestCase


class APITestCase(IntegrationTestCase):

    def test_it(self):
        for url, expected in (
            ('/foo', 'foo.index'),
            ('/foo/bar', 'bar.index'),
            ('/foo/bar/baz', 'baz.index'),
            ('/foo/bar/qux', 'qux.index'),
            ('/foo/resource_id', '<TestModel>'),
            ('/foo/resource_id/sub', 'sub.index'),
            ('/foo/resource_id/sub/sub_id', '<SubModel><TestModel>'),
        ):
            resp = self.app.get(url)
            self.assertEqual(resp.text, expected)

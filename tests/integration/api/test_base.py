from __future__ import unicode_literals

from tests.integration import IntegrationTestCase


class APITestCase(IntegrationTestCase):

    def test_nested_gets(self):
        """
        Tests various levels of nesting and resource lookup
        """
        for url, expected in (
            ('/foo', 'foo.index'),
            ('/foo/bar', 'bar.index'),
            ('/foo/bar/baz', 'baz.index'),
            ('/foo/bar/qux', 'qux.index'),
            ('/foo/resource_id', '<TestModel>'),
            ('/foo/resource_id/sub', 'sub.index'),
            ('/foo/resource_id/sub/sub_id', '<SubModel><TestModel>'),
            # ('/foo/resource_id/sub/sub_id/bar/baz', 'baz.index'),
        ):
            resp = self.app.get(url)
            self.assertEqual(resp.text, expected)

    def test_other_operations(self):
        for url, expected, op in (
            ('/foo', 'foo.created', self.app.post),
            ('/foo/resource_id', 'foo.updated', self.app.put),
            ('/foo/resource_id', 'foo.deleted', self.app.delete),
        ):
            resp = op(url)
            self.assertEqual(resp.text, expected)

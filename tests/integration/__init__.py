from __future__ import unicode_literals
import logging

from webtest import TestApp

from thed import db, models

from tests import TestCase, fixtures


logger = logging.getLogger(__name__)


class IntegrationTestCase(TestCase):

    settings = {
        'sqlalchemy.url': 'sqlite://'
    }

    @classmethod
    def setUpClass(cls):
        super(IntegrationTestCase, cls).setUpClass()
        settings = cls.settings

        db.init(settings)
        models.init(settings)

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        app = fixtures.apps.create_integration_app(**self.settings)
        self.app = TestApp(app)
        self.app.session = self.settings['session']

    def tearDown(self):
        self.app.session.bind.dispose()

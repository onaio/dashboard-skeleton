import os
import unittest
import transaction

from webob.multidict import MultiDict
from pyramid.registry import Registry
from pyramid import testing
from pyramid.paster import (
    get_appsettings
)
from pyramid.security import IAuthenticationPolicy
from sqlalchemy import engine_from_config
from webtest import TestApp

from dashboard import main
from dashboard.models.base import (
    DBSession,
    Base)


SETTINGS_FILE = 'test.ini'
settings = get_appsettings(SETTINGS_FILE)
engine = engine_from_config(settings, 'sqlalchemy.')


class TestBase(unittest.TestCase):
    def setUp(self):
        registry = Registry()
        registry.settings = settings
        self.config = testing.setUp(registry=registry)
        # setup db
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine
        Base.metadata.drop_all()
        Base.metadata.create_all()
        # setup request
        self.request = testing.DummyRequest()

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()


class IntegrationTestBase(TestBase):
    def setUp(self):
        super(IntegrationTestBase, self).setUp()
        self.config.include('dashboard')


class FunctionalTestBase(IntegrationTestBase):
    def _login_user(self, userid):
        policy = self.testapp.app.registry.queryUtility(IAuthenticationPolicy)
        headers = policy.remember(self.request, userid)
        cookie_parts = dict(headers)['Set-Cookie'].split('; ')
        cookie = filter(
            lambda i: i.split('=')[0] == 'auth_tkt', cookie_parts)[0]
        return {'Cookie': cookie}

    def setUp(self):
        super(FunctionalTestBase, self).setUp()
        current_dir = os.getcwd()
        app = main(
            {
                '__file__': os.path.join(current_dir, SETTINGS_FILE),
                'here': current_dir
            },
            **settings)
        self.testapp = TestApp(app)
        self.request = testing.DummyRequest()
        self.request.environ = {
            'SERVER_NAME': 'example.com',
        }
import logging.config

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config

from dashboard.libs.utils import format_date, format_time
from dashboard.security import group_finder, pwd_context
from dashboard.models.base import (
    DBSession,
    Base,
    )
from dashboard.libs.submission_handler import (
    submission_handler_manager)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    session_factory = UnencryptedCookieSessionFactoryConfig(
        settings['secret_key'])
    config = Configurator(settings=settings,
                          root_factory='dashboard.models.base.BaseRootFactory',
                          session_factory=session_factory)
    config.set_authentication_policy(
        AuthTktAuthenticationPolicy(settings['secret_key'],
                                    callback=group_finder,
                                    hashalg='sha512'))

    config.set_authorization_policy(ACLAuthorizationPolicy())

    logging.config.fileConfig(
        global_config['__file__'], disable_existing_loggers=False)

    # configure password context
    pwd_context.load_path(global_config['__file__'])

    includeme(config)
    return config.make_wsgi_app()


def includeme(config):
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("dashboard:templates")
    config.commit()  # commit to allow access to jinja environment
    config.get_jinja2_environment().filters['format_date'] = format_date
    config.get_jinja2_environment().filters['format_time'] = format_time
    config.add_static_view('static', 'dashboard:static', cache_max_age=3600)
    config.add_route('default', '/')
    config.add_route(
        'submissions', '/submissions/*traverse')
    config.scan()

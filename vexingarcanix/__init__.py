
from pyramid_beaker import session_factory_from_settings
from pyramid.config import Configurator
# from pyramid.session import UnencryptedCookieSessionFactoryConfig
# my_session_factory = UnencryptedCookieSessionFactoryConfig('not-really-secret')

""" The docs have a charming parallel to the way `apt-get remove perl` used to
    make you type out 'I know that what I am doing is wrong':

    > Note the very long, very explicit name for
    > UnencryptedCookieSessionFactoryConfig. It's trying to tell you that this
    > implementation is, by default, *unencrypted*. You should not use it when
    > you keep sensitive information in the session object, as the information
    > can be easily read by both users of your application and third parties
    > who have access to your users' network traffic. Use a different session
    > factory implementation (preferably one which keeps session data on the
    > server) for anything but the most basic of applications where "session
    > security doesn't matter".
"""

from sqlalchemy import engine_from_config
from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)
    # config = Configurator(session_factory=my_session_factory, settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    # "Show me your deck list."
    config.add_route('give_deck', '/')
    # "Did I parse your deck list correctly?"
    config.add_route('check_deck', '/check')
    # "Okay, I'm asking you questions about your deck."
    config.add_route('show_question', '/ask')
    # "This is my answer to the question."
    config.add_route('check_answer', '/answer')
    # /answer should be POSTed to, and leads back to /ask with a flash message
    # telling you whether you were right or wrong.

    config.scan()
    return config.make_wsgi_app()

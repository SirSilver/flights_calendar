from aiohttp import web
from aiohttp_cache import setup_cache
from views import index


def create_app():
    app = web.Application()
    app.add_routes([web.get('/', index)])
    setup_cache(app)

    return app

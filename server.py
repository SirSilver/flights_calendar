from aiohttp import web
from aiohttp_cache import cache
from app import create_app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)

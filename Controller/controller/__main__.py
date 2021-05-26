from aiohttp import web

from controller.app import app


web.run_app(app, host='0.0.0.0', port=8087, access_log=None)

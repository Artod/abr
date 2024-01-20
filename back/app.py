import os
import aiohttp_cors

from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers

async def on_startup(app):
    # Setup default CORS settings
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["GET", "POST", "OPTIONS"]
        )
    })

    # Add CORS to all resources
    for resource in app.router.resources():
        cors.add(resource)

def run() -> None:
    """
    Entry point of the application.
    """

    app = web.Application()
    app.on_startup.append(on_startup)

    web.run_app(
        register_graphql_handlers(
            app=app,
            # engine_sdl=os.path.dirname(os.path.abspath(__file__)) + "/sdl",
            engine_sdl=f"{os.path.dirname(os.path.abspath(__file__))}/sdl",
            engine_modules=[
                "app.snippet_web",
                "app.query_resolvers"
            ],
            executor_http_endpoint="/graphql",
            executor_http_methods=["POST"],
            graphiql_enabled=True,
        )
    )
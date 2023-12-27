from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routers import game


def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(game.router)

    app.mount("/", StaticFiles(directory="frontend/dist/", html=True), name="static")

    @app.get("/")
    def index():
        return app.send_static_file("index.html")

    return app


app = create_app()

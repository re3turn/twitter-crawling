from fastapi import FastAPI

from src.routers import router as api_router


def init_application():
    fast_api = FastAPI()

    fast_api.include_router(api_router)

    return fast_api


app = init_application()

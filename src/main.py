from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic.error_wrappers import ValidationError

from src.exception_handlers import validation_error_handler
from src.utils.openapi import CustomOpenAPIGenerator
from src.frontend.routers import router as frontend_router
from src.auth.routers import router as auth_router


def get_app() -> FastAPI:
    app = FastAPI()
    app.title = 'Client that uses external service for authentication by graphical password'
    app.description = ''
    app.version = '1.0.0'
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.include_router(router=frontend_router)
    app.include_router(router=auth_router, prefix='/api/v1')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['https://gp-auth-ru'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.openapi = CustomOpenAPIGenerator(app)
    return app


app = get_app()

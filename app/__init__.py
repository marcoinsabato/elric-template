from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.exceptions import global_exception_handler
from app.middleware.api_key import ApiKeyMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.providers.database import init_db
from app.providers.langsmith import init_langsmith
from app.providers.redis import close_redis, init_redis
from app.routes import health, test_errors
from config.logging import configure_logging
from config.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await init_db()
    await init_redis()
    init_langsmith()
    yield
    await close_redis()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Elric App",
        lifespan=lifespan,
        docs_url="/docs" if settings.APP_DEBUG else None,
    )

    app.add_middleware(ApiKeyMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(LoggingMiddleware)

    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(RequestValidationError, global_exception_handler)

    app.include_router(health.router)
    app.include_router(test_errors.router)

    return app

import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from config.logging import set_trace_id


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        set_trace_id(trace_id)
        request.state.trace_id = trace_id

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(trace_id=trace_id)

        logger = structlog.get_logger()

        start_time = time.time()

        logger.info(
            "request.started",
            method=request.method,
            path=request.url.path,
            client_host=request.client.host if request.client else None,
        )

        response: Response = await call_next(request)

        duration_ms = int((time.time() - start_time) * 1000)

        logger.info(
            "request.completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        response.headers["X-Trace-ID"] = trace_id

        return response

import structlog
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.responses import JSONResponse

from app.exceptions.base import ElricException
from config.logging import trace_id_var

logger = structlog.get_logger()


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler that catches all exceptions and returns
    a uniform JSON response with trace_id for debugging.
    """
    trace_id = trace_id_var.get(None)

    if isinstance(exc, ElricException):
        logger.error(
            "elric_exception",
            error_code=exc.error_code,
            message=exc.message,
            status_code=exc.status_code,
            details=exc.details,
            trace_id=trace_id,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_code,
                "message": exc.message,
                "trace_id": trace_id,
                "code": exc.status_code,
                **({"details": exc.details} if exc.details else {}),
            },
        )

    if isinstance(exc, HTTPException):
        logger.warning(
            "http_exception",
            status_code=exc.status_code,
            detail=exc.detail,
            trace_id=trace_id,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "http_error",
                "message": str(exc.detail),
                "trace_id": trace_id,
                "code": exc.status_code,
            },
        )

    if isinstance(exc, RequestValidationError):
        logger.warning(
            "validation_error",
            errors=exc.errors(),
            trace_id=trace_id,
        )
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error",
                "message": "Request validation failed",
                "trace_id": trace_id,
                "code": 422,
                "details": {"errors": exc.errors()},
            },
        )

    logger.error(
        "unhandled_exception",
        exception_type=type(exc).__name__,
        exception_message=str(exc),
        trace_id=trace_id,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "An unexpected error occurred",
            "trace_id": trace_id,
            "code": 500,
        },
    )

from typing import Any, Optional


class ElricException(Exception):
    """Base exception class for all Elric framework exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "internal_error",
        details: Optional[dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(ElricException):
    """Raised when request validation fails."""

    def __init__(
        self,
        message: str = "Validation failed",
        error_code: str = "validation_error",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=422,
            error_code=error_code,
            details=details,
        )


class AuthException(ElricException):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: str = "auth_error",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=401,
            error_code=error_code,
            details=details,
        )


class ForbiddenException(ElricException):
    """Raised when user lacks permission for the requested resource."""

    def __init__(
        self,
        message: str = "Access forbidden",
        error_code: str = "forbidden",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=403,
            error_code=error_code,
            details=details,
        )


class NotFoundException(ElricException):
    """Raised when a requested resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str = "not_found",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=404,
            error_code=error_code,
            details=details,
        )


class RateLimitException(ElricException):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        error_code: str = "rate_limit_exceeded",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=429,
            error_code=error_code,
            details=details,
        )


class AgentException(ElricException):
    """Raised when an agent execution fails."""

    def __init__(
        self,
        message: str = "Agent execution failed",
        error_code: str = "agent_failed",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code=error_code,
            details=details,
        )


class DatabaseException(ElricException):
    """Raised when a database operation fails."""

    def __init__(
        self,
        message: str = "Database operation failed",
        error_code: str = "database_error",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=503,
            error_code=error_code,
            details=details,
        )


class ExternalServiceException(ElricException):
    """Raised when an external service call fails."""

    def __init__(
        self,
        message: str = "External service unavailable",
        error_code: str = "external_service_error",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=502,
            error_code=error_code,
            details=details,
        )

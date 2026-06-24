from fastapi import APIRouter

from app.exceptions import (
    AgentException,
    AuthException,
    DatabaseException,
    ExternalServiceException,
    ForbiddenException,
    NotFoundException,
    RateLimitException,
    ValidationException,
)

router = APIRouter(prefix="/test-errors", tags=["test"])


@router.get("/validation")
async def test_validation_error():
    """Test ValidationException (422)"""
    raise ValidationException(
        message="Invalid input data",
        details={"field": "email", "error": "Invalid email format"},
    )


@router.get("/auth")
async def test_auth_error():
    """Test AuthException (401)"""
    raise AuthException(message="Invalid credentials")


@router.get("/forbidden")
async def test_forbidden_error():
    """Test ForbiddenException (403)"""
    raise ForbiddenException(message="You don't have permission to access this resource")


@router.get("/not-found")
async def test_not_found_error():
    """Test NotFoundException (404)"""
    raise NotFoundException(message="User not found", details={"user_id": "123"})


@router.get("/rate-limit")
async def test_rate_limit_error():
    """Test RateLimitException (429)"""
    raise RateLimitException(
        message="Too many requests",
        details={"retry_after": 60},
    )


@router.get("/agent")
async def test_agent_error():
    """Test AgentException (500)"""
    raise AgentException(
        message="Agent execution failed",
        details={"agent": "ExampleAgent", "step": "process"},
    )


@router.get("/database")
async def test_database_error():
    """Test DatabaseException (503)"""
    raise DatabaseException(message="Database connection failed")


@router.get("/external-service")
async def test_external_service_error():
    """Test ExternalServiceException (502)"""
    raise ExternalServiceException(
        message="OpenAI API unavailable",
        details={"service": "openai"},
    )


@router.get("/generic")
async def test_generic_error():
    """Test generic Python exception (500)"""
    raise ValueError("This is a generic Python exception")


@router.get("/zero-division")
async def test_zero_division():
    """Test ZeroDivisionError (500)"""
    result = 1 / 0
    return {"result": result}

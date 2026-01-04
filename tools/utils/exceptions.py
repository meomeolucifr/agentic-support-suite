"""Custom exceptions."""


class SupportSystemException(Exception):
    """Base exception for support system."""
    pass


class AgentException(SupportSystemException):
    """Exception raised by agents."""
    pass


class DatabaseException(SupportSystemException):
    """Database-related exception."""
    pass


class LLMException(SupportSystemException):
    """LLM provider exception."""
    pass


class VectorDBException(SupportSystemException):
    """Vector database exception."""
    pass


class IntegrationException(SupportSystemException):
    """Integration exception."""
    pass




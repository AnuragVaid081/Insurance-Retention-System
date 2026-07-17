class LLMServiceError(Exception):
    """Base exception for all LLM service errors."""


class LLMConnectionError(LLMServiceError):
    """Raised when Ollama cannot be reached."""


class LLMTimeoutError(LLMServiceError):
    """Raised when the LLM request times out."""


class LLMResponseError(LLMServiceError):
    """Raised when the LLM returns an invalid response."""
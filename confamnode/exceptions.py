class ConfamNodeError(Exception):
    """Base error for all ConfamNode errors"""
    def __init__(self, message: str = "An error occured"):
        super().__init__(message)


class ConfamAuthError(ConfamNodeError):
    """Raised when API key is invalid"""
    def __init__(self, message: str = "Invalid ConfamNode API key format"):
        super().__init__(message)


class ConfamRateLimitError(ConfamNodeError):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str = "You don reach your free limit. To upgrade your plan, contact us at confamnode@gmail.com"):
        super().__init__(message)


class ConfamModelError(ConfamNodeError):
    """Raised when an invalid model name is used"""
    def __init__(self, model_name: str):
        super().__init__(f"Invalid model name: {model_name}")


class ConfamInsufficientBalanceError(ConfamNodeError):
    """Raised when the wallet balance is too low for requested model (HTTP 402)"""
    def __init__(self, message: str = "Insufficient wallet balance. Top up to continue using paid models."):
        super().__init__(message)


class ConfamProviderError(ConfamNodeError):
    """Raised when the upstream provider is unreachable or fails (HTTP 502/504)"""
    def __init__(self, message: str = "The AI provider is temporarily unavailable. Please try again."):
        super().__init__(message)


class ConfamRequestError(ConfamNodeError):
    """Raised for other client-side request errors (HTTP 400/422/other 4xx)"""
    def __init__(self, message: str = "Your request could not be processed."):
        super().__init__(message)
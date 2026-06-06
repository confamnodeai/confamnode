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

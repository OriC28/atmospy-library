
class MissingAPIKeyError(Exception):
    def __init__(self, message="API key is missing."):
        super().__init__(message)


class MissingParamsError(Exception):
    def __init__(self, message="Missing parameters for the request."):
        super().__init__(message)


class APIRequestError(Exception):
    def __init__(self, status_code: int, message="An error occurred while making the API request."):
        super().__init__(f"Error {status_code}: {message}")
        self.status_code = status_code

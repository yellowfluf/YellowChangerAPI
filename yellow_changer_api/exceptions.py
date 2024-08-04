

class BadRequest(Exception):
    """Exception raised for invalid requests."""

    def __init__(self, message: str = "Bad request"):
        self.message = message
        super().__init__(self.message)
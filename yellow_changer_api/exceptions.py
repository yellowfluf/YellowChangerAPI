class BadRequest(Exception):
    """Exception raised for invalid requests."""

    def __init__(self, message: str = "Bad request"):
        self.message = message
        super().__init__(self.message)


class UnsupportedBank(Exception):
    """Exception raised if the bank is not supported."""

    def __init__(self, message: str = "Bank is not supported"):
        self.message = message
        super().__init__(self.message)


class UnsupportedMemo(Exception):
    """Exception raised if the memo is not supported for coin."""

    def __init__(self, message: str = "Memo is not supported for this coin"):
        self.message = message
        super().__init__(self.message)

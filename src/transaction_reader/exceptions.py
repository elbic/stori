class TransactionReaderError(Exception):
    """Base class for all transaction-reader-related errors."""


class TransactionReaderFileError(TransactionReaderError):
    """Raised when there is an error trying to read the file."""

    def __init__(self, message, **kwargs):
        self.messages = (
            [message] if isinstance(message, (str, bytes)) else message
        )
        self.kwargs = kwargs
        super().__init__(message)

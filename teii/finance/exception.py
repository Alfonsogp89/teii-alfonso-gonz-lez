""" Exception classes """


class FinanceClientError(Exception):
    """
    Base class for finance client exceptions.

    Source:
        https://www.loggly.com/blog/exceptional-logging-of-exceptions-in-python/
    """

    pass


class FinanceClientInvalidAPIKey(FinanceClientError):
    """
    Invalid finance API Key.
    """

    pass


class FinanceClientAPIError(FinanceClientError):
    """
    Finance API access failure.
    """

    pass


class FinanceClientInvalidData(FinanceClientError):
    """
    Finance API returned incomplete or malformed data.
    """

    pass


class FinanceClientIOError(FinanceClientError):
    """
    Error reading or writing data file.
    """

    pass


class FinanceClientParamError(FinanceClientError):
    """
    Invalid parameter provided to finance client.
    """

    pass

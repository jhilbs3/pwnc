class PWNCException(Exception):
    """
    Base exception class for pwnc.
    """
    pass

class PWNCResponseError(PWNCException):
    """
    Exception raised for responses that are not expected when received from a
    urllib3 query.
    """
    pass

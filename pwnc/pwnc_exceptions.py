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


class PWNCTypeError(PWNCException):
    """
    Exception raised when the type of an object is not compatible with an
    action
    """
    pass


class PWNCArgumentError(PWNCException):
    """
    Exception when the arguments passed to a method are either the wrong type
    or no enough arguments are passed.
    """
    pass

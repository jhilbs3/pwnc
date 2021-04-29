class PWNCException(Exception):
    """ Base exception class for pwnc. """

    pass


class PWNCResponseError(PWNCException):
    """ Raised when a urllib3 response is unexpected """

    pass


class PWNCTypeError(PWNCException):
    """ Raised when the type of an object is unexpected """

    pass


class PWNCArgumentError(PWNCException):
    """ Raised when an arg is the wrong type or too few args were passed """

    pass


class PWNCSymbolError(PWNCException):
    """ Raised when a symbol is not found or otherwise unexpected """

    pass

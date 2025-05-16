
class SkipException(Exception):
    """
    Exception raised when item should be skipped
    """
    pass

class InvalidResponseException(Exception):
    """
    Exception raised when received unexpected response status code
    """
    pass

class UnsupportedOptionCombination(Exception):
    """
    Exception raised when an unsupported combination of command options is used
    """
    pass

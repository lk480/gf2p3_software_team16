class MyException(Exception):
    """My exception is class that inherits properties from the Exception class.
    All of our syntax and semantic error build upon MyException.
    
    The attributes are:
    
    row: shows in which row the error ocured in .txt file
    col: shows in which column the error ocured in .txt file
    """

    def __init__(self, *args):
        """
        *args: list of arguments passed to Exception."""

        super().__init__(*args)
        self.row = None
        self.col = None
    
    def get_error_name(self):
        """Returns the error name."""
        return type(self).__name__

    def set_error_position(self):
        """Set the row and column at which the error occured."""
        # TODO: Need to figure out how to do this
        pass


# Syntax Errors


class MissingPunctuationError(MyException):
    """Error is raised when a punctuation is missing."""

class KeywordError(MyException):
    """Error is raised when a KEYWORD e.g. DEVICE is missing."""

class DefinitionError(MyException):
    """Error is raised when a device is incorrectly defined."""

class DeviceNameError(MyException):
    """Error is raised when a device name is defined incorrectly."""

class DeviceTypeError(MyException):
    """Error is raised when an unknown device type is specified."""



# Semantic Errors

class ConnectError(MyException):
    """Error is raised when in a CONNECT the first param is a device input
    and the second is a device output. It should be the other way round.
    """

class ReferenceError(MyException):
    """Error is raised when component is referenced before asignment."""

class InputPinNumberError(MyException):
    """Error is raised when the number of input pins exceeds maximum number of
    defined device inputs, or when input pin refernced is negative.
    """

class PortReferenceError(MyException):
    """Error is raised when referenced port does not exist."""

class DevicePropertyError(MyException):
    """Error is raised when device property is incorrectly defined."""

class MonitorError(MyException):
    """Error raised when system input cannot be monitored."""

class DeviceExistsError(MyException):
    """Error raised when device already exists."""

class MissingParameterError(MyException):
    """Error raised when insufficient parameters are defined when creating a DEVICE."""

class KeywordNameError(MyException):
    """Error raised when a keyword is used for device name."""

class MultipleInputError(MyException):
    """Error raised when multiple outputs connect to a single input port."""







class ErrorHandler:
    """Used to store all errors that ocur when parsing.
    Each error is an instance of MyException.
    """

    def __init__(self):
        """Initiale an empty list of MyException instances."""
        self.error_list: list[MyException] = []

    def __call__(self, error: MyException):
        """Adds an error to error_list."""
        self.error_list.append(error)
    
    def found_no_errors(self):
        """True if parser didn't find any errors."""
        return not self.error_list
    
    def print_all_errors(self):
        """Print all errors found by parser."""

        for i, error in enumerate(self.error_list):
            print(f'Error number {i} in ErrorHandler().error_list is: {error.get_error_name}\n')

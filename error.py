from scanner import Scanner


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
        self.error_row = None
        self.error_col = None

    def get_error_name(self):
        """Returns the error name."""
        return type(self).__name__

    def set_error_position(self, scanner: Scanner):
        """Set the row and column at which the error occured."""
        # TODO: Need to figure out how to do this

        self.error_row = scanner.start_of_symbol_row
        self.error_col = scanner.start_of_symbol_col


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
    """Error raised when system input cannot be monitored or no monitor is declared."""


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

    def print_all_errors(self, scanner: Scanner):
        """Print all errors found by parser."""
        path = scanner.path

        try:
            input_file = open(path, "r")
        except IOError:
            raise FileNotFoundError(
                "Cannot find file or read data in print_all_errors in error.py."
            )

        lines = [line.replace("\n", " ") for line in input_file.readlines()] + [""]
        # print(lines)

        for i, error in enumerate(self.error_list):
            print(
                f"Error number {i} in ErrorHandler().error_list is: {error.get_error_name}\n",
                f"{lines[error.error_row]}\n",
                f"{' ' * error.error_col}^\n"
            )

    def print_error(self, scanner: Scanner):
        """Prints the encountered error."""

        path = scanner.path

        try:
            input_file = open(path, "r")
        except IOError:
            raise FileNotFoundError(
                "Cannot find file or read data in print_all_errors in error.py."
            )

        lines = [line.replace("\n", " ") for line in input_file.readlines()] + [""]

        print(f"Error no. {len(self.error_list) - 1} in ErrorHandler().error_list is: {self.error_list[-1].get_error_name}\n",
              f"{lines[self.error_list[-1].error_row]}\n",
              f"{' ' * self.error_list[-1].error_col}^\n"
        )
    
    def raise_error(self):
        """Method raises an error at end of parsing."""

        if self.found_no_errors():
            return None
        
        raise self.error_list[0]
    
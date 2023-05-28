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


# Syntax errors


class MissingPunctuationError(MyException):
    """Error is raised when a punctuation is missing."""

# TODO

# Semantic errors:

# TODO


class Error:
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

        for error in self.error_list:
            print(error.get_error_name, '\n')
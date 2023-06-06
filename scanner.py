"""
Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes:
    Scanner - reads definition file and translates characters into symbols.
    Symbol - encapsulates a symbol and stores its properties.

names_ints = Names()
scanner_instance = Scanner(file_path, names_ints)
"""


class Symbol:
    """
    Encapsulate a symbol and store its properties.

    Parameters:
        No parameters.

    Public methods:
        No public methods.
    """

    def __init__(self):
        """Initialize symbol properties."""
        self.type = None
        self.id = None
        self.row = None
        self.col = None


class Scanner:
    """
    Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters:
        path: path to the circuit definition file.
        names: instance of the names.Names() class.

    Public methods:
        get_symbol(self): Translates the next sequence of characters into a
                          symbol and returns the symbol.

        skip_space(self): Skip whitespace characters and move to the
                            next non-whitespace character.

        advance(self): Move the marker to next symbol in the definition file

        get_number(self): Assumes the current character is a number, returns
                          the integer number and places the next non-digit
                          character in current_character.

        get_name(self): Assumes current character is a letter, returns the name
                        string and sets current_character as the next
                        non-alphanumeric character.
    """

    def __init__(self, path, names):
        """Open specified file and initialize reserved words and IDs.
        Parameters:
            path (str): Path to the circuit definition file
            names (names.Names): Instance of the names.Names() class

        Returns:
            None
        Raises:
            FileNotFoundError: If the specified file cannot be found or read

        """

        self.names = names
        self.path = path
        # Try to open and read file, otherwise raise an error
        try:
            self.input_file = open(path, "r")
        except IOError:
            raise FileNotFoundError("Cannot find file or read data")

        # Set first character as whitespace
        self.current_character = " "
        # List of keywords present in the defintion file
        self.keywords_list = [
            "DEVICE",
            "CONNECT",
            "MONITOR",
            "TYPE",
            "STATE",
            "INPUTS",
            "NONE",
        ]

        # This stores the current position of the marker in the file
        self.marker_row = 0
        self.marker_col = -1

        self.start_of_symbol_row = None
        self.start_of_symbol_col = None

        # Assign a unique number to each symbol type
        self.symbol_type_list = [
            self.COMMA,
            self.SEMICOLON,
            self.EQUALS,
            self.DOT,
            self.OPENBRACKET,
            self.CLOSEDBRACKET,
            self.KEYWORD,
            self.NUMBER,
            self.NAME,
            self.EOF,
            self.COLON,
            self.HASH,
        ] = range(12)

        [
            self.DEVICE_ID,
            self.CONNECT_ID,
            self.MONITOR_ID,
            self.TYPE_ID,
            self.STATE_ID,
            self.INPUTS_ID,
            self.NONE_ID,
        ] = self.names.lookup(self.keywords_list)

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol.

           Returns:
                Symbol: The translated symbol.

           Raises:
                None
        """
        # Instantiate Symbol Object
        symbol = Symbol()

        # Initalise marker
        self.start_of_symbol_row = self.marker_row
        self.start_of_symbol_col = self.marker_col

        # Call skip_space which returns next non-whitespace character
        self.skip_space()

        if self.current_character.isalpha():
            name_string = self.get_name()
            if name_string in self.keywords_list:
                symbol.type = self.KEYWORD
            elif name_string in self.names.names_list:
                symbol.type = self.NAME
            elif name_string.isdigit():
                symbol.type = self.NUMBER
            elif name_string.isalnum():
                symbol.type = self.NAME
            else:
                symbol.type = None

            [symbol.id] = self.names.lookup([name_string])

        elif self.current_character.isdigit():
            symbol.id = self.get_number()
            symbol.type = self.NUMBER

        elif self.current_character == "(":
            symbol.type = self.OPENBRACKET
            self.advance()
        elif self.current_character == ")":
            symbol.type = self.CLOSEDBRACKET
            self.advance()
        elif self.current_character == ",":
            symbol.type = self.COMMA
            self.advance()
        elif self.current_character == ":":
            symbol.type = self.COLON
            self.advance()
        elif self.current_character == "=":
            symbol.type = self.EQUALS
            self.advance()
        elif self.current_character == ";":
            symbol.type = self.SEMICOLON
            self.advance()
        elif self.current_character == "":
            symbol.type = self.EOF
            self.advance()
        elif self.current_character == ".":
            symbol.type = self.DOT
            self.advance()
        elif self.current_character == "#":
            symbol.type = self.HASH
            self.advance()
        else:
            self.advance()

        # Verbose outuput for debugging only:
        # print(f"Symbol id: {symbol.id}, symbol type: {symbol.type}")
        return symbol

    def advance(self):
        """Reads the next character from the definition file and
           places it in current character.

        Returns:
            str: current character in file

        Raise: None
        """
        # Advance marker column by 1
        self.marker_col += 1

        # Check if current character encounters a newline
        if self.current_character == "\n":
            # Reset marker column to zero, advance marker row
            self.marker_col = 0
            self.marker_row += 1

        self.current_character = self.input_file.read(1)
        print(self.current_character)

        return self.current_character

    def skip_space(self):
        """Sets current character to next non-whitespace character
           by repeatedly calling advance() as necessary.

           Returns:
                None
           Raises:
                None
        """
        # Check if current character is whitespace
        while self.current_character.isspace():
            # Call advance until a non-whitespace character is read
            self.current_character = self.advance()

    def get_number(self):
        """Assumes current character is a number and returns 
           the integer number and places sets current character
           to the next non-digit character.

        Returns:
            int: integer number
        Raises:
            None
        """
        # Assumes current character is the first digit of a number
        number = self.current_character
        while True:
            self.current_character = self.advance()
            # Check current character is digit
            if self.current_character.isdigit():
                # Concatenate digit with string stored in number
                number = number + self.current_character
            else:
                return number

    def get_name(self):
        """Assumes current character is a letter and returns the
           name string and sets current character to the next
           non-alphanumeric character.

        Returns:
            str: name string
        Raises:
            None
        """
        # Assumes current character is the first letter of a name
        name = self.current_character
        while True:
            self.current_character = self.advance()
            # Check current character is alphanumeric
            if self.current_character.isalnum():
                # Concatenate character with string stored in name
                name = name + self.current_character
            else:
                return name

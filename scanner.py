"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.

names_ints = Names()
scanner_instance = Scanner(file_path, names_ints)
"""


class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self):
        """Initialise symbol properties."""
        self.type = None
        self.id = None


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""
        self.names = names
        self.path = path

        try:
            self.input_file = open(path, 'r')
        except IOError:
            raise print("Cannot find file or read data")
        self.current_character = ' '
        self.keywords_list = ['NEW_DEVICES', 'CONNECT',
                              'MONITOR', 'TYPE', 'STATE', 'INPUTS']
        self.symbol_type_list = [self.COMMA, self.SEMICOLON, self.EQUALS,
                                 self.DOT, self.OPENBRACKET,
                                 self.CLOSEBRACKET, self.KEYWORD, self.NUMBER,
                                 self.NAME, self.EOF] = range(10)
        [self.NEW_DEVICES_ID,
         self.CONNECT_ID,
         self.MONITOR_ID,
         self.TYPE_ID,
         self.STATE_ID,
         self.INPUTS_ID] = self.names.lookup(self.keywords_list)

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        symbol = Symbol()
        self.skip_space()  # current character now not a whitespace
        # print('in get symbol ' + self.current_character)
        if self.current_character.isalpha():
            name_string = self.get_name()
            if name_string in self.keywords_list:
                symbol.type = self.KEYWORD
            else:
                symbol.type = self.NAME
            [symbol.id] = self.names.lookup([name_string])

        elif self.current_character.isdigit():
            symbol.id = self.get_number()
            symbol.type = self.NUMBER

        elif self.current_character == '(':
            symbol.type = self.OPENBRACKET
            self.advance()
        elif self.current_character == ')':
            symbol.type = self.CLOSEBRACKET
            self.advance()
        elif self.current_character == ',':
            symbol.type = self.COMMA
            self.advance()
        elif self.current_character == ';':
            symbol.type = self.SEMICOLON
            self.advance()
        elif self.current_character == " ":
            symbol.type = self.EOF
            self.advance()
        else:  # not a valid character
            self.advance()
        print(f"Symbol id: {symbol.id}, symbol type: {symbol.type}.")
        return symbol

    def skip_space(self):
        """Return next non-whitespace character"""
        while self.current_character.isspace():
            self.current_character = self.advance()

    def advance(self):
        self.current_character = self.input_file.read(1)
        print(self.current_character)
        return self.current_character

    def get_number(self):
        number = self.current_character
        while True:
            self.current_character = self.advance()
            if self.current_character.isdigit():
                number = number + self.current_character
            else:
                return number

    def get_name(self):
        name = self.current_character
        while True:
            self.current_character = self.advance()
            if self.current_character.isalnum():
                name = name + self.current_character
            else:
                return name

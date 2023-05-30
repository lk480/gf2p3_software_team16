from devices import Devices
from monitors import Monitors
from names import Names
from network import Network
from scanner import Scanner
import error


"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""


class Parser:

    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """

    def __init__(self, names: Names, devices: Devices, network: Network,
                 monitors: Monitors, scanner: Scanner):
        """Initialise constants."""
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner
        self.error_handler = error.ErrorHandler()

    def log_error(self, err: error.MyException):
        """Log an error and continue parsing."""

        # TODO: Set the positions of an error
        # calls the __call__ funciton in class ErrorHandler in error.py
        self.error_handler(err)

        # Delete the following in the final code
        # print all errors
        err.set_error_position(self.scanner)
        print(f"Error row: {err.error_row}, column: {err.error_col}.")
        self.error_handler.print_all_errors(self.scanner)
        print('Done with printing log_error.')

        # Edit the below comment
        # Current symbol is skipped but do keep reading until
        # we reach a "stopping symbol"
        self.get_next_symbol()

        # TODO: add self.scanner.COMMA in the following list
        # after implementing the cursor position
        while self.symbol.type not in [self.scanner.SEMICOLON, self.scanner.EOF]:
            self.get_next_symbol()

        print('I am about to enter self.parse_network() in log_error() in parse.py')
        
        # THIS LINE BELOW IS ONLY NEEDED IF ALL OF THE DEVICE_LIST AND MONITORS_LIST
        # FUNCTIONS ARE COMMENTTED OUT inside log_error.
        #self.parse_network()

    def get_next_symbol(self):
        """Get next symbol and assign it to self.symbol"""
        self.symbol = self.scanner.get_symbol()

    def parse_network(self):
        """Parse the circuit definition file.
        Return True if there are no errors in the defintion file,
        false otherwise."""
        print("I'm in parse network.")
        self.get_next_symbol()
        self.device_list()
        # self.connection_list()
        self.monitor_list()

        # Returns true if all symbols are correctly parsed, if not return false
        return self.error_handler.found_no_errors()

    def connection_list(self):
        # print('Im inside parser connection_list')
        if (self.symbol.type == self.scanner.KEYWORD and
           self.symbol.id == self.scanner.CONNECT_ID):

            self.symbol = self.scanner.get_symbol()
            # self.connection()
            print('Making a connection.\n')
            while self.symbol.type == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                # self.connection()
                print('Making a connection.\n')
            if self.symbol.type == self.scanner.SEMICOLON:
                self.symbol = self.scanner.get_symbol()
        else:
            print(self.symbol)
            raise Exception(
                'List of connections must begin with CONNECT keyword')

    def connection(self):
        op_device_id, op_port_id = self.output_device()
        if self.symbol.type == self.scanner.EQUALS:
            self.get_next_symbol()
            ip_device_id, ip_port_id = self.input_device()
            input_device = self.devices.get_device(ip_device_id)
            if input_device.inputs[ip_port_id] is not None:
                raise Exception('Port in use')
            self.network.make_connection(
                op_device_id, op_port_id, ip_device_id, ip_port_id)
        else:
            self.error_handler()

        # TODO for Lolith: call parse_network()

    def input_device(self):
        # Retrieve device id
        ip_device_id = self.get_device_id()
        # Advance to next symbol
        self.symbol = self.scanner.get_symbol()

        # Check symbol type is DOT which denotes definition of input port
        if self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            # Find input port name
            input_str = self.names.get_name_string()
            if input_str[0] == 'I' and input_str[1:].isdigit():
                ip_port_id = self.symbol.id
                return ip_device_id, ip_port_id
        else:
            raise error.MissingPunctuationError(
                'Must have a DOT before specifying input')

    def output_device(self):
        op_device_id = self.get_device_id()
        self.symbol = self.scanner.get_symbol()
        # TODO implement parsing of D-TYPE latch output
        return op_device_id, None

    def get_device_id(self):
        if self.symbol.type == self.scanner.NAME:
            return self.symbol.id
        elif self.symbol.type == self.scanner.KEYWORD:
            raise NameError("Cannot use KEYWORD as device name")
        else:
            raise NameError("Device Name must be an alphanumeric string.")

    def device_list(self):
        print('Im inside of device_list in parse_network()')
        try:  # check device type has been declared
            if (self.symbol.type == self.scanner.KEYWORD and self.symbol.id
                    == self.scanner.DEVICE_ID):
                # Advance to next symbol, which should be a ":"
                print('The current symbol is DEVICE')
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.COLON:
                    print('The current symbol is :')
                    self.symbol = self.scanner.get_symbol()
                    self.device()

                else:
                    raise error.MissingPunctuationError(
                        'Missing ":" in device definition.')
            # else:
            #    raise error.DeviceNameError("Device name is missing.")
        except error.MyException as err:
            # Logs an error and continue parsing
            print(err.get_error_name)
            self.log_error(err)

    def device(self):
        # Initialise three properties of device (id, kind and property)
        # Get device_id from device_name specified in syntax
        device_id = self.get_device_id()
        print(
            f"Current symbol is {self.symbol.type} and current device_id is: {device_id}")
        device_kind = None
        device_property = None

        try:
            print('Im in the try block in device() in parse.py')

            # Advance to next symbol
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.COMMA:
                print('Current symbol is a COMMA')
                self.symbol = self.scanner.get_symbol()

                if (self.symbol.type is None and self.symbol.id == 0):
                    # Set device kind as AND
                    device_kind = self.devices.AND
                    print('Device is AND')
                    # Advance to next symbol which is expected to be be a comma
                    self.symbol = self.scanner.get_symbol()

                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        print('second COMMA')
                        device_property = self.scanner.get_symbol()
                        self.get_next_symbol()
                        if self.symbol.type == self.scanner.SEMICOLON:
                            print('I found a SEMICOLON at end of line, as I should.')
                            pass
                        else:
                            print(
                                'Im in the else inside of the AND in devices() in parse.py')
                            raise error.MissingPunctuationError(
                                "Missing SEMICOLON at end of line.")

                elif (self.symbol.type is None and self.symbol.id == 1):
                    # Set device kind as OR
                    device_kind = self.devices.OR
                    # Advance to next symbol which is expected to be be a comma
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        device_property = self.scanner.get_symbol()
                        self.get_next_symbol()
                        if self.symbol.type == self.scanner.SEMICOLON:
                            pass

                elif (self.symbol.type is None and self.symbol.id == 2):
                    # Set device kind as NAND
                    device_kind = self.devices.NAND
                    # Advance to next symbol which is expected to be be a comma
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        device_property = self.scanner.get_symbol()
                        self.get_next_symbol()
                        if self.symbol.type == self.scanner.SEMICOLON:
                            pass

                elif (self.symbol.type is None and self.symbol.id == 3):
                    # Set device kind as NOR
                    device_kind = self.devices.NOR
                    # Advance to next symbol which is expected to be be a comma
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        device_property = self.scanner.get_symbol()
                        self.get_next_symbol()
                        if self.symbol.type == self.scanner.SEMICOLON:
                            pass

                elif (self.symbol.type is None and self.symbol.id == 4):
                    # Set device kind as XOR
                    device_kind = self.devices.XOR
                    # Advance to next symbol which is expected to be be a comma
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        device_property = self.scanner.get_symbol()
                        self.get_next_symbol()
                        if self.symbol.type == self.scanner.SEMICOLON:
                            pass

                elif (self.symbol.type is None and self.symbol.id == 5):
                    # Set device kind as CLOCK
                    device_kind = self.devices.CLOCK
                    # Advance to next symbol which is expected to be be a comma
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        device_property = self.scanner.get_symbol()
                        self.get_next_symbol()
                        if self.symbol.type == self.scanner.SEMICOLON:
                            pass

                elif (self.symbol.type is None and self.symbol.id == 6):
                    # Set device kind as SWITCH
                    device_kind = self.devices.SWITCH
                    # Advance to next symbol which is expected to be be a comma
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        device_property = self.scanner.get_symbol()
                        self.get_next_symbol()
                        if self.symbol.type == self.scanner.SEMICOLON:
                            pass

                # TODO: Add an elif for a DTYPE, once DTYPE is functional

        except error.MyException as err:
            print('Im in the except inside of device() in parse.py')
            print(err.get_error_name)
            self.log_error(err)

        else:

            # Call make_device
            # error_type = self.devices.make_device(
            #    device_id, device_kind, device_property)

            # TODO: Comment the thing above in final code
            error_type = self.devices.NO_ERROR
            print('Now "fake" calling make_device.')

            if error_type is self.devices.NO_ERROR:
                self.parse_network()

            return None

    def monitor_list(self):
        print("i'm inside monitor_list")
        try:
            if (self.symbol.type == self.scanner.KEYWORD
                    and self.symbol.id == self.scanner.MONITOR_ID):

                self.get_next_symbol()
                if (self.symbol.type == self.scanner.COLON):
                    self.get_next_symbol()
                    self.monitor()
                    while self.symbol.type == self.scanner.COMMA:
                        self.get_next_symbol()
                        self.monitor()
                    if self.symbol.type == self.scanner.SEMICOLON:
                        self.get_next_symbol()
                    else:
                        raise error.MissingPunctuationError(
                            'SEMICOLON missing from end of line.')
                else:
                    raise error.MissingPunctuationError(
                        'Missing ":" in MONITOR definition.')
            else:
                raise error.KeywordError('MONITOR keyword is missing')

        except error.MyException as err:
            # Logs an error and continue parsing
            print(err.get_error_name)
            self.log_error(err)

    def monitor(self):
        op_device_id, op_port_id = self.output_device()
        # Call make_monitor from monitors.py
        # self.monitors.make_monitor(op_device_id, op_port_id)

    def comment(self):
        """Do not parse symbols between two hash symbols"""
        if self.symbol.type == self.scanner.HASH:
            self.get_next_symbol()
            while self.symbol.type != self.scanner.HASH:
                # Continue getting symbols but not parsing
                self.get_next_symbol()
                # move to next symbol
            self.get_next_symbol()

    def error(self):
        raise Exception("You have an error!")

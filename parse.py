from devices import Devices
from monitors import Monitors
from names import Names
from network import Network
from scanner import Scanner, Symbol


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
                 monitors: Monitors, scanner: Scanner, symbol: Symbol):
        """Initialise constants."""
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner
        self.symbol = symbol

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        return True

    def connection_list(self):
        if (self.symbol.type == self.scanner.KEYWORD and self.symbol.id ==
                self.scanner.CONNECT_ID):
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.COLON:
                self.symbol.type == self.get_symbol()
                self.connection()
                while self.symbol.type == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    self.connection()
                if self.symbol.type == self.scanner.SEMICOLON:
                    self.symbol = self.scanner.get_symbol()
        else:
            # TODO
            self.error()

    def connection(self):
        ip_device_id, ip_port_id = self.input_device()
        if self.symbol.type == self.scanner.EQUALS:
            self.symbol = self.scanner.get_symbol()
            op_device_id, op_port_id = self.output_device()
            self.network.make_connection(
                ip_device_id, ip_port_id, op_device_id, op_port_id)
        else:
            self.error()

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
            raise NameError("Device Name must be an alphanumeric string")

    def device_list(self):
        # check device type has been declared
        if (self.symbol.type == self.scanner.KEYWORD and self.symbol.id
                == self.scanner.NEW_DEVICE_ID):
            # Advance to next symbol
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.COLON:
                self.symbol = self.scanner.get_symbol()
                self.device()

        else:
            raise SyntaxError('Must specify device type beforehand')

    def device(self):
        # Intialise three properties of device (id, kind and property)
        # Get device_id from device_name specified in syntax
        device_id = self.get_device_id()
        device_kind = None
        device_property = None
        # Advance to next symbol
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.COMMA:
            self.symbol.type = self.scanner.get_symbol()
            if (self.symbol.type is None and self.symbol.id == 0):
                # Set device kind as AND
                device_kind = self.devices.AND
                # Advance to next symbol which is expected to be be a comma
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.COMMA:
                    """following comma, device property is specified -
                    any errors will be raised by devices"""
                    device_property = self.scanner.get_symbol()

            elif (self.symbol.type is None and self.symbol.id == 1):
                # Set device kind as
                device_kind = self.devices.OR
                # Advance to next symbol which is expected to be be a comma
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.COMMA:
                    """following comma, device property is specified -
                    any errors will be raised by devices"""
                    device_property = self.scanner.get_symbol()

            elif (self.symbol.type is None and self.symbol.id == 2):
                # Set device kind as NAND
                device_kind = self.devices.NAND
                # Advance to next symbol which is expected to be be a comma
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.COMMA:
                    """following comma, device property is specified -
                    any errors will be raised by devices"""
                    device_property = self.scanner.get_symbol()

            elif (self.symbol.type is None and self.symbol.id == 3):
                # Set device kind as AND
                device_kind = self.devices.NOR
                # Advance to next symbol which is expected to be be a comma
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.COMMA:
                    """following comma, device property is specified -
                    any errors will be raised by devices"""
                    device_property = self.scanner.get_symbol()

            elif (self.symbol.type is None and self.symbol.id == 4):
                # Set device kind as AND
                device_kind = self.devices.XOR
                # Advance to next symbol which is expected to be be a comma
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.COMMA:
                    """following comma, device property is specified -
                    any errors will be raised by devices"""
                    device_property = self.scanner.get_symbol()

            elif (self.symbol.type is None and self.symbol.id == 5):
                # Set device kind as AND
                device_kind = self.devices.CLOCK
                # Advance to next symbol which is expected to be be a comma
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.COMMA:
                    """following comma, device property is specified -
                    any errors will be raised by devices"""
                    device_property = self.scanner.get_symbol()

            elif (self.symbol.type is None and self.symbol.id == 6):
                # Set device kind as AND
                device_kind = self.devices.DTYPE
                # Advance to next symbol which is expected to be be a comma
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.COMMA:
                    """following comma, device property is specified -
                    any errors will be raised by devices"""
                    device_property = self.scanner.get_symbol()

        # Call make_device
        error_type = self.devices.make_device(
            device_id, device_kind, device_property)
        return error_type

    def error():
        pass

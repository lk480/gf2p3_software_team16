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

    def __init__(
        self,
        names: Names,
        devices: Devices,
        network: Network,
        monitors: Monitors,
        scanner: Scanner,
    ):
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

        self.error_handler.print_error(self.scanner)
        print("Done with printing log_error.")

        # Edit the below comment
        # Current symbol is skipped but do keep reading until
        # we reach a "stopping symbol"
        self.get_next_symbol()

        # TODO: add self.scanner.COMMA in the following list
        # after implementing the cursor position
        while self.symbol.type not in [self.scanner.SEMICOLON, self.scanner.EOF]:
            self.get_next_symbol()

    def get_next_symbol(self):
        """Get next symbol and assign it to self.symbol"""
        self.symbol = self.scanner.get_symbol()

    def parse_network(self):
        """Parse the circuit definition file.
        Return True if there are no errors in the defintion file,
        false otherwise."""

        print("Calling parse_network().")
        # Advance to the next symbol
        self.get_next_symbol()
        # Parse specified devices in def. file
        self.device_list()

        # Parse specified connections in def. file
        self.connection_list()
        # Parse specified monitor points in def. file
        self.monitor_list()

        if self.error_handler.found_no_errors():
            print("Defintion File Parsed")
            return True
        else:
            self.error_handler.raise_error()

    def connection_list(self):
        try:
            print("Successfully called connection_list in parser")
            if (
                self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.CONNECT_ID
            ):
                self.symbol = self.scanner.get_symbol()
                print("Making a connection.\n")
                self.get_next_symbol()
                self.connection()
                self.get_next_symbol()  # SHOULD BE COMMA OR SEMICOLON
                # Checking for mutiple connections
                while self.symbol.type == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    print("Making a connection.\n")
                    self.connection()
                self.get_next_symbol()
                if self.symbol.type == self.scanner.SEMICOLON:
                    self.symbol = self.scanner.get_symbol()
                else:
                    raise error.MissingPunctuationError(
                        "Missing SEMICOLON at end of line."
                    )
                """THIS IS A TEMPORARY THING DELETE PLEASE"""
            elif 1 == 1:
                pass
            else:
                print(self.symbol)
                raise error.KeywordError(
                    "List of connections must begin with CONNECT keyword"
                )
        except error.MyException as err:
            print("Im in the except inside of connection_list() in parse.py")
            self.log_error(err)

    def connection(self):
        try:
            """first find output device id and port_id
            (note port_id will be None for all devices except DTYPE )"""

            op_device_id, op_port_id = self.output_device()

            if self.symbol.type == self.scanner.EQUALS:
                self.get_next_symbol()
                ip_device_id, ip_port_id = self.input_device()
                input_device = self.devices.get_device(ip_device_id)
                if input_device.inputs[ip_port_id] is not None:
                    raise error.MultipleInputError("This input is already connected")

            else:
                raise error.MissingPunctuationError(
                    "Connections must be specified with an EQUAL (=)"
                )
        except error.MyException() as err:
            print("Successfuly entered exception condition of connection()")
            # print error log
            self.log_error(err)
        # if there are no errors, call make connection
        else:
            error_type = self.devices.NO_ERROR
            print("Now calling make_connection")
            self.network.make_connection(
                op_device_id, op_port_id, ip_device_id, ip_port_id
            )
            if error_type != self.devices.NO_ERROR:
                self.log_error(error_type)

        # TODO for Lolith: call parse_network()

    def input_device(self):
        """Function that returns the input device id and input port id
        (in case of DTYPE Latch) - these paramters are needed when calling
        the make_connection() method from the network module"""
        # Retrieve device id
        ip_device_id = self.get_device_id()
        # Check if input device_id is obtained
        if ip_device_id is None:
            raise error.DefinitionError(
                f"Device {self.names.get_name_string(ip_device_id)} not found"
            )

        # Advance to next symbol
        self.symbol = self.scanner.get_symbol()
        # Check symbol type is DOT which denotes definition of input port
        if self.symbol.type == self.scanner.DOT:
            self.get_next_symbol()
            # Find input port name and check whether device is a DTYPE Latch
            if self.symbol.id in self.devices.dtype_input_ids:
                # Device is DTYPE Latch
                print("Device is a DTYPE")
                ip_port_id = self.symbol.id
                self.get_next_symbol()
                return ip_device_id, ip_port_id
            else:
                # Device is not a DTYPE Latch
                print("Device is NOT DTYPE")
                input_str = self.names.get_name_string(self.symbol.id)
                if input_str[0] == "I" and input_str[1:].isdigit():
                    ip_port_id = self.symbol.id
                    return ip_device_id, ip_port_id
                else:
                    raise error.PortReferenceError(
                        "Input port incorrectly defined - see EBNF"
                    )
        else:
            raise error.MissingPunctuationError(
                "Must have a DOT before specifying input"
            )

    def output_device(self):
        """Function that returns the output device id and output port id
        (in case of DTYPE Latch) - these paramters are needed when calling
        the make_connection() method from the network module"""
        # Retrieve device id
        op_device_id = self.get_device_id()

        # Check if output device_id is obtained
        if op_device_id is None:
            raise error.DefinitionError(
                f"Device {self.names.get_name_string(op_device_id)} not found"
            )
        # Advance to next symbol
        self.get_next_symbol()
        if self.symbol.type == self.scanner.DOT:
            self.get_next_symbol()
            if self.symbol.type == self.scanner.NAME:
                if self.symbol.id in self.devices.dtype_output_ids:
                    # Device is a DTYPE Latch
                    print("Device is a DTYPE Latch")
                    op_port_id = self.symbol.id
                    self.get_next_symbol()
                    return op_device_id, op_port_id
                else:
                    raise error.PortReferenceError("Device input port does not exist")
        else:
            print("Device is not a DTYPE Latch")
            # Output device is not a DTYPE Latch so op_port_id must be None
            return op_device_id, None

    def get_device_id(self):
        if self.symbol.type == self.scanner.NAME:
            return self.symbol.id
        elif self.symbol.type == self.scanner.KEYWORD:
            raise error.DeviceNameError("Cannot use KEYWORD as device name")
        else:
            raise error.DeviceNameError("Device Name must be an alphanumeric string.")

    # Continue checking for devices until keyword "CONNECT" is detected
    def device_list(self):
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.DEVICE_ID
        ):
            defining_devices = True
        count = 0
        while defining_devices is True:
            # Create new device
            if count >= 500:
                break

            count += 1
            self.device_creation()
            # Get next symbol
            self.get_next_symbol()
            # Check if next symbol is CONNECT

            if (
                self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.CONNECT_ID
            ):
                defining_devices = False

            elif (
                self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.MONITOR_ID
            ):
                defining_devices = False

            elif self.symbol.type == self.scanner.EOF:
                break

    def device_creation(self):
        print("Successfully called device_creation in parser module")
        try:  # check device type has been declared
            if (
                self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.DEVICE_ID
            ):
                # Check current symbol is DEVICE

                print(f"Current Symbol {self.names.get_name_string(self.symbol.id)}")
                self.get_next_symbol()

                if self.symbol.type == self.scanner.COLON:
                    # print(f"Current Symbol {self.names.get_name_string(self.symbol.id)}")
                    self.get_next_symbol()
                    # Calling device()
                    self.device()
                else:
                    raise error.MissingPunctuationError(
                        'Missing ":" in device definition.'
                    )
            else:
                raise error.DeviceNameError("Device name is missing.")
        except error.MyException as err:
            # Logs an error and continue parsing
            self.log_error(err)

    def device(self):
        try:
            print(f"Current symbol {self.names.get_name_string(self.symbol.id)}")
            # Initalise parameters of the device
            device_id = self.get_device_id()
            device_kind = None
            device_property = None
            # Advance to next symbol --> COMMA
            self.get_next_symbol()
            if self.symbol.type == self.scanner.COMMA:
                print("FIRST COMMA PARSED")
                # Advance to the next symbol --> DEVICE TYPE
                self.get_next_symbol()
                # If DEVICE-TYPE is AND,NAND,OR,NOR
                if self.symbol.type is self.scanner.NAME and self.symbol.id in [
                    self.devices.AND,
                    self.devices.NAND,
                    self.devices.OR,
                    self.devices.NOR,
                ]:
                    # Set device_kind
                    print(
                        f"Device Type is {self.names.get_name_string(self.symbol.id)}"
                    )
                    device_kind = self.symbol.id
                    # Advance to next symbol --> COMMA
                    self.get_next_symbol()

                    if self.symbol.type == self.scanner.COMMA:
                        print("SECOND COMMA PARSED")
                        """following comma, device property is specified"""
                        device_property = self.scanner.get_symbol()
                        self.get_next_symbol()

                        if int(device_property.id) not in range(1, 17):
                            raise error.InputPinNumberError(
                                "Number of device inputs not valid"
                            )
                            # Advance to final symbol --> SEMICOLON
                            self.get_next_symbol()
                            if self.symbol.type == self.scanner.SEMICOLON:
                                pass
                            else:
                                raise error.MissingPunctuationError(
                                    "Missing SEMICOLON at end of line."
                                )

                # If DEVICE TYPE is D_TYPE or XOR
                elif self.symbol.type is self.scanner.NAME and self.symbol.id in [
                    self.devices.D_TYPE,
                    self.devices.XOR,
                ]:
                    # Set device kind
                    print(
                        f"Device Type is {self.names.get_name_string(self.symbol.id)}"
                    )
                    device_kind = self.symbol.id
                    # Advance to next symbol --> COMMA
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified"""
                        # For D_TYPE and XOR gates, this should be NoneType
                        self.get_next_symbol()
                        if self.symbol.type == self.scanner.SEMICOLON:
                            pass

                # If DEVICE TYPE is CLOCK
                elif (
                    self.symbol.type is self.scanner.NAME
                    and self.symbol.id == self.devices.CLOCK
                ):
                    # Set device kind
                    print(
                        f"Device Type is {self.names.get_name_string(self.symbol.id)}"
                    )
                    device_kind = self.symbol.id
                    # Advance to next symbol --> COMMA
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        device_property = self.scanner.get_symbol()

                        self.get_next_symbol()
                        if self.symbol.type == self.scanner.SEMICOLON:
                            pass

                elif (
                    self.symbol.type is self.scanner.NAME
                    and self.symbol.id == self.devices.SWITCH
                ):
                    device_kind = self.symbol.id
                    # Advance to next symbol --> COMMA
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        print("SECOND COMMA")
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        device_property = self.scanner.get_symbol()
                        self.get_next_symbol()

                        if self.symbol.type == self.scanner.SEMICOLON:
                            pass

        except error.MyException as err:
            print("Im in the except inside of device() in parse.py")
            self.log_error(err)

        else:
            # Call make_device
            # Using None to avoid problems with switches in state 0
            if device_property is not None:
                int_device_property = int(device_property.id)
            else:
                int_device_property = None
            error_type = self.devices.make_device(
                device_id, device_kind, int_device_property
            )

            error_type = self.devices.NO_ERROR
            print('Now "fake" calling make_device.')
            if error_type != self.devices.NO_ERROR:
                self.log_error(error_type)

    def monitor_list(self):
        print("i'm inside monitor_list")
        try:
            if (
                self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.MONITOR_ID
            ):
                self.get_next_symbol()
                if self.symbol.type == self.scanner.COLON:
                    self.get_next_symbol()

                    # Calling monitor
                    self.monitor()
                    # When monitoring multiple ports
                    while self.symbol.type == self.scanner.COMMA:
                        self.get_next_symbol()
                        self.monitor()
                    if self.symbol.type == self.scanner.SEMICOLON:
                        self.get_next_symbol()
                    else:
                        raise error.MissingPunctuationError(
                            "SEMICOLON missing from end of line."
                        )
                else:
                    raise error.MissingPunctuationError(
                        'Missing ":" in MONITOR definition.'
                    )
            else:
                raise error.KeywordError("MONITOR keyword is missing")

        except error.MyException as err:
            # Logs an error and continue parsing
            self.log_error(err)

    def monitor(self):
        try:
            op_device_id, op_port_id = self.output_device()
        except error.MyException as err:
            self.log_error(err)
        else:
            self.monitors.make_monitor(op_device_id, op_port_id)

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

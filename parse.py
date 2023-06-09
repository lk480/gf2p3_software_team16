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
        """Logs errors encoutered in the defintion file and continues parsing

        Args:
            err (error.MyException): custom exceptions defined in error.py
        """

        self.error_handler(err)

        err.set_error_position(self.scanner)
        # Display the row and colum of encountered error
        print(f"Error row: {err.error_row}, column: {err.error_col}.")

        # Print the message for the encountered error
        self.error_handler.print_error(self.scanner)

        # Advance to the next symbol
        self.get_next_symbol()

        # Check whether symbol type is one the stopping symbols
        while self.symbol.type not in [self.scanner.SEMICOLON,
                                       self.scanner.EOF]:
            # Continue parsing until a stopping symbol is encountered
            self.get_next_symbol()

    def semantic_error_reporting(self, error_type: int):
        """Function converts the error_type to a
        custom exception defined in error.py

        Args:
            error_type (int): each error code corresponds to a semantic error
            that is assigned by the methods in Devices class

        Raises:
            error.UnknownUniqueErrorCode: Error code is outside of range
            error.InvalidPropertyError: Device property is invalid
            error.NoPropertyError: Device property has not been provided
            error.NoDeviceFoundError: Device has not been defined
            error.PropertyPresentError: Device property specified
                                            but not required for chosen device
            error.DevicePresentError: Device already exists
        """

        if error_type not in range(6):
            raise error.UnknownUniqueErrorCode("Unknown unique error code")
        if error_type == 0:
            pass
        if error_type == 1:
            raise error.InvalidPropertyError(
                "Device property is incorrectly defined")
        if error_type == 2:
            raise error.NoPropertyError("Property is missing")
        if error_type == 3:
            raise error.NoDeviceFoundError("Device does not exist")
        if error_type == 4:
            raise error.PropertyPresentError(
                "DTYPE and XOR devices do not require a property"
            )
        if error_type == 5:
            raise error.DevicePresentError("Device already exists")

    def get_next_symbol(self):
        """Get next symbol and assign it to self.symbol
        """
        self.symbol = self.scanner.get_symbol()

    def parse_network(self):
        """Parse the circuit definition file.

        Returns True if there are no errors in the defintion file.

        Returns:
            bool or None: True if there are no errors in definiton file, if
                          errors are encountered returns None.

        """
        self.get_next_symbol()
        # Check if file is empty
        if self.symbol.type == self.scanner.EOF:
            print("NO CIRCUIT SPECIFIED")
            return False
        else:
            # Check for comments
            self.comment()
            # Parse specified devices in def. file
            self.device_list()
            # Parse specified connections in def. file
            self.connection_list()
            # Parse specified monitor points in def. file
            self.monitor_list()

        if self.error_handler.found_no_errors():
            print("DEFINITION FILE PARSED")
            return True
        else:
            # this should raise the first error
            self.error_handler.print_error(self.scanner)
            self.error_handler.raise_error()

    def connection_list(self):
        """Parses the connections specified in the definition file and
        determines whether a single or multiple connections have been defined.

        Raises:
            error.MissingPunctuationError: SEMICOLON not specified at end of
                                            line in definition file
            error.KeywordError: CONNECT keyword must be used when
                specifying connections in definition file
        """

        try:
            # Check if symbol type is KEYWORD and id corresponds to CONNECT
            if (
                self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.CONNECT_ID
            ):
                self.get_next_symbol()
                self.get_next_symbol()
                # Check if symbol type is KEYWORD and id corresponds to NONE
                if (
                    self.symbol.type == self.scanner.KEYWORD
                    and self.symbol.id == self.scanner.NONE_ID
                ):
                    print("NO CONNECTION SPECIFIED")
                    self.get_next_symbol()
                else:
                    print("MAKING CONNECTION \n")
                    self.connection()
                # Checking for mutiple connections
                while self.symbol.type == self.scanner.COMMA:
                    self.symbol = self.scanner.get_symbol()
                    print("MAKING CONNECTION \n")
                    self.connection()
                if self.symbol.type is not self.scanner.SEMICOLON:
                    raise error.MissingPunctuationError(
                        "Missing SEMICOLON at end of line."
                    )

            else:
                print(self.symbol)
                raise error.KeywordError(
                    "List of connections must begin with CONNECT keyword"
                )
        except error.MyException as err:
            print("ERROR RAISED")
            self.log_error(err)

    def connection(self):
        """Parses the individual connections i.e. 'input' = 'output' and checks
        whether the device property e.g. number of inputs for a GATE, have
        been correctly specified in the definition file.

        Raises:
            error.InvalidPropertyError: Device property incorrectly specified
            error.MultipleInputError: Multiple outputs connect to a single
                                      input port
            error.MissingPunctuationError: Missing Punctuation
                                           e.g. COMMA, SEMICOLON
        """

        try:
            op_device_id, op_port_id = self.output_device()
            print(
                f"Current Symbol Type {self.symbol.type}, ID: {self.symbol.id}"
            )
            if self.symbol.type == self.scanner.EQUALS:
                self.get_next_symbol()
                ip_device_id, ip_port_id = self.input_device()
                input_device = self.devices.get_device(ip_device_id)
                if input_device is None:
                    raise error.InvalidPropertyError(
                        "Incorrect Device Property.")
                if input_device.inputs.get(ip_port_id) is not None:
                    raise error.MultipleInputError(
                        "This input is already connected")

            else:
                raise error.MissingPunctuationError(
                    "Connections must be specified with an EQUAL (=)"
                )
        except error.MyException as err:
            print("ERROR RAISED")
            # print error log
            self.log_error(err)
        # if there are no errors, call make_connection() located in Network
        else:
            error_type = self.devices.NO_ERROR
            print("Now calling make_connection")
            self.network.make_connection(
                op_device_id, op_port_id, ip_device_id, ip_port_id
            )
            # Report semantic error and raise custom exception
            if error_type != self.devices.NO_ERROR:
                self.semantic_error_reporting(error_type)

    def input_device(self):
        """Function that returns the input device id and input port id
        (in case of DTYPE Latch) - these parameters are needed when calling
        the make_connection() method from the network module

        Raises:
            error.DefinitionError: Device not found/defined
            error.PortReferenceError: Input port not found/defined
            error.MissingPunctuationError: Input must be defined using
                                            the notation .I#

        Returns:
            int: input device ID
            int or None: the input port id if device is D-TYPE,
                         or None for all other devices.
        """

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
                    # Advance symbol -- test
                    self.get_next_symbol()
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
        the make_connection() method from the network module

        Raises:
            error.DefinitionError: Device not found/defined
            error.MonitorError: Cannot monitor a device input
            error.PortReferenceError: Output port not found/defined

        Returns:
            int: output device ID
            int or None: the output port id if device is D-TYPE,
                         or None for all other devices.
        """
        # Retrieve device id
        op_device_id = self.get_device_id()

        # Check if output device_id is obtained
        if op_device_id is None:
            raise error.DefinitionError(
                f"Device {self.names.get_name_string(op_device_id)} not found"
            )

        self.get_next_symbol()
        if self.symbol.type == self.scanner.DOT:
            self.get_next_symbol()
            if (
                self.symbol.type == self.scanner.NAME
                and self.symbol.id in self.devices.dtype_output_ids
                and 
            ):
                # Device is a DTYPE Latch
                print("Device is a DTYPE Latch")
                print(f"Output PORT ID: {self.symbol.id}")
                op_port_id = self.symbol.id
                self.get_next_symbol()

                return op_device_id, op_port_id

            elif self.symbol.type == self.scanner.NAME:
                raise error.MonitorError("Cannot monitor a device input")

            else:
                raise error.PortReferenceError(
                    "DTYPE outport does not exist")
        else:
            print("Device is not a DTYPE Latch")
            # Output device is not a DTYPE Latch so op_port_id must be None
            return op_device_id, None

    def get_device_id(self):
        """Function that gets the ID of the device

        Raises:
            error.DeviceNameError: Device name must be alphanumeric but
                                   not a KEYWORD

        Returns:
            int: Symbol ID
        """
        if self.symbol.type == self.scanner.NAME:
            return self.symbol.id
        elif self.symbol.type == self.scanner.KEYWORD:
            raise error.DeviceNameError("Cannot use KEYWORD as device name")
        else:
            raise error.DeviceNameError(
                "Device Name must be an alphanumeric string.")

    def device_list(self):
        """Identifies devices specified in the definiton file and checks
        whether mutliple devices have been defined

        Raises:
            error.KeywordError: Definition file must contain at least
                                one device
        """
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.DEVICE_ID
        ):
            defining_devices = True

        else:
            raise error.KeywordError("File needs to have at least 1 DEVICE.")

        count = 0
        while defining_devices is True:
            # Debugging Infinte Loops
            if count >= 500:
                break

            count += 1
            self.device_creation()
            # Get next symbol
            self.get_next_symbol()
            # Check if next symbol is CONNECT

            # Only calls device_creation, if the DEVICE KEYWORD is specified
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
        """Checks whether each device has been defined using the correct
            syntax and raises errors accordingly.

        Raises:
            error.MissingPunctuationError: Missing COLON after DEVICE KEYWORD
            error.DeviceNameError: Device name has not been specified
        """
        try:  # check device type has been declared
            if (
                self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.DEVICE_ID
            ):
                # Check current symbol is DEVICE
                print(f"Symbol:{self.names.get_name_string(self.symbol.id)}")

                self.get_next_symbol()

                if self.symbol.type == self.scanner.COLON:
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
        """Parses and processes device definitions.
        This function is responsible for parsing and processing device
        definitions in a larger code context.
        It verifies the device name, type, and properties,
        and initializes the parameters of the device accordingly.

        Returns:
            None

        Raises:
            DeviceNameError: If the device name is a keyword or gate type.
            InputPinNumberError: If the number of device inputs is
                                 not specified or invalid.
            MissingPunctuationError: If there are missing commas or semicolons
                                     in the device definition.
            PropertyPresentError: If a property is specified for device types
                                  that should have None as the property.
            DeviceTypeError: If the device type is missing or unknown.

    """
        try:
            print(
                f"Current symbol {self.names.get_name_string(self.symbol.id)}")
            # Check device name must not be KEYWORD or GATE TYPE
            if self.symbol.type is self.scanner.KEYWORD or self.symbol.id in [
                self.devices.AND,
                self.devices.NAND,
                self.devices.OR,
                self.devices.NOR,
            ]:
                raise error.DeviceNameError(
                    "Device name cannot be KEYWORD or GATE")
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
                if (self.symbol.type is self.scanner.NAME
                        and self.symbol.id) in [
                    self.devices.AND,
                    self.devices.NAND,
                    self.devices.OR,
                    self.devices.NOR,
                ]:
                    # Set device_kind
                    print(f"Type {self.names.get_name_string(self.symbol.id)}")
                    device_kind = self.symbol.id
                    # Advance to next symbol --> COMMA
                    self.get_next_symbol()

                    if self.symbol.type == self.scanner.COMMA:
                        print("SECOND COMMA PARSED")
                        """following comma, device property is specified"""
                        device_property = self.scanner.get_symbol()

                        # I dont think the line below is needed.
                        # self.get_next_symbol()
                        if device_property.id is None:
                            raise error.DefinitionError(
                                "Number of device inputs needs to be specified"
                            )
                        elif int(device_property.id) not in range(1, 17):
                            raise error.InputPinNumberError(
                                "Number of device inputs not valid"
                            )

                        # Advance to final symbol --> SEMICOLON
                        self.get_next_symbol()
                        if self.symbol.type is not self.scanner.SEMICOLON:
                            raise error.MissingPunctuationError(
                                "Missing SEMICOLON at end of line."
                            )
                    else:
                        raise error.MissingPunctuationError(
                            "Missing 2nd COMMA in DEVICE definiton."
                        )

                # If DEVICE TYPE is D_TYPE or XOR
                elif (self.symbol.type is self.scanner.NAME
                        and self.symbol.id) in (
                    self.devices.D_TYPE,
                    self.devices.XOR,
                ):
                    # Set device kind
                    print(f"Type {self.names.get_name_string(self.symbol.id)}")
                    device_kind = self.symbol.id
                    # Advance to next symbol --> SEMICOLON
                    self.symbol = self.scanner.get_symbol()
                    # Checking whether next symbol is SEMICOLON
                    # For DTYPE and XOR, device property should be None
                    if self.symbol.type == self.scanner.SEMICOLON:
                        pass

                    elif self.symbol.type == self.scanner.COMMA:
                        raise error.PropertyPresentError(
                            "For DTYPE or XOR, property should be None."
                        )

                    else:
                        raise error.MissingPunctuationError(
                            "Missing SEMICOLON at end of line."
                        )

                # If DEVICE TYPE is CLOCK
                elif (self.symbol.type is self.scanner.NAME
                        and self.symbol.id) in (
                    self.devices.CLOCK,
                    self.devices.SIGGEN,
                ):
                    # Set device kind
                    print(f"Type {self.names.get_name_string(self.symbol.id)}")
                    device_kind = self.symbol.id
                    # Advance to next symbol --> COMMA
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        device_property = self.scanner.get_symbol()

                        self.get_next_symbol()
                        if self.symbol.type is not self.scanner.SEMICOLON:
                            raise error.MissingPunctuationError(
                                "Missing SEMICOLON at end of line."
                            )
                    else:
                        raise error.MissingPunctuationError(
                            "Missing 2nd COMMA in DEVICE definiton."
                        )

                # If DEVICE TYPE is SWITCH
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

                        if self.symbol.type is not self.scanner.SEMICOLON:
                            raise error.MissingPunctuationError(
                                "Missing SEMICOLON at end of line."
                            )

                # If DEVICE TYPE is RC
                elif (
                    self.symbol.type is self.scanner.NAME
                    and self.symbol.id == self.devices.RC
                ):
                    # Set device kind

                    print(f"Type {self.names.get_name_string(self.symbol.id)}")
                    device_kind = self.symbol.id
                    # Advance to next symbol --> COMMA
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.COMMA:
                        """following comma, device property is specified -
                        any errors will be raised by devices"""
                        device_property = self.scanner.get_symbol()

                        self.get_next_symbol()
                        if self.symbol.type is not self.scanner.SEMICOLON:
                            raise error.MissingPunctuationError(
                                "Missing SEMICOLON at end of line."
                            )

                else:
                    raise error.DeviceTypeError(
                        "Device type is missing or unknown.")
            else:
                raise error.MissingPunctuationError(
                    "Missing a COMMA in DEVICE: definition."
                )

        except error.MyException as err:
            print("Im in the except inside of device() in parse.py")
            self.log_error(err)

        else:
            # Call make_device
            # Using None to avoid problems with switches in state 0
            if device_property is not None:
                if device_kind == self.devices.SIGGEN:
                    int_device_property = list(device_property.id)
                else:
                    int_device_property = int(device_property.id)
                error_type = self.devices.make_device(
                    device_id, device_kind, int_device_property
                )

            else:
                int_device_property = None
                error_type = self.devices.make_device(
                    device_id, device_kind, int_device_property
                )
            if error_type != self.devices.NO_ERROR:
                self.semantic_error_reporting(error_type)

    def monitor_list(self):
        """Parses the list of monitor points specified in the
           definiton file and checks whether multiple monitor points
           have been defined.

        Raises:
            error.MissingPunctuationError: Missing punctuation
            error.MonitorError: MONITOR KEYWORD missing
        """
        if self.symbol.type == self.scanner.SEMICOLON:
            self.get_next_symbol()
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
                    if self.symbol.type is not self.scanner.SEMICOLON:
                        raise error.MissingPunctuationError(
                            "Missing SEMICOLON at end of line."
                        )
                    # TODO: Check if self.get_next_symbol() is missing here
                else:
                    raise error.MissingPunctuationError(
                        'Missing ":" in MONITOR definition.'
                    )
            else:
                raise error.MonitorError("MONITOR keyword is missing.")

        except error.MyException as err:
            # Logs an error and continue parsing
            self.log_error(err)

    def monitor(self):
        """Creates monitor point by calling make_monitor from monitor.py module
        """
        try:
            op_device_id, op_port_id = self.output_device()
        except error.MyException as err:
            self.log_error(err)
        else:
            self.monitors.make_monitor(op_device_id, op_port_id)

    def comment(self):
        """Do not parse symbols between two hash symbols
        """
        if self.symbol.type == self.scanner.HASH:
            self.get_next_symbol()
            while self.symbol.type != self.scanner.HASH:
                # Continue getting symbols but not parsing
                self.get_next_symbol()
                # move to next symbol
            self.get_next_symbol()

    def error(self):
        raise Exception("ERROR!")

import pytest
import error
from pathlib import Path
from names import Names
from scanner import Symbol
from scanner import Scanner
from parse import Parser
from devices import Devices
from monitors import Monitors
from network import Network


@pytest.fixture
def new_symbol():
    """Returns a new Symbol() instance. This will be used
    as a shorthand for instanciating Symbol()
    when defining other functions.
    """
    return Symbol()


@pytest.fixture
def new_names():
    """Return a new Names() instance. This will be used
    as a shorthand for instanciating Names()
    when defining other functions.
    """
    return Names()


@pytest.fixture
def new_device(new_names):
    """Retuns a new Device() instance. The call to this class prepopulates
    the new_names().names_list with gate_strings, device_strings,
    dtype_inputs, dtype_outputs which are defined in devices.py.
    """
    return Devices(new_names)


@pytest.fixture
def new_network(new_names, new_device):
    """Returns a new Network() instance. The call to this class sets
    the new_names().error_code_count equal to 6.
    """
    return Network(new_names, new_device)


@pytest.fixture
def new_monitor(new_names, new_device, new_network):
    """Returns a new Monitor() instance. The call to this class increases
    the new_names().error_code_count equal to 9, because it adds 3 new error
    codes to the fixture from above.
    """
    return Monitors(new_names, new_device, new_network)


@pytest.fixture(scope="function")
def parser(path):
    """Create a new parser object
    Note that the scope is *not* module, as a new Parser is required
    for each different file path"""

    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner)


# ---- SYNTAX ERRORS ----#

"""
Syntax Error - Missing Colon
DEVICE: GATE1, NAND, 2;
DEVICE Gate2, OR, 2;
"""


@pytest.mark.parametrize("file_path, exception", [
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_colon.txt", error.MissingPunctuationError)])
def test_parse_missing_punctuation(new_names, new_device,
                                   new_network, new_monitor,
                                   file_path, exception):
    parser = Parser(new_names, new_device, new_network,
                    new_monitor, Scanner(file_path, new_names))
    with pytest.raises(exception):
        parser.parse_network()


"""
Syntax Error - Missing Attribute
DEVICE: GATE1, NAND, ;
CONNECT: NONE;
MONITOR: GATE1;
"""


@pytest.mark.parametrize("file_path, exception", [
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_attribute.txt", error.DefinitionError)])
def test_parse_missing_attribute(new_names, new_device,
                                 new_network, new_monitor,
                                 file_path, exception):
    parser = Parser(new_names, new_device, new_network,
                    new_monitor, Scanner(file_path, new_names))
    with pytest.raises(exception):
        parser.parse_network()


"""
Syntax Error - Missing Comma
DEVICE: GATE1, NAND 2;
"""


@pytest.mark.parametrize("file_path, exception", [
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_comma.txt", error.MissingPunctuationError)])
def test_parse_missing_comma(new_names, new_device,
                             new_network, new_monitor,
                             file_path, exception):
    parser = Parser(new_names, new_device, new_network,
                    new_monitor, Scanner(file_path, new_names))
    with pytest.raises(exception):
        parser.parse_network()


"""
Syntax Error - Missing Device
    : GATE1, AND, 4;
"""


@pytest.mark.parametrize("file_path, exception", [
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_device.txt", error.KeywordError)])
def test_parse_missing_device(new_names, new_device,
                              new_network, new_monitor,
                              file_path, exception):
    parser = Parser(new_names, new_device, new_network,
                    new_monitor, Scanner(file_path, new_names))
    with pytest.raises(exception):
        parser.parse_network()


"""
Syntax Error - Missing Device Type
    DEVICE: GATE1, , 2;
"""


@pytest.mark.parametrize("file_path, exception", [
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_device_type.txt", TypeError)])
def test_parse_missing_device_type(new_names, new_device,
                                   new_network, new_monitor,
                                   file_path, exception):
    parser = Parser(new_names, new_device, new_network,
                    new_monitor, Scanner(file_path, new_names))
    with pytest.raises(exception):
        parser.parse_network()


"""
Syntax Error - Missing Semicolon
DEVICE: GATE1, NAND, 2
CONNECT: NONE;
"""


@pytest.mark.parametrize("file_path, exception", [
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_semicolon.txt", error.MissingPunctuationError)])
def test_parse_missing_semicolon(new_names, new_device,
                                 new_network, new_monitor,
                                 file_path, exception):
    parser = Parser(new_names, new_device, new_network,
                    new_monitor, Scanner(file_path, new_names))
    with pytest.raises(exception):
        parser.parse_network()


# ---- SEMANTIC ERRORS ---- #

"""
Semantic Error - Multiple outputs connect to a single input port
DEVICE: G1, NAND, 1;
DEVICE: SW1, SWITCH, 0;
DEVICE: SW2, SWITCH, 0;
CONNECT: SW1 = G1.I1, SW2 = G1.I1;
MONITOR: G1;
"""


@pytest.mark.parametrize("file_path, exception", [
    (Path.cwd() / "definition_files" / "semantic_error_files" /
     "multiple_inputs.txt", error.MultipleInputError)])
def test_parse_multiple_inputs(new_names, new_device,
                               new_network, new_monitor,
                               file_path, exception):
    parser = Parser(new_names, new_device, new_network,
                    new_monitor, Scanner(file_path, new_names))
    with pytest.raises(exception):
        parser.parse_network()


"""
Semantic Error - Device name is keyword
DEVICE: NAND, NAND, 2;
"""


@pytest.mark.parametrize("file_path, exception", [
    (Path.cwd() / "definition_files" / "semantic_error_files" /
     "keyword_name_error.txt", error.DeviceNameError)])
def test_parse_keyword_name_error(new_names, new_device,
                                  new_network, new_monitor,
                                  file_path, exception):
    parser = Parser(new_names, new_device, new_network,
                    new_monitor, Scanner(file_path, new_names))
    with pytest.raises(exception):
        parser.parse_network()


"""
Semantic Error - Monitoring a device input
DEVICE: GATE1, NAND, 2;
DEVICE: SWITCH1, SWITCH, 0;
DEVICE: SWITCH2, SWITCH, 0;
CONNECT: SWITCH1 = GATE1.I1, SWITCH2 = GATE1.I2;
MONITOR: GATE1.I1;
"""


@pytest.mark.parametrize("file_path, exception", [
    (Path.cwd() / "definition_files" / "semantic_error_files" /
     "monitor_input.txt", error.MonitorError)])
def test_parse_monitor_input(new_names, new_device,
                             new_network, new_monitor,
                             file_path, exception):
    parser = Parser(new_names, new_device, new_network,
                    new_monitor, Scanner(file_path, new_names))
    with pytest.raises(exception):
        parser.parse_network()


"""
Semantic Error - Referenced port does not exist
DEVICE: G1, NOR, 2;
CONNECT: NONE;
MONITOR: G1.QBAR;
"""


@pytest.mark.parametrize("file_path, exception", [
    (Path.cwd() / "definition_files" / "semantic_error_files" /
     "port_reference_error.txt", error.PortReferenceError)])
def test_parse_port_reference(new_names, new_device,
                              new_network, new_monitor,
                              file_path, exception):
    parser = Parser(new_names, new_device, new_network,
                    new_monitor, Scanner(file_path, new_names))
    with pytest.raises(exception):
        parser.parse_network()

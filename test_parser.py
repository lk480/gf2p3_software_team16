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
SyntaxError - Missing Colon
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
SyntaxError - Missing Attribute
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
SyntaxError - Missing Comma
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
SyntaxError - Missing Device
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
SyntaxError - Missing Device Type
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


"""

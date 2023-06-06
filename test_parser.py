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
    """Returns a new Symbol() instance."""
    return Symbol()


@pytest.fixture
def new_names():
    """Return a new Names() instance."""
    return Names()


@pytest.fixture
def new_device(new_names):
    """Retuns a new Device() instance. The call to this class prepopulates
    the new_names().names_list with gate_strings, device_strings,
    dtype_inputs, dtype_outputs which are defined in devices.py"""
    return Devices(new_names)


@pytest.fixture
def new_network(new_names, new_device):
    """Returns a new Network() instance. The call to this class sets
    the new_names().error_code_count equal to 6."""
    return Network(new_names, new_device)


@pytest.fixture
def new_monitor(new_names, new_device, new_network):
    """Returns a new Monitor() instance. The call to this class increases
    the new_names().error_code_count equal to 9, because it adds 3 new error
    codes to the fixture from above."""
    return Monitors(new_names, new_device, new_network)


@pytest.mark.parametrize("file_path, parse_bool_value", [
    (Path.cwd() / "text files for pytest" /
     "valid circuits" / "make_a_gate.txt", True),
    (Path.cwd() / "text files for pytest" /
     "valid circuits" / "monitor_a_switch.txt", True),
    (Path.cwd() / "text files for pytest" /
     "valid circuits" / "comment_make_a_gate.txt", True)
])
def test_parser(new_names, new_device,
                new_network, new_monitor, file_path, parse_bool_value):
    """Tests if Parser().parse_network() returns True if a correct definition
    file is parsed. If the definition file is erronious, it raises an error.
    This method calls an instance of the Scanner() class, which
    scans the file one line at a time and then parses that line and checks
    if it correctly written.
    """

    parser = Parser(new_names, new_device, new_network, new_monitor,
                    Scanner(file_path, new_names))

    assert parser.parse_network() == parse_bool_value


@pytest.mark.parametrize("file_path, exception", [

    # Syntax error checking
    (Path.cwd() / "text files for pytest" / "syntax errors" /
     "missing_colon.txt", error.MissingPunctuationError),
    (Path.cwd() / "text files for pytest" / "syntax errors" /
     "missing_colon2.txt", error.MissingPunctuationError),
    (Path.cwd() / "text files for pytest" / "syntax errors" /
     "missing_colon3.txt", error.MissingPunctuationError),
    (Path.cwd() / "text files for pytest" / "syntax errors" /
     "missing_colon_with_comment.txt", error.MissingPunctuationError),
    (Path.cwd() / "text files for pytest" / "syntax errors" / "missing_comma.txt",
     error.MissingPunctuationError),
    (Path.cwd() / "text files for pytest" / "syntax errors" /
     "missing_comma2.txt", error.MissingPunctuationError),
    (Path.cwd() / "text files for pytest" / "syntax errors" /
     "missing_attribute.txt", error.InputPinNumberError),
    (Path.cwd() / "text files for pytest" / "syntax errors" /
     "missing_semicolon.txt", error.MissingPunctuationError),
    (Path.cwd() / "text files for pytest" / "syntax errors" /
     "missing_device_type.txt", error.DeviceTypeError),
    (Path.cwd() / "text files for pytest" / "syntax errors" /
     "missing_device.txt", error.KeywordError)


    # Sematic error checking

    # (Path.cwd() / "text files for pytest" / "semantic errors" /
    # "monitor_input.txt", error.InputPinNumberError), # Monitor Error
    
    


    # below tests MAY NOT work.

    # (Path.cwd() / "text files for pytest" / "semantic errors" /
    # "keyword_name_error.txt", error.DeviceNameError)


    #(Path.cwd() / "text files for pytest" / "semantic errors" /
    # "connect_error.txt", error.ConnectError)

    #(Path.cwd() / "text files for pytest" / "semantic errors" /
    # "port_reference_error.txt", error.PortReferenceError)

])
def test_parser_raises_exceptions(new_names, new_device,
                                  new_network, new_monitor,
                                  file_path, exception):

    parser = Parser(new_names, new_device, new_network, new_monitor,
                    Scanner(file_path, new_names))

    with pytest.raises(exception):
        parser.parse_network()

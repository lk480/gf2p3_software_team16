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
    """Returns a new symbol instance."""
    return Symbol()


@pytest.fixture
def new_names():
    """Return a names instance."""
    return Names()


@pytest.fixture
def new_device(new_names):
    """Retuns a new device instance. This pre-populates the new_names().names_list with gates."""
    return Devices(new_names)


@pytest.fixture
def new_network(new_names, new_device):
    """Returns a new network instance."""
    return Network(new_names, new_device)


@pytest.fixture
def new_monitor(new_names, new_device, new_network):
    """Returns a new monitor instance."""
    return Monitors(new_names, new_device, new_network)


@pytest.mark.parametrize("file_path, parse_bool_value", [
    (Path.cwd() / "text files for pytest" / "valid circuits" / "make_a_gate.txt", True),
    (Path.cwd() / "text files for pytest" / "valid circuits" / "monitor_a_switch.txt", True),
    (Path.cwd() / "text files for pytest" / "valid circuits" / "comment_make_a_gate.txt", True)
])
def test_parser(new_names, new_device,
                new_network, new_monitor, file_path, parse_bool_value):

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

    #(Path.cwd() / "text files for pytest" / "semantic errors" /
    # "MonitorError1.txt", error.MonitorError)

    # below tests MAY NOT work.
    
    #(Path.cwd() / "text files for pytest" / "semantic errors" / "ConnectError.txt",

    # error.ConnectError)

    # (Path.cwd() / "text files for pytest" / "semantic errors" / "ReferenceError.txt", error.ReferenceError)
    # (Path.cwd() / "text files for pytest" / "semantic errors" / "PortReferenceError.txt", error.PortReferenceError)

])
def test_parser_raises_exceptions(new_names, new_device,
                                         new_network, new_monitor,
                                         file_path, exception):

    parser = Parser(new_names, new_device, new_network, new_monitor,
                    Scanner(file_path, new_names))

    with pytest.raises(exception):
        parser.parse_network()

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


@pytest.fixture
def file_path_test_connection():
    """Returns the absolute path of test_connection.txt."""
    return Path.cwd() / "text files for pytests" / "test_connection.txt"


@pytest.fixture
def new_scanner_connections_txt(file_path_test_connection, new_names):
    """Returns a new scanner which reads the test_connection.txt"""
    return Scanner(file_path_test_connection, new_names)


@pytest.fixture
def new_parser(new_names, new_device, new_network,
               new_monitor, new_scanner_connections_txt):
    """Returns a new parser that is ready to parses test_connection.txt."""
    return Parser(new_names, new_device,
                  new_network, new_monitor, new_scanner_connections_txt)


@pytest.mark.parametrize("file_path, parse_bool_value", [
    (Path.cwd() / "text files for pytests" / "test_incorrect_monitor.txt", False),
    (Path.cwd() / "text files for pytests" / "test_correct_monitor.txt", True),
    (Path.cwd() / "text files for pytests" / "test_incorrect_device_def.txt", False),
    (Path.cwd() / "monitor_a_switch.txt", True)
])
def test_parse_network_returns_false(new_names, new_device,
                                     new_network, file_path, parse_bool_value):
    parser = Parser(new_names, new_device, new_network, new_monitor,
                    Scanner(file_path, new_names))
    
    assert parser.parse_network() == parse_bool_value





@pytest.mark.parametrize("file_path, exception", [
    # (Path.cwd() / "text files for pytests" / "test_openbracket.txt"),
    # (Path.cwd() / "text files for pytests" / "test_closedbracket.txt"),   
    (Path.cwd() / "text files for pytests" / "test_incorrect_device_def.txt", error.MyException)
    # (Path.cwd() / "example_circuit" / "example_circuit.txt")
    # (Path.cwd() / "monitor_a_switch.txt")
    # (Path.cwd() / "text files for pytests" / "test_one_device.txt")

])
def test_parse_network_raises_exceptions(new_names, new_device,
                                         new_network, file_path, exception):
    
    parser = Parser(new_names, new_device, new_network, new_monitor,
                    Scanner(file_path, new_names))
    
    #assert parser.parse_network() == False

    # The with pytest.raises below might not work
    # with try and except clauses
    with pytest.raises(exception):
        parser.parse_network()



def test_parser(new_parser):
    # TODO: Find a better way to test the parser
    # assert new_parser.parse_network() is True
    pass

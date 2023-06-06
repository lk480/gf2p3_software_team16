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


@pytest.mark.parametrize("file_path, parse_bool_value", [
    (Path.cwd() / "definition_files" /
     "simple_files" / "clock.txt", True),
    (Path.cwd() / "definition_files" /
     "simple_files" / "dtype.txt", True),
    (Path.cwd() / "definition_files" /
     "simple_files" / "nand.txt", True),
    (Path.cwd() / "definition_files" /
     "simple_files" / "nor.txt", True),
    (Path.cwd() / "definition_files" /
     "simple_files" / "rc.txt", True),
    (Path.cwd() / "definition_files" /
     "simple_files" / "siggen.txt", True),
    (Path.cwd() / "definition_files" /
     "simple_files" / "switch.txt", True),
    (Path.cwd() / "definition_files" /
     "simple_files" / "xor.txt", True),
    (Path.cwd() / "definition_files" /
     "demonstration_files" / "2on_2off.txt", True),
    (Path.cwd() / "definition_files" /
     "demonstration_files" / "PWM_clock.txt", True),
    (Path.cwd() / "definition_files" /
     "demonstration_files" / "recursive.txt", True),
    (Path.cwd() / "definition_files" /
     "demonstration_files" / "shift_register.txt", True),
    (Path.cwd() / "definition_files" /
     "demonstration_files" / "sr_bistable.txt", True)
])
def test_parser(new_names, new_device,
                new_network, new_monitor, file_path, parse_bool_value):
    """Test if Parser().parse_network() returns True if a correct definition
    file is parsed. If the definition file is erronious, it raises an error,
    which is explored in the next test, test_parser_raises_exceptions().

    Parser().parse_network() calls an instance of the Scanner() class, which
    scans the .txt file one line at a time and then parses that line and checks
    if it has any errors.
    """
    parser = Parser(new_names, new_device, new_network, new_monitor,
                    Scanner(file_path, new_names))
    assert parser.parse_network() == parse_bool_value


@pytest.mark.parametrize("file_path, exception", [

    # Paths to definition files which contain a syntax error.
    # We pass these paths to the Parser()
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_colon.txt", error.MissingPunctuationError),
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_colon2.txt", error.MissingPunctuationError),
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_colon3.txt", error.MissingPunctuationError),
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_colon_with_comment.txt", error.MissingPunctuationError),
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_comma.txt", error.MissingPunctuationError),
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_comma2.txt", error.MissingPunctuationError),
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_attribute.txt", error.InputPinNumberError),
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_semicolon.txt", error.MissingPunctuationError),
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_device_type.txt", error.DeviceTypeError),
    (Path.cwd() / "definition_files" / "syntax_error_files" /
     "missing_device.txt", error.KeywordError),


    # Paths to definition files which contain a semantic error.
    # We pass these paths to the Parser()

    # TODO: Make the below test cases work

    # (Path.cwd() / "definition_files" / "semantic_error_files" /
    # "monitor_input.txt", error.InputPinNumberError)

    # (Path.cwd() / "definition_files" / "semantic_error_files" /
    # "keyword_name_error.txt", error.DeviceNameError)


    # (Path.cwd() / "definition_files" / "semantic_error_files" /
    # "connect_error.txt", error.ConnectError)

    # (Path.cwd() / "definition_files" / "semantic_error_files" /
    # "port_reference_error.txt", error.PortReferenceError)

])
def test_parser_raises_exceptions(new_names, new_device,
                                  new_network, new_monitor,
                                  file_path, exception):
    """Test if Parser().parse_network() raises the correct error when the
    definition file contains an error. We tests for syntax and semantic errors.
    We created our own error classes which we raise.
    You can find them in error.py.
    """

    parser = Parser(new_names, new_device, new_network, new_monitor,
                    Scanner(file_path, new_names))

    with pytest.raises(exception):
        parser.parse_network()

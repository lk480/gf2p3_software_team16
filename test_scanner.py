"""
Test Suite for scanner.py module

This test file contains unit tests for the scanner module. It verifies
the functionality of the Scanner class in scanning input files and
producing symbols.

Fixtures:
- new_names(): Returns a new Names() instance. Used as a shorthand for
  instantiating Names() when defining other functions.
- new_symbol(): Returns a new Symbol() instance. Used as a shorthand for
  instantiating Symbol() when defining other functions.
- file_path(): Returns the absolute path of scan_device.txt. Used as a test
  file to check the scanner's functionality.
- device_scanner(file_path, new_names): Returns a new Scanner() instance
  that can scan the type_nand.txt file. Used in tests to verify the
  scanner's functionality.

Tests:
- test_init_raises_exception(new_names, file_path): Verifies that when
  supplied with a non-existing file path, the __init__() method in
  Scanner() raises a FileNotFoundError.
- test_scanner_init(device_scanner, new_names): Verifies that the __init__()
  method in Scanner() initializes all the correct arguments, including
  keywords, symbols, and devices.
- test_get_symbol(device_scanner): Verifies the functionality of the
  get_symbol() method in Scanner(), which translates the next sequence
  of characters into a symbol using the Symbol() class.
 - test_skip_space(device_scanner): Verifies the functionality of the skip_space()
  method in Scanner() which skips whitespace characters and returns the
  next-non whitespace character
 - advance(device_scanner):
 - get_number(device_scanner):
 - get_name(device_scanner):
"""

import pytest
from pathlib import Path
from names import Names
from scanner import Symbol
from scanner import Scanner


@pytest.fixture
def new_names():
    """Return a new Names() instance. This will be used
    as a shorthand for instanciating Names()
    when defining other functions.
    """
    return Names()


@pytest.fixture
def new_symbol():
    """Return a new Symbol() instance. This will be used
    as a shorthand for instanciating Symbol()
    when defining other functions.
    """
    return Symbol()


@pytest.fixture
def file_path_scan_device():
    """Returns the absolute path of scan_device.txt. We will use
    this file as a test to see if the scanner works correctly.
    scan_device.txt contains a single line of our EBNF outlining device
    creation:
    DEVICE: G1, NAND, 12;
    """
    path = Path.cwd() / "definition_files" / "scanner_test_files" \
        / "scan_device.txt"
    return path


@pytest.fixture
def device_scanner(file_path_scan_device, new_names):
    """Returns a new Scanner() instance which will
    scan the scan_device.txt file. This is later used in tests
    to see if the scanner works correctly."""
    return Scanner(file_path_scan_device, new_names)


@pytest.fixture
def sequence_scanner(file_path_sequence, new_names):
    """Returns a new Scanner() instance which will scan the 
    character_sequence.txt file. This will be used to test the
    functionality of Scanner() class methods"""
    return Scanner(file_path_sequence, new_names)


def test_init_raises_exception(new_names, file_path_scan_device):
    """Tests if when supplied a non existing file path
    the __init__() method in Scanner() raises a "FileNotFoundError".
    """
    with pytest.raises(FileNotFoundError):
        Scanner(Path('unknown.bla'), new_names)
    with pytest.raises(FileNotFoundError):
        Scanner(Path('unknown.txt'), new_names)


def test_scanner_init(device_scanner, new_names):
    """Tests if the __init__() method in Scanner()
    initializes all the correct arguments such as keywords,
    symbols and devices. To see how __init()__ works go to scanner.py.
    """
    assert isinstance(device_scanner, Scanner)
    assert device_scanner.current_character == ' '
    assert device_scanner.keywords_list == ['DEVICE', 'CONNECT', 'MONITOR',
                                            'TYPE', 'STATE', 'INPUTS', 'NONE']

    assert device_scanner.symbol_type_list == range(12)
    assert device_scanner.COMMA in device_scanner.symbol_type_list
    assert device_scanner.EQUALS in device_scanner.symbol_type_list
    assert device_scanner.DOT in device_scanner.symbol_type_list
    assert device_scanner.OPENBRACKET in device_scanner.symbol_type_list
    assert device_scanner.CLOSEDBRACKET in device_scanner.symbol_type_list
    assert device_scanner.KEYWORD in device_scanner.symbol_type_list
    assert device_scanner.NUMBER in device_scanner.symbol_type_list
    assert device_scanner.NAME in device_scanner.symbol_type_list
    assert device_scanner.EOF in device_scanner.symbol_type_list
    assert device_scanner.COLON in device_scanner.symbol_type_list
    assert device_scanner.HASH in device_scanner.symbol_type_list

    assert [device_scanner.DEVICE_ID] == device_scanner.names.lookup([
                                                                     'DEVICE'])
    assert [device_scanner.CONNECT_ID] == device_scanner.names.lookup([
                                                                      'CONNECT'])
    assert [device_scanner.MONITOR_ID] == device_scanner.names.lookup([
                                                                      'MONITOR'])
    assert [device_scanner.TYPE_ID] == device_scanner.names.lookup(['TYPE'])
    assert [device_scanner.STATE_ID] == device_scanner.names.lookup(['STATE'])
    assert [device_scanner.INPUTS_ID] == device_scanner.names.lookup([
                                                                     'INPUTS'])
    assert [device_scanner.NONE_ID] == device_scanner.names.lookup(['NONE'])


def test_get_symbol(device_scanner):
    """Tests the Scanner().get_symbol() method. The method
    translates the sequence of characters into a symbol,
    which is an instance of the class Symbol(). 
    """
    # The first symbol should be "DEVICE" from scan_device.txt
    # As this is is a KEYWORD we must check its type and ID
    symbol = device_scanner.get_symbol()
    assert symbol.type == device_scanner.KEYWORD
    assert symbol.id == device_scanner.DEVICE_ID

    # The next symbol should be ":" from scan_device.txt
    symbol = device_scanner.get_symbol()
    assert symbol.type == device_scanner.COLON
    # ":" should not have ID
    assert symbol.id is None

    # The next symbol should be the string 'G1' from scan_device.txt
    symbol = device_scanner.get_symbol()
    assert symbol.type == device_scanner.NAME
    assert symbol.type == 8
    # "G1" should not have ID
    print(symbol.id)

    # The next symbol should be a COMMA
    symbol = device_scanner.get_symbol()
    assert symbol.type == device_scanner.COMMA
    # "," should not have ID
    assert symbol.id is None

    # The next symbol should be "NAND" from scan_device.txt
    # the symbol type of a NAND is 8 and the ID should be 7
    symbol = device_scanner.get_symbol()
    assert symbol.type == 8
    assert symbol.id == device_scanner.names.lookup(["NAND"])[0]

    # The next symbol should be a COMMA
    symbol = device_scanner.get_symbol()
    assert symbol.type == device_scanner.COMMA
    # "," should not have ID
    assert symbol.id is None

    # The next symbol should be "12" from scan_device.txt
    symbol = device_scanner.get_symbol()
    assert symbol.type == device_scanner.NUMBER
    assert symbol.id == '12'

    # The next symbol should be ";" from scan_device.txt
    symbol = device_scanner.get_symbol()
    assert symbol.type == device_scanner.SEMICOLON
    # ';' should not have ID
    assert symbol.id is None

    # The next symbol should be EOF, i.e. ""
    symbol = device_scanner.get_symbol()
    assert symbol.type == device_scanner.EOF


def test_skip_space(device_scanner):
    """Test the skip whitespace functionality of scanner class"""
    device_scanner.skip_space()
    print(device_scanner.current_character)
    assert device_scanner.current_character == 'D'


def test_advance(device_scanner):
    """ Test   """


def test_get_number():
    pass


def test_get_name():
    pass

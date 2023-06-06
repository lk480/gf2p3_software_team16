"""
Test Suite for scanner.py module

This tesf file contains unit tests for the scanner module. It verifies
the functionality of the Scanner class in scanning input files and
producing symbols.

Fixtures:
- new_names(): Returns a new Names() instance. Used as a shorthand for
  instantiating Names() when defining other functions.
- new_symbol(): Returns a new Symbol() instance. Used as a shorthand for
  instantiating Symbol() when defining other functions.
- file_path(): Returns the absolute path of scan_device.txt. Used as a test
  file to check the scanner's functionality.
- new_scanner(file_path, new_names): Returns a new Scanner() instance
  that can scan the type_nand.txt file. Used in tests to verify the
  scanner's functionality.

Tests:
- test_init_raises_exception(new_names, file_path): Verifies that when
  supplied with a non-existing file path, the __init__() method in
  Scanner() raises a FileNotFoundError.
- test_scanner_init(new_scanner, new_names): Verifies that the __init__()
  method in Scanner() initializes all the correct arguments, including
  keywords, symbols, and devices.
- test_get_symbol(new_scanner): Verifies the functionality of the
  get_symbol() method in Scanner(), which translates the next sequence
  of characters into a symbol using the Symbol() class.
 - test_skip_space(new_scanner): Verifies the functionality of the skip_space()
  method in Scanner() which skips whitespace characters and returns the
  next-non whitespace character
 - advance(new_scanner):
 - get_number(new_scanner):
 - get_name(new_scanner):
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
def new_scanner(file_path_scan_device, new_names):
    """Returns a new Scanner() instance which will be able to
    scan the scan_device.txt file. This is later used in tests
    to see if the scanner works correctly."""
    return Scanner(file_path_scan_device, new_names)


def test_init_raises_exception(new_names, file_path_scan_device):
    """Tests if when supplied a non existing file path
    the __init__() method in Scanner() raises a "FileNotFoundError".
    """
    with pytest.raises(FileNotFoundError):
        Scanner(Path('unknown.bla'), new_names)
    with pytest.raises(FileNotFoundError):
        Scanner(Path('unknown.txt'), new_names)


def test_scanner_init(new_scanner, new_names):
    """Tests if the __init__() method in Scanner()
    initializes all the correct arguments such as keywords,
    symbols and devices. To see how __init()__ works go to scanner.py.
    """
    assert isinstance(new_scanner, Scanner)
    assert new_scanner.current_character == ' '
    assert new_scanner.keywords_list == ['DEVICE', 'CONNECT', 'MONITOR',
                                         'TYPE', 'STATE', 'INPUTS', 'NONE']

    assert new_scanner.symbol_type_list == range(12)
    assert new_scanner.COMMA in new_scanner.symbol_type_list
    assert new_scanner.EQUALS in new_scanner.symbol_type_list
    assert new_scanner.DOT in new_scanner.symbol_type_list
    assert new_scanner.OPENBRACKET in new_scanner.symbol_type_list
    assert new_scanner.CLOSEDBRACKET in new_scanner.symbol_type_list
    assert new_scanner.KEYWORD in new_scanner.symbol_type_list
    assert new_scanner.NUMBER in new_scanner.symbol_type_list
    assert new_scanner.NAME in new_scanner.symbol_type_list
    assert new_scanner.EOF in new_scanner.symbol_type_list
    assert new_scanner.COLON in new_scanner.symbol_type_list
    assert new_scanner.HASH in new_scanner.symbol_type_list

    assert [new_scanner.DEVICE_ID] == new_scanner.names.lookup(['DEVICE'])
    assert [new_scanner.CONNECT_ID] == new_scanner.names.lookup(['CONNECT'])
    assert [new_scanner.MONITOR_ID] == new_scanner.names.lookup(['MONITOR'])
    assert [new_scanner.TYPE_ID] == new_scanner.names.lookup(['TYPE'])
    assert [new_scanner.STATE_ID] == new_scanner.names.lookup(['STATE'])
    assert [new_scanner.INPUTS_ID] == new_scanner.names.lookup(['INPUTS'])
    assert [new_scanner.NONE_ID] == new_scanner.names.lookup(['NONE'])


def test_get_symbol(new_scanner):
    """Tests the Scanner().get_symbol() method. The method
    translates the sequence of characters into a symbol,
    which is an instance of the class Symbol(). 
    """
    # The first symbol should be "DEVICE" from scan_device.txt
    # As this is is a KEYWORD we must check its type and ID
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.KEYWORD
    assert symbol.id == new_scanner.DEVICE_ID

    # The next symbol should be ":" from scan_device.txt
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.COLON
    # ":" should not have ID
    assert symbol.id is None

    # The next symbol should be the alphanumeric string 'G1' from scan_device.txt
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.NAME
    assert symbol.type == 8
    # "G1" should not have ID
    print(symbol.id)

    # The next symbol should be a COMMA
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.COMMA
    # "," should not have ID
    assert symbol.id is None

    # The next symbol should be "NAND" from scan_device.txt
    # the symbol type of a NAND is 8 and the ID should be 7
    symbol = new_scanner.get_symbol()
    assert symbol.type == 8
    assert symbol.id == new_scanner.names.lookup(["NAND"])[0]

    # The next symbol should be a COMMA
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.COMMA
    # "," should not have ID
    assert symbol.id is None

    # The next symbol should be "12" from scan_device.txt
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.NUMBER
    assert symbol.id == '12'

    # The next symbol should be ";" from scan_device.txt
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.SEMICOLON
    # ';' should not have ID
    assert symbol.id is None

    # The next symbol should be EOF, i.e. ""
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.EOF


def test_skip_space(new_scanner):
    """Test the skip whitespace functionality of scanner class"""
    new_scanner.skip_space()
    print(new_scanner.current_character)
    assert new_scanner.current_character == 'D'


def test_advance(new_scanner):
    """ Test   """


def test_get_number():
    pass


def test_get_name():
    pass

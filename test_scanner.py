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
def file_path():
    """Returns the absolute path of type_nand.txt. We will use
    this file as a test to see if the scanner works correctly.
    type_nand.txt contains a single line saying:
    TYPE(NAND)
    """
    path = Path.cwd() / "definition_files" / "scanner_test_files" \
        / "type_nand.txt"
    return path


@pytest.fixture
def new_scanner(file_path, new_names):
    """Returns a new Scanner() instance which will be able to
    scan the type_nand.txt file. This is later used in tests
    to see if the scanner works correctly."""
    return Scanner(file_path, new_names)


def test_init_raises_exception(new_names, file_path):
    """Tests if when supplied a non existing file path
    the __init__() method in Scanner() raises a "FileNotFoundError".
    """
    with pytest.raises(FileNotFoundError):
        Scanner(Path('not existing file.bla'), new_names)
    with pytest.raises(FileNotFoundError):
        Scanner(Path('not existing file.txt'), new_names)


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
    translates the next sequence of characters into a symbol, 
    which is an instance of the class Symbol().
    """
    # The first symbol should be "TYPE" from type_nand.txt
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.KEYWORD
    assert symbol.id == new_scanner.TYPE_ID

    # The next symbol shoud be "(" in type_nand.txt
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.OPENBRACKET
    # "(" shoudln't have id
    assert symbol.id is None

    # The next symbol should be "NAND" in type_nand.txt
    # the symbol type of a NAND is 8 and the id should be 7
    symbol = new_scanner.get_symbol()
    assert symbol.type == 8
    assert symbol.id == new_scanner.names.lookup(["NAND"])[0]

    # The next symbol should be ")" in test_circuit.txt
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.CLOSEDBRACKET

    # The next symbol should be nothing, i.e. ""
    # so check if EOF is reached
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.EOF

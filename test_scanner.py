import pytest
from pathlib import Path
from names import Names
from scanner import Symbol
from scanner import Scanner


@pytest.fixture
def new_names():
    """Return a names instance."""
    return Names()


@pytest.fixture
def new_symbol():
    """Returns a new symbol instance."""
    return Symbol()


@pytest.fixture
def file_path_test_circuit():
    """Returns the absolute path of test_circuit.txt."""
    return Path.cwd() / "text files for pytest" / "scanner tests" / "type_nand.txt"


@pytest.fixture
def file_path_test_connection():
    """Returns the absolute path of test_connection.txt."""
    return Path.cwd() / "text files for pytest" / "scanner tests" / "connection.txt"


@pytest.fixture
def new_scanner(file_path_test_circuit, new_names):
    """Returns a new scanner instance."""
    return Scanner(file_path_test_circuit, new_names)


#@pytest.fixture
#def next_symbol(new_scanner):
#    """Returns the next symbol in the scanner."""
#    return new_scanner.get_symbol()


def test_init_raises_exception(new_names, file_path_test_circuit):
    """Tests if when supplied a non existing file path
    the __init__ function raises an IOError.
    """
    with pytest.raises(FileNotFoundError):
        Scanner(Path('not existing file.bla'), new_names)

    # with pytest.raises(TypeError):
    #    Scanner(file_path_test_circuit, 'Not a instance of class names')


def test_scanner_init(new_scanner, new_names):
    """Tests if the __init__ of scanner contains correct arguments."""
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
    """Tests the get_symbol methods in Scanner."""

    symbol = new_scanner.get_symbol()
    # The symbol should be "TYPE" from test_circuit.txt
    assert symbol.type == new_scanner.KEYWORD
    assert symbol.id == new_scanner.TYPE_ID
    # The next symbol shoud be "(" in test_circuit.txt
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.OPENBRACKET
    # "(" shoudln't have id
    assert symbol.id is None
    # The next symbol should be "NAND" in test_circuit.txt
    symbol = new_scanner.get_symbol()
    print(f'NAND symbol id: {symbol.id}, symbol type {symbol.type}')
    
    # TODO(optional): Figure out what should the bellow assert give
    # assert symbol.type == 8
    # assert symbol.id == new_scanner.NAND_ID
    # The next symbol should be ")" in test_circuit.txt
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.CLOSEDBRACKET
    # The next symbol should be nothing, i.e. "", so EOF is reached
    symbol = new_scanner.get_symbol()
    assert symbol.type == new_scanner.EOF

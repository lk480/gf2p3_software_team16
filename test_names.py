import pytest

from names import Names
from devices import Device


@pytest.fixture
def new_device():
    """Returns a new Device instace."""
    return Device()


@pytest.fixture
def new_names():
    """Return a new Names() instance."""
    return Names()


@pytest.fixture
def name_string_list():
    """Return a list of peoples names."""
    return ["Alice", "Bob", "Charlie"]


@pytest.fixture
def used_names(name_string_list):
    """Return a Names() instance with three names added to the
    names list.
    """
    my_name = Names()
    my_name.lookup(name_string_list)
    return my_name


def test_query_raises_exception(used_names):
    """Test if Names.query() raises expected exceptions inside Names class."""
    with pytest.raises(TypeError):
        used_names.query(2.5)
    with pytest.raises(TypeError):
        used_names.query(2)
    with pytest.raises(TypeError):
        used_names.query(True)


def test_lookup_raises_exception(used_names):
    """Test if Names().lookup() raises expected exceptions inside the
    Names class.
    """
    with pytest.raises(TypeError):
        used_names.lookup(2.5)
    with pytest.raises(TypeError):
        used_names.lookup(2)
    with pytest.raises(TypeError):
        used_names.lookup(True)


def test_get_name_string_raises_exceptions(used_names):
    """Test if Names().get_name_string() raises expected exceptions inside
    the Names class. The get_name_string() method accepts only
    non-negative integers.
    """
    with pytest.raises(TypeError):
        used_names.get_name_string(1.4)
    with pytest.raises(TypeError):
        used_names.get_name_string("hello")
    with pytest.raises(ValueError):
        used_names.get_name_string(-1)


@pytest.mark.parametrize("name_string, expected_name_id", [
    ("Alice", 0),
    ("Bob", 1),
    ("Charlie", 2),
    ("Dylan", None),
    ("Zak", None)
])
def test_query(used_names, new_names, expected_name_id, name_string):
    """Test if Names().query() returns the expected ID of a person inside
    the Names class.
    """
    # used_names an instance of Names class and it is prepopulated
    # with the names ["Alice", "Bob", "Charlie"]
    assert used_names.query(name_string) == expected_name_id

    # new_names an instance of Names class and it has no stored
    # names in the name_string_list
    assert new_names.query(name_string) is None


@pytest.mark.parametrize("expected_name_id, name_string_list", [
    ([0, 1, 2, 3], ["Alice", "Bob", "Charlie", "Dave"]),
    ([0, 1, 2, 3, 4], ["Oggie", "Juan", "Lolith", "Daniel", "Ankit"]),
    ([0, 1, 2], ["Zero", "Juan", "Two"]),
    ([0, 1, 2, 3, 4, 5], ['NEW_DEVICES', 'CONNECT', 'MONITOR', 'TYPE', 'STATE', 'INPUTS'])
])
def test_lookup(used_names, new_names, expected_name_id, name_string_list):
    """Test if Names().lookup() returns the expected ID if a name inside
    the Names class.
    """
    # used_names an instance of Names class and it is prepopulated
    # with the names ["Alice", "Bob", "Charlie"]
    assert used_names.lookup(name_string_list) == expected_name_id
    
    # new_names an instance of Names class and it has no stored
    # names in the name_string_list
    assert new_names.lookup(name_string_list) == \
           list(range(len(name_string_list)))


@pytest.mark.parametrize("name_id, expected_string", [
    (0, "Alice"),
    (1, "Bob"),
    (2, "Charlie"),
    (3, None)
])
def test_get_name_string(used_names, new_names, name_id, expected_string):
    """Test if Names().get_string() returns the expected name of a person
    inside the Names class.
    """
    # used_names an instance of Names class and it is prepopulated
    # with the names ["Alice", "Bob", "Charlie"]
    assert used_names.get_name_string(name_id) == expected_string
    
    # new_names an instance of Names class and it has no stored
    # names in the name_string_list
    assert new_names.get_name_string(name_id) is None

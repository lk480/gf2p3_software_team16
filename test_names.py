
import pytest
from names import Names
from devices import Device

"""
Test Suite for names.py module

This test file contains unit tests for the string manipulation utilities
contained withing the names.py module.

Fixtures:
---------
- `new_device()`: Returns a new Device instance. This will be used as a
  shorthand for instantiating `Device()` when defining other functions.

- `new_names()`: Returns a new `Names()` instance. This will be used as a
  shorthand for instantiating `Names()` when defining other functions.

- `name_string_list()`: Returns a list of names. This will be used
  for prepopulating `Names().names_list` with these names.

- `used_names(name_string_list)`: Returns a `Names()` instance with three
  names added to the names list. So now `used_names.names_list` 
  has three names.

Test Cases:
-----------
- `test_query_raises_exception(used_names)`: Test if `Names.query()` raises
  expected exceptions inside the `Names` class. `Names.query()` can only accept
  strings.

- `test_lookup_raises_exception(used_names)`: Test if `Names().lookup()` raises
  expected exceptions inside the `Names` class.

- `test_get_name_string_raises_exceptions(used_names)`: Test if
  `Names().get_name_string()` raises expected exceptions inside the `Names`
  class. The `get_name_string()` method accepts only non-negative integers.

- `test_query(used_names, new_names, expected_name_id, name_string)`: Test if
  `Names().query()` returns the expected ID of a name inside the `Names`
  class. It takes as an argument a name string and should return the ID of the
  name inside `Names().name_string_list`.

- `test_lookup(used_names, new_names, expected_name_id, name_string_list)`: 
   Test if `Names().lookup()` returns the expected ID of a name inside the
   `Names` class. `Names().lookup()` gets a list of non-negative indices and
   returns a list of name strings.

- `test_get_name_string(used_names, new_names, name_id, expected_string)`: Test
  if `Names().get_name_string()` returns the expected name inside
  the `Names` class. Each name should be stored in the list
  `Names().name_string_list`.
"""


@pytest.fixture
def new_device():
    """Returns a new Device instance. This will be used
    as a shorthand for instantiating Device() when defining
    other functions.
    """
    return Device()


@pytest.fixture
def new_names():
    """Return a new Names() instance. This will be used
    as a shorthand for instantiating Names()
    when defining other functions.
    """
    return Names()


@pytest.fixture
def name_string_list():
    """Returns a list of names. This will be used for
    prepopulating Names().names_list with these test names.
    """
    return ["Alice", "Bob", "Charlie"]


@pytest.fixture
def used_names(name_string_list):
    """Return a Names() instance with three names added to
    names list. So now used_names.names_list has three names.
    """
    my_name = Names()
    my_name.lookup(name_string_list)
    return my_name


def test_query_exceptions(used_names):
    """Test if Names.query() raises expected exceptions inside the
    Names class. Names.query() can only accept strings.
    """
    # Check with int
    with pytest.raises(TypeError):
        used_names.query(2)
    # Check with float
    with pytest.raises(TypeError):
        used_names.query(2.5)
    # Check with bool
    with pytest.raises(TypeError):
        used_names.query(True)
    # Check with a None
    with pytest.raises(TypeError):
        used_names.query(None)


def test_lookup_exceptions(used_names):
    """Test if Names().lookup() raises expected exceptions inside the
    Names class.
    """
    # Check with float
    with pytest.raises(TypeError):
        used_names.lookup(2.5)
    # Check with int
    with pytest.raises(TypeError):
        used_names.lookup(2)
    # Check with bool
    with pytest.raises(TypeError):
        used_names.lookup(True)
    # Check with None
    with pytest.raises(TypeError):
        used_names.lookup(None)


def test_get_name_string_raises_exceptions(used_names):
    """Test if Names().get_name_string() raises expected exceptions inside
    the Names class. The get_name_string() method accepts only
    non-negative integers.
    """
    # Check with float
    with pytest.raises(TypeError):
        used_names.get_name_string(1.4)
    # Check with str
    with pytest.raises(TypeError):
        used_names.get_name_string("hello")
    # Check with negative ID
    with pytest.raises(ValueError):
        used_names.get_name_string(-1)
    # Check with None
    with pytest.raises(TypeError):
        used_names.get_name_string(None)


@pytest.mark.parametrize("name_string, expected_name_id", [
    ("Alice", 0),
    ("Bob", 1),
    ("Charlie", 2),
    ("Dylan", None),
    ("Zak", None)
])
def test_query(used_names, new_names, expected_name_id, name_string):
    """Test if Names().query() returns the expected ID of a person inside
    the Names class. It takes as argument a name string and should return
    the id of the name inside of Names().name_string_list
    """

    """ used_names is an instance of Names class and it is prepopulated
    with the names ["Alice", "Bob", "Charlie"] """

    assert used_names.query(name_string) == expected_name_id

    """ new_names an instance of Names class and it has no stored
    names in the name_string_list """

    assert new_names.query(name_string) is None


@pytest.mark.parametrize("expected_name_id, name_string_list", [
    ([0, 1, 2, 3], ["Alice", "Bob", "Charlie", "Dave"]),
    ([0, 1, 2, 3, 4], ["Oggie", "Juan", "Lolith", "Daniel", "Ankit"]),
    ([0, 1, 2], ["Zero", "Juan", "Two"]),
    ([0, 1, 2, 3, 4, 5], ['NEW_DEVICES', 'CONNECT', 'MONITOR',
                          'TYPE', 'STATE', 'INPUTS']),
    ([0, 1, 2, 3], ["0", "1", "2", "3"])
])
def test_lookup(used_names, new_names, expected_name_id, name_string_list):
    """Test if Names().lookup() returns the expected ID of a name inside
    the Names class. Names().lookup() gets a list of non-negative indices
    and retuns a list of name strings.
    """

    # used_names an instance of Names class and it is prepopulated
    # with the names ["Alice", "Bob", "Charlie"]
    assert used_names.lookup(name_string_list) == expected_name_id

    # new_names an instance of Names class and it has no stored
    # names in the name_string_list,
    # so new_names.lookup(name_string_list) should retuns indexies
    assert new_names.lookup(name_string_list) == \
        list(range(len(name_string_list)))


def test_lookup_append(used_names):
    """Checks that lookup appends a name if not already
        present in names_list """
    current_length = len(used_names.names_list)
    used_names.lookup(['Dave'])
    updated_length = len(used_names.names_list)
    assert updated_length == current_length + 1


def test_lookup_unique_ids(used_names, name_string_list):
    """Checks that lookup has assigned unique IDs to each name
    within the name_string_list"""
    for i in range(0, 2):
        for j in range(0, 2):
            if i != j:
                assert (
                    used_names.query(name_string_list[i]) !=
                    used_names.query(name_string_list[j])
                )
            elif i == j:
                assert (
                    used_names.query(name_string_list[i]) ==
                    used_names.query(name_string_list[j])
                )
            else:
                raise IndexError('Unknown ID')


def test_method_types(used_names, name_string_list):
    """Check whether lookup and query are retuning the expected types """
    for i in range(0, 2):
        assert type(used_names.query(name_string_list[i])) is int
        assert type(used_names.lookup(name_string_list)[i]) is int


@pytest.mark.parametrize("name_id, expected_string", [
    (0, "Alice"),
    (1, "Bob"),
    (2, "Charlie"),
    (3, None),
    (4, None)
])
def test_get_name_string(used_names, new_names, name_id, expected_string):
    """Test if Names().get_string() returns the expected name of a person
    inside the Names class. The name of every person should be stored in the 
    list Names().name_string_list.
    """

    # used_names an instance of Names class and it is prepopulated
    # with the names ["Alice", "Bob", "Charlie"]
    assert used_names.get_name_string(name_id) == expected_string

    # new_names an instance of Names class and it has no stored
    # names in the name_string_list
    assert new_names.get_name_string(name_id) is None

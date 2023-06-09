class Names:
    """
    Map variable names and string names to unique integers.

    This class deals with storing grammatical keywords and user-defined words,
    and their corresponding name IDs, which are internal indexing integers. It
    provides functions for looking up either the name ID or the name string.
    It also keeps track of the number of error codes defined by other classes,
    and allocates new, unique error codes on demand.

    Parameters
    ----------
    No parameters.

    Public methods
    -------------
    unique_error_codes(self, num_error_codes): Returns a list of unique integer
                                               error codes.

    query(self, name_string): Returns the corresponding name ID for the
                        name string. Returns None if the string is not present.

    lookup(self, name_string_list): Returns a list of name IDs for each
                        name string. Adds a name if not already present.

    get_name_string(self, name_id): Returns the corresponding name string for
                        the name ID. Returns None if the ID is not present.
    """

    def __init__(self):
        # Stores the number of declared error codes
        self.error_code_count = 0
        # List of names defined in the defintion file
        self.names_list = []

    def unique_error_codes(self, num_error_codes):
        """

        Args:
            num_error_codes (list): _description_

        Raises:
            TypeError: If the type of num_error_codes is not int

        Returns:
            list: list of unique error codes
        """

        if not isinstance(num_error_codes, int):
            raise TypeError("Expected num_error_codes to be an integer.")

        self.error_code_count += num_error_codes
        return range(self.error_code_count - num_error_codes,
                     self.error_code_count)

    def query(self, name_string):
        """
    Return the corresponding name_ID for the provided name_string.

    If the name_string is not present in the names_list, return None.

    Args:
        name_string (str): The name specified in the definition file.

    Raises:
        TypeError: Type of name_string is not a string.

    Returns:
        int or None: The name ID for the provided name_string,
                    or None if the name_string is not present
                    in the names_list.
    """
        if not isinstance(name_string, str):
            raise TypeError("Expected name_string to be a string.")

        if name_string in self.names_list:
            return self.names_list.index(name_string)
        else:
            return None

    def lookup(self, name_string_list):
        """Returns a list of corresponding name_IDs for provided list of names.

        If name_string is not present in the names_list, add name_string to
        names_string_list, then return list of name_IDs.

        Args:
            name_string_list (list): list of name_strings

        Raises:
            TypeError: Type of name_string_list is not a list

        Returns:
            list: list of name_IDs corresponding to each name_string provided
                  in name_string_list.
        """
        # Check type of name_string_list
        if not isinstance(name_string_list, list):
            raise TypeError("Expected name_string_list to be a list.")

        # Intialise empty ids_list
        ids_list = []
        # Iterate through all name_strings and check if present in names_list
        for name_string in name_string_list:
            # If name_string not present, append to names_list
            if name_string not in self.names_list:
                self.names_list.append(name_string)
            # Append ids for each name_string in names_list to ids_list
            ids_list.append(self.names_list.index(name_string))

        return ids_list

    def get_name_string(self, name_id):
        """Return the corresponding name string for name_id.

        If the name_id is not an index in the names list, return None.

        Args:
            name_id (int): name_ID corresponding to a given name_string

        Raises:
            TypeError: Type of name_ID is not int
            ValueError: name_id is a non-negative integer

        Returns:
            str or None: The name_string for the provided name ID,
                         or None if a name_string corresponding to the
                         provided name ID cannot be found.
        """
        if not isinstance(name_id, int):
            raise TypeError("Expected name_id to be an integer.")
        elif name_id < 0:
            raise ValueError("Expected name_id to be a non-negative integer.")
        else:
            try:
                return self.names_list[name_id]
            # Catches an IndexError and instead returns None
            except IndexError:
                return None

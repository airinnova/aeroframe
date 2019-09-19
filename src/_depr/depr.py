import re


def sed_like_replace(filename, replacement_list):
    """
    Replace expressions in a "sed"-like style

    Args:
        :filename: name of file to modify
        :replacement_list: list of lists, each entry with ["old", "new"]
    """

    with open(filename, "r") as fp:
        lines = fp.readlines()

    with open(filename, "w") as fp:
        for line in lines:
            mod_line = string_replace(replacement_list, line)
            fp.write(mod_line)


def string_replace(replacement_list, string):
    """
    Replace multiple expressions in a string

    Args:
        :replacement_list: list of lists, each entry with ["old", "new"]
        :string: string to modify

    Returns:
        :mod_string: modified string
    """

    for replacement in replacement_list:
        orig, new = replacement
        string = re.sub(orig, new, string)

    return string


def is_string_in_file(string, filepath):
    """
    Check if a string is in a file

    Args:
        :string: string to search for
        :filepath: path of file

    Returns:
        :is_found: True if found, False otherwise
    """

    if string in open(filepath).read():
        return True

    return False

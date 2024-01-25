# Brandon Kong's String Parsing
# Motorola_Brainstem 2024

from typing import List


def string_to_int_list(string_as_list: str) -> List[int]:
    """
    Converts a string of format "[a1,b1,c1,d1,e1]" to a list of lists
    :param string_as_list: A string of format "[1,2,3]"
    :return: A list of integers
    """

    # Remove brackets at the end of they exist

    string_as_list = string_as_list.replace("[", "").replace("]", "").replace(" ", "")

    split_string = string_as_list.split(",")

    return list(map(int, split_string))

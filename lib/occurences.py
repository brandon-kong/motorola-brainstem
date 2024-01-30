# Brandon Kong's Occurences of Cluster Numbers
# Motorola_Brainstem 2024

from typing import List, Dict, OrderedDict
from collections import Counter, OrderedDict


def get_occurence_dict (list: List[int]) -> OrderedDict[int, int]:
    """
    Gets the occurences of each number in a list
    :param list: A list of integers
    :return: A dictionary of the occurences of each number in the list
    """

    counted_dict = dict(Counter(list))

    # Sort the dictionary by key
    sorted_dict = OrderedDict(sorted(counted_dict.items()))

    return sorted_dict

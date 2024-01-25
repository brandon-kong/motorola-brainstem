# Brandon Kong's Occurences of Cluster Numbers
# Motorola_Brainstem 2024

from typing import List, Dict

def get_occurence_dict (list: List[int]) -> Dict[int, int]:
    """
    Gets the occurences of each number in a list
    :param list: A list of integers
    :return: A dictionary of the occurences of each number in the list
    """

    occurence_dict = {}

    for i in range(len(list)):
        a = occurence_dict.get(list[i])

        if (a is None):
            occurence_dict[list[i]] = 1
        else:
            occurence_dict[list[i]] = occurence_dict[list[i]] + 1

    return occurence_dict
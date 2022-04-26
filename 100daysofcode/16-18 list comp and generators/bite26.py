# Bite 26. Dictionary comprehensions are awesome 
# A dictionary comprehension is like a list comprehension, but it constructs a dict instead of a list. They are convenient to quickly operate on each (key, value) pair of a dict. And often in one line of code, maybe two after checking PEP8 ;)

# We think they are elegant, that's why we want you to know about them!

# In this Bite you are given a dict and a set. Write a dictionary comprehension that filters out the items in the set and returns the resulting dict, so if your dict is {1: 'bob', 2: 'julian', 3: 'tim'} and your set is {2, 3}, the resulting dict would be {1: 'bob'}.


from typing import Dict, Set

DEFAULT_BITES = {
    6: "PyBites Die Hard",
    7: "Parsing dates from logs",
    9: "Palindromes",
    10: "Practice exceptions",
    11: "Enrich a class with dunder methods",
    12: "Write a user validation function",
    13: "Convert dict in namedtuple/json",
    14: "Generate a table of n sequences",
    15: "Enumerate 2 sequences",
    16: "Special PyBites date generator",
    17: "Form teams from a group of friends",
    18: "Find the most common word",
    19: "Write a simple property",
    20: "Write a context manager",
    21: "Query a nested data structure",
}
EXCLUDE_BITES = {6, 10, 16, 18, 21}


def filter_bites(
    bites: Dict[int, str] = DEFAULT_BITES,
    bites_done: Set[int] = EXCLUDE_BITES
) -> Dict[int, str]:
    """
    Return the bites dict with bites_done filtered out.
    """
    return {num: bite for num, bite in bites.items() if num not in bites_done}

# another way
    for d in exclude_bites:
        bites.pop(d)
    return bites

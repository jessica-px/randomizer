"""
This file contains the main logic for the RandomList class and
the helper functions it uses
"""

import typing as t
import random
from copy import deepcopy

# ------------------------------------------------- #
#                        Helpers                    #
# ------------------------------------------------- #


def format_list(input_list: t.List[t.Any]) -> t.List[t.Dict]:
    '''
    Given a list, for each item, adds a "probability" of 1 if key isn't present,
    then sorts list by probability value
    '''
    formatted_list = []
    for item in input_list:
        if isinstance(item, dict) and "probability" in item and "item" in item:
            formatted_list.append(item)
        else:
            new_item = {
                "item": item,
                "probability": 1
            }
            formatted_list.append(new_item)
    return sorted(formatted_list, key=lambda k: k['probability'], reverse=True)


def format_list_probabilities(input_list: t.List[t.Dict]) -> t.List[t.Dict]:
    '''
    Given a formatted list, formats it (again) so the probabilities are cumulatively weighed
    Ex: Given items with probabilties of 10 and 20, it will return items
    with probabilities of 10 and 30 (10+20).
    '''
    cumulative_probability = 0
    new_list = []
    for item in input_list:
        new_item = item.copy()
        cumulative_probability += new_item["probability"]
        new_item["probability"] = cumulative_probability
        new_list.append(new_item)
    return new_list


def get_from_list(target: int, input_list: t.List[t.Dict]) -> t.Dict:
    '''
    Given a "target", returns the first item in formatted list with a greater probability
    Ex: Item A has a probability of 20 and Item B has 50. Our target is 32, so we return Item B.
    '''
    for item in input_list:
        if target <= item["probability"]:
            return item
    raise IndexError(f'Nothing found in list matching probability value of {target}.')


def deepcopy_list(input_list: t.List[t.Dict]) -> t.List[t.Dict]:
    '''
    Returns a deepcopy of a list of dictionaries
    '''
    new_list = []
    for dict_item in input_list:
        new_dict = deepcopy(dict_item)
        new_list.append(new_dict)
    return new_list

# ------------------------------------------------- #
#                        Class                      #
# ------------------------------------------------- #


class RandomList:
    '''
    A class for getting random results from a list.

    Items in this list can either given in the following format:
        {
            "item": (the actual thing you want),
            "probability": (an int representing the comparative probability)
        }

    If given in any other format, items will be auto-formatted and provided
    a probability of 1.

    Public Attributes
    ----------
    contents : List[t.Dict]
        A list of items, with weighted probabilities (defaults to 1)

    Public Methods
    -------
    get_random():
        Returns a random item from self.contents
    get_random_and_remove():
        Returns a random item from self.contents and decreases its probability by 1
    reset_contents():
        Returns contents to their original state
    get_all_items():
        Returns a list of all possible items in RandomList

    '''

    def __init__(self, input_list: t.List[t.Any]):
        self.contents = format_list(deepcopy_list(input_list))
        self._offset_contents = format_list_probabilities(self.contents)
        self._original_contents = deepcopy_list(self.contents)

    def _get_item_index(self, input_item: t.Any):
        for item in self.contents:
            if item["item"] == input_item:
                return self.contents.index(item)
        raise IndexError(f'Could not find index of list item {input_item}.')

    def _adjust_probability(self, target_item: t.Dict, adjustment_amount: int):
        target_index = self._get_item_index(target_item)
        self.contents[target_index]["probability"] += adjustment_amount
        # Remove from list if prob becomes 0
        if self.contents[target_index]["probability"] <= 0:
            del self.contents[target_index]
        self._offset_contents = format_list_probabilities(self.contents)

    def _get_random_probability(self):
        range_max = self._offset_contents[-1]["probability"]
        return random.randint(1, range_max)

    def get_random(self):
        '''
        Returns a random item from self.contents
        '''
        if len(self.contents) == 0:
            raise IndexError('RandomList is empty!')
        target_probability = self._get_random_probability()
        return get_from_list(target_probability, self._offset_contents)["item"]

    def get_random_and_remove(self):
        '''
        Returns a random item from self.contents and decreases its probability by 1
        If its probability reaches 0, it is removed from the list
        '''
        if len(self.contents) == 0:
            raise IndexError('RandomList is empty!')
        target_probability = self._get_random_probability()
        random_item = get_from_list(target_probability, self._offset_contents)["item"]
        self._adjust_probability(random_item, -1)
        return random_item

    def reset_contents(self):
        '''
        Returns contents to their original state, resetting all probability values
        and replacing any removed items
        '''
        self.contents = self._original_contents
        self._offset_contents = format_list_probabilities(self.contents)

    def get_all_items(self):
        '''
        Returns a list of all possible items in RandomList
        '''
        return [item["item"] for item in self.contents]

class RandomGroup:
    '''
    Very much like a RandomList, except it's a collection of RandomLists. They can
    be given comparative probabilities like follows:

        {
            "item": (your RandomList),
            "probability": (an int representing the comparative probability)
        }

    Otherwise the RandomLists will be auto-formatted and each given a probability of 1.

    Public Attributes
    ----------
    lists : List[t.Dict]
        A list of RandomLists, with weighted probabilities (defaults to 1)

    Public Methods
    -------
    get_random():
        Randomly selects a RandomList from self.lists, then returns a random item from that list
    get_all_lists():
        For each list in self.lists, returns a list of its items
    '''

    def __init__(self, input_lists: t.List[t.Type[RandomList]]):
        self.lists = format_list(input_lists)
        self._offset_lists = format_list_probabilities(self.lists)
        self._original_lists = deepcopy_list(self.lists)

    def _get_random_probability(self):
        range_max = self._offset_lists[-1]["probability"]
        return random.randint(1, range_max)

    def get_random(self):
        '''
        Selects a RandomList from self.lists, then returns a random item from its contents
        by calling the RandomList's own get_random() method
        '''
        if len(self.lists) == 0:
            raise IndexError('RandomGroup is empty!')
        target_probability = self._get_random_probability()
        random_list = get_from_list(target_probability, self._offset_lists)["item"]
        return random_list.get_random()

    def get_all_lists(self):
        '''
        For each list in self.lists, returns a list of its items
        '''
        return [random_list["item"].get_all_items() for random_list in self.lists]

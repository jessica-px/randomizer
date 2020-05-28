import typing as t
import random


# ------------------------------------------------- #
#                        Helpers                    #
# ------------------------------------------------- #

# Given a list, for each item, adds a "probability" of 1 if key isn't present
# then sorts list by probability value
def format_list(input_list: t.List[t.Any]) -> t.List[t.Dict]:
    formatted_list = []
    for item in input_list:
        if type(item) is dict and "probability" in item:
            formatted_list.append(item)
        else:
            new_item = {
                "item": item,
                "probability": 1
            }
            formatted_list.append(new_item)
    return sorted(formatted_list, key=lambda k: k['probability'], reverse=True)


# Given a formatted list, formats it (again) so the probabilities are cumulatively weighed
# Ex: Given items with probabilties of 10 and 20, it will return items
# with probabilities of 10 and 30 (10+20).
def format_list_probabilities(input_list: t.List[t.Dict]) -> t.List[t.Dict]:
    cumulative_probability = 0
    new_list = []
    for item in input_list:
        new_item = item.copy()
        cumulative_probability += new_item["probability"]
        new_item["probability"] = cumulative_probability
        new_list.append(new_item)
    return new_list

# Given a "target", returns the first item in formatted list with a greater probability
# Ex: Item A has a probability of 20 and Item B has 50. Our target is 32, so we return Item B.
def get_from_list(target: int, input_list: t.List[t.Dict]) -> t.Dict:
    for item in input_list:
        if target <= item["probability"]:
            return item
    raise IndexError(f'Nothing found in list matching probability value of {target}.')

# ------------------------------------------------- #
#                        Class                      #
# ------------------------------------------------- #

class RandomList:
    def __init__(self, contents: t.List[t.Any]):
        self.contents = format_list(contents)
        self.offset_contents = format_list_probabilities(self.contents)

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
        self.offset_contents = format_list_probabilities(self.contents)

    def _get_random_probability(self):
        max = self.offset_contents[-1]["probability"]
        return random.randint(1, max)

    def get_random(self):
        target_probability = self._get_random_probability()
        return get_from_list(target_probability, self.offset_contents)["item"]

    def get_random_and_remove(self):
        target_probability = self._get_random_probability()
        random_item = get_from_list(target_probability, self.offset_contents)["item"]
        self._adjust_probability(random_item, -1)
        return random_item

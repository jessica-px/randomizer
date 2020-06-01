# Randomizer

A small library that simplifies randomly selecting things from lists.

## RandomList

RandomList is a class that collects together the pool of items that you want to be able to randomly select from. You can think of it as the "hat" from which your options will be drawn.

### Simple Definition

The simplest way of defining a RandomList is with a flat list:

```python
from randomizer import RandomList

flavor_list = RandomList(['vanilla', 'chocolate', 'strawberry'])
random_flavor = flavor_list.get_random()
```

Each item in a RandomList is given a `probability` value, which is by default set to `1`. The odds of an item being selected are equal to `item probability / sum of all probabilities`.

Since each item in this RandomList is given a probability of `1`, they each have an equal chance of being returned by `get_random()`.

### Custom Probabilities

You can declare your own probability values for the items in your RandomList by using a list of dictionaries. Each dictionary must have an `item` key and a `probability` key, as follows:

```python
from randomizer import RandomList

flavor_list = RandomList([
    {
      "item": "vanilla",
      "probability": 3
    },
    {
      "item": "chocolate",
      "probability": 11
    }
])
random_flavor = flavor_list.get_random()
```

In this example, `vanilla` has a probability of `3`, while `chocolate` has `11`. The sum of all the probability values is `14`, meaning `vanilla` has a 3/14 chance of being returned (~21%), while `chocolate` has 11/14 (~79%).

If you want to work directly with percent values as inputs, just make sure that the sum of all probabilities equals 100, as shown below:

```python
from randomizer import RandomList

flavor_list = RandomList([
    {
      "item": "vanilla",
      "probability": 20
    },
    {
      "item": "chocolate",
      "probability": 80
    }
])
random_flavor = flavor_list.get_random()
```

Now `vanilla` has a 20/100 (20%) chance of being returned, while `chocolate` has an 80/100 (80%) chance. But you can rest assured that if your total probability ends up above or below 100, no errors will occur.

### Viewing RandomLists

You can view the contents of your RandomList in JSON format with the `get_contents()` method.

```python
print(flavor_list.get_contents())
# Output:
# {
#   "item": "vanilla",
#   "probability": 20
# },
# {
#   "item": "chocolate",
#   "probability": 80
# }
```

`get_contents()` will return the full contents of your RandomList, including any probability values. If you only want to see a list of the items in the RandomList, you can use `get_items()`:

```python
print(flavor_list.get_items())
# Output:
# ['vanilla', 'chocolate']
```

You can also view the current number of items in your RandomList with `item_count()`:

```python
print(flavor_list.item_count())
# Output: 2
```

### Diminishing Probability

RandomLists can also operate like “raffle buckets”. Imagine each “probability” point is a ticket that’s been entered into a raffle -- whenever an item is selected with the `get_random_and_remove()` method, one of its “tickets” is removed, and its probability is decreased by one.

In this example, there are a total of six “tickets”. We begin with a 1/6 chance of getting `vanilla`. When we select an item with `get_random_and_remove()`, this number will change:

```python
flavor_list = RandomList([
    {
      "item": "vanilla",
      "probability": 5
    },
    {
      "item": "chocolate",
      "probability": 1
    }
])
```

```python
random_flavor = flavor_list.get_random_and_remove()
print(random_flavor)
# Output: "vanilla"
print(flavor_list.view_contents())
# Output:
# {
#   "item": "vanilla",
#   "probability": 4
# },
# {
#   "item": "chocolate",
#   "probability": 1
# }
```

Running `get_random_and_remove()` returned `vanilla`, and also decreased the probability for `vanilla` from `6` to `5`. The next time we run `get_random_and_remove()`, we will have a 1/5 chance of getting `vanilla`.

When the probability of an item hits 0, it is removed from the RandomList and can no longer be returned. 

### Resetting RandomLists

You can return a RandomList to its initial state with `reset_contents()`:

```python
flavor_list = RandomList(['vanilla', 'chocolate', 'strawberry'])
random_flavor = flavor_list.get_random_and_remove()
print(random_flavor)
# Output: "vanilla"
print(flavor_list.view_items())
# Output: ["chocolate", "strawberry"]
flavor_list.reset_contents()
print(flavor_list.view_items())
# Output: ["vanilla", "chocolate", "strawberry"]
```

`reset_contents()` sets all probabilities to their initial values and replaces any items that may have been removed.

## RandomGroups

Perhaps you don’t just want to randomly pull from one list -- maybe you want a chance for your item to come from several different lists. You can do this by defining a RandomGroup, which is essentially a "list of lists".

```python
from randomizer import RandomList, RandomGroup

flavor_group = RandomGroup([
  {
    "list": common_flavor_list,
    "probability": 70
  },
  {
    "list": uncommon_flavor_list,
    "probability": 30
  }
])
random_food = food_group.get_random()
```

When we call `flavor_group.get_random()`, first it selects a RandomList based on the given probability, then it looks inside that RandomList and returns an item by calling its `RandomList.get_random()`.

In this example, we have a 30% chance of selecting the `uncommon_flavor_list`. Let’s assume it looks like this:

```python
uncommon_flavor_list = RandomList(["pistachio", "mocha chip", "praline pecan"])
```

Once this RandomList is selected, `uncommon_flavor_list.get_random()` will run. In this case, each item in this list has a default probability of 1/3.

So ultimately, when we call `flavor_group.get_random()`, `"pistachio"`, `"mocha chip"`, and `"praline pecan"` each have a 10% chance of being returned.


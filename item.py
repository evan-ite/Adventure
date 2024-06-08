"""
item.py

Elise van Iterson, 11907223
13 - 12 - 2022

This file contains an Item class to use with Crowthers Adventure game.
The class is used to keep track of an inventory with items and their description.
"""


class Item():
    """ Item class that implements a dictionary with items plus description. """

    def __init__(self) -> None:
        """ Initialize inventory. """
        self.inventory: dict[str, str] = {}

    def add_item(self, key: str, description: str) -> None:
        """ Add item to inventory. """
        self.inventory[key] = description

    def drop_item(self, key: str) -> None:
        """ Remove item from inventory. """
        del self.inventory[key]

    def search(self, key: str) -> bool:
        """ Check if item is in inventory. """
        if key in self.inventory:
            return True
        return False

    def empty(self) -> bool:
        """ Check if inventory is empty. """
        if len(self.inventory) > 0:
            return False
        return True

    def __str__(self) -> str:
        """ Print elements from inventory. """
        final_string: list[str] = []
        for key in self.inventory.keys():
            final_string.append("{}: {}".format(key, self.inventory[key]))
        return "\n".join(final_string)
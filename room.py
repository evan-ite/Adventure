"""
room.py

Elise van Iterson, 11907223
13 - 12 - 2022

This file contains a Room class to use with Crowthers Adventure game.
The class is used to load all rooms from the map of the game. All rooms
have a room ID, name, description, connections to other rooms, items and a visited status.
"""

from typing import Any


class Room():
    """ Implementation of Room class. All rooms have a room ID, name, description,
        connections to other rooms, items and a visited status. """

    def __init__(self, room_id: int, name: str, description: str) -> None:
        """ Initialize room with all characteristics"""
        self.room_id: int = room_id
        self.name: str = name
        self.description: str = description
        self.connections: dict[str, Any] = {}
        self.items: dict[str, str] = {}
        self.visited: bool = False

    def set_visited(self) -> None:
        """ Set room status to visited. """
        self.visited = True

    def is_visited(self) -> bool:
        """" Check if room is visited. """
        if not self.visited:
            return False
        return True

    def add_connection(self, direction: str, room: Any) -> None:
        """ Add connection to another room in a given direction. """

        # If there's no connection in this direction yet
        if direction not in self.connections:
            # create an empty list
            self.connections[direction] = []
            # Append room to list
            self.connections[direction].append(room)
        # If there is already a connection in this direction
        else:
            # Append room to list
            self.connections[direction].append(room)

    def has_connection(self, direction: str) -> bool:
        """ Check wether room has a specific connection. """
        if direction in self.connections:
            return True
        return False

    def get_connection(self, direction: str) -> Any:
        """ Get the connection a certain direction leads to. """
        return self.connections[direction]

    def add_item(self, key: str, description: str) -> None:
        """ Add item to room. """
        self.items[key] = description

    def remove_item(self, key: str) -> None:
        """ Remove item from room. """
        del self.items[key]

    def print_items(self) -> str:
        """ Print items in room. """
        final_string: list[str] = []

        for key in self.items.keys():
            final_string.append("{}: {}".format(key, self.items[key]))

        return "\n".join(final_string)

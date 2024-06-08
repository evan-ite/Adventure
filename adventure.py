"""
adventure.py

Elise van Iterson, 11907223
13 - 12 - 2022

This file contains an Adventure class and further code to play
Crowthers Adventure game. You should insert a datafile with
all information to load the game.

Usage: python adventure.py datafile
"""

from room import Room
from history import History
from item import Item
from typing import Any


class Adventure():
	""" Class that loads all data and implements different actions of the game. """

	def __init__(self, game: str) -> None:
		""" Create rooms and items for the appropriate 'game' version."""

		# Rooms is a dictionary that maps a room number to the corresponding room object
		self.rooms: dict[int, Room] = {}

		# Create a list to keep track of history
		self.history: History = History()

		# Create an inventory of collected items
		self.inventory: Item = Item()

		# Load room structures
		self.load_rooms(f"data/{game}Adv.dat")

		# Game always starts in room number 1, so we'll set it after loading
		assert 1 in self.rooms
		self.current_room = self.rooms[1]

	def load_rooms(self, filename: str) -> None:
		""" Load rooms from filename in three-step process. """

		# Open file
		with open(filename) as f:
			# First load the rooms into the dictionary self.rooms
			while True:
				line: str = f.readline()
				if line == '\n':
					break
				line = line.rstrip('\n')
				info: list[Any] = line.split("\t")
				new_room: Room = Room(info[0], info[1], info[2])
				self.rooms[int(info[0])] = new_room

			# Second load the connections between the rooms
			while True:
				line = f.readline()
				if line == '\n':
					break
				line = line.rstrip('\n')
				info = line.split("\t")
				source: Room = self.rooms[int(info[0])]

				for i in range(1, len(info), 2):
					# check if there's a conditional movement, add the connection
					if len(info[i + 1]) > 2:
						destination: Any = info[i + 1]
						source.add_connection(info[i], destination)
					# When there's no conditional movement, simply add the connection
					else:
						destination = self.rooms[int(info[i + 1])]
						source.add_connection(info[i], destination)

			# Third load objects to rooms
			while True:
				line = f.readline()
				if line == '':
					break
				line = line.rstrip('\n')
				info = line.split("\t")
				source = self.rooms[int(info[2])]
				source.add_item(info[0], info[1])

	def get_description(self) -> str:
		""" Pass along the description of the current room if the
			room was already visited, only the room name is returned. """
		# If room was already visited, return only room name
		if self.current_room.is_visited():
			return self.current_room.name

		# If room hasn't been visited and contains items, return description and items
		if self.current_room.items:
			return f'{self.current_room.description} \n {self.current_room.print_items()}'
		# If room doesn't contain items, return description
		return self.current_room.description

	def get_long_description(self) -> str:
		""" Pass along the description of the current room. """
		# If room contains items, return description and items
		if self.current_room.items:
			return f'{self.current_room.description} \n {self.current_room.print_items()}'
		# Otherwise just return description
		return self.current_room.description

	def move(self, direction: str) -> bool:
		""" Move to a different room by changing "current" room, if possible. """
		current: Room = self.current_room

		# Check wether direction is valid
		if not current.has_connection(direction):
			return False

		# Set room to visited and save in history
		current.set_visited()
		self.history.push(current)

		# Check if there are conditional movements
		if self.check_requirements(direction):
			requirements: dict[str, str] = self.get_requirements(direction)
			# Check what items (treasures) are in inventory
			treasures: list[str] = self.check_inventory(requirements)

			# Check if items in inventory result in conditional movement
			for i in range(0, len(requirements)):
				if list(requirements)[i] in treasures:
					key: str = list(requirements)[i]
					# Move to new room
					self.current_room = self.rooms[int(requirements[key])]
					return True

		# When there are no conditional movements or requirements aren't met
		dir_list: list[Any] = current.get_connection(direction)

		# Find the room in the list
		for dir in dir_list:
			if not type(dir) == str:
				# Move to new room
				self.current_room = dir
				return True

		# If none of the above applies
		return False

	def move_back(self) -> None:
		""" Moves user back to the previous room. """
		# Make sure current room is set to visited
		self.current_room.set_visited()
		# Set current room to previous room and remove this room from history
		self.current_room = self.history.pop()

	def check_requirements(self, direction: str) -> bool:
		""" Check if there are any conditional movements for a direction. """
		list_directions: list[Any] = self.current_room.get_connection(direction)
		if len(list_directions) > 1:
			return True
		return False

	def get_requirements(self, direction: str) -> dict[str, str]:
		""" Function that returns the items required for a conditional movement,
			mapped to the direction this conditional movement leads to. """
		list_directions: list[Any] = self.current_room.get_connection(direction)
		requirements: dict[str, str] = {}

		# Loop through all directions to find the required treasures (items) and direction
		for d in list_directions:
			treasure: str = ""
			new_direction: str = ""
			if type(d) == str:

				for char in d:
					if char.isalpha():
						# Save the required treasure
						treasure += char
					elif char.isdigit():
						# Save the direction that belongs to the item
						new_direction += char
			# Map treasure to direction
			requirements[treasure] = new_direction

		return requirements

	def check_inventory(self, requirements: dict[str, str]) -> list[str]:
		""" Compares inventory to requirements for a conditional movement.
			A list of items in inventory that match the required items is returned."""
		inventory: list[str] = []

		# Loop through the items that are required for conditional movement
		for item in requirements:
			if item in self.inventory.inventory:
				inventory.append(item)
		return inventory

	def is_forced(self) -> bool:
		""" A function to check if theres a forced direction in the current room. """
		if self.current_room.has_connection('FORCED'):
			return True
		return False

	def take_item(self, item: str) -> bool:
		""" A function to take items out of the current room and put them
			in users inventory. Returns true if action is completed, false if not. """
		# Check if item is in current room
		if item in self.current_room.items:
			item_description = self.current_room.items[item]
			# Add item to inventory and remove from room
			self.inventory.add_item(item, item_description)
			self.current_room.remove_item(item)
			return True

		# If item is not in room
		return False

	def drop_item(self, item: str) -> bool:
		""" A function to drop items from inventory and leave them in the room.
			Returns true if action is completed, false if not. """
		# Check if item is in inventory
		if self.inventory.search(item):
			item_description = self.inventory.inventory[item]
			# Add item to current room and remove from inventory
			self.current_room.add_item(item, item_description)
			self.inventory.drop_item(item)
			return True

		# If item is not in inventory
		return False


def help() -> None:
	""" Fucntion to provide user with instructions. """
	print("You can move by typing directions such as EAST/WEST/IN/OUT")
	print("QUIT quits the game.")
	print("HELP prints instructions for the game.")
	print("INVENTORY lists the item in your inventory.")
	print("LOOK lists the complete description of the room and its contents.")
	print("TAKE <item> take item from the room.")
	print("DROP <item> drop item from your inventory.")


def load_synonyms(filename: str) -> dict[str, str]:
	""" Function to load file with synonyms into dictionary. """
	synonyms: dict[str, str] = {}

	# Open file
	with open(filename) as f:
		for line in f:
			line = line.rstrip('\n')
			(key, val) = line.split('=')
			# Map key to value
			synonyms[key] = val
	# Return dictionary
	return synonyms


if __name__ == "__main__":

	from sys import argv

	# Check command line arguments
	if len(argv) not in [2]:
		print("Usage: python adventure.py [game name]")
		print("options [Crowther, Small, Tiny]")
		exit(1)

	# Load the requested game or else Tiny
	if argv[1] != "Crowther" and argv[1] != "Small" and argv[1] != "Tiny":
		print("Usage: python adventure.py [game name]")
		print("options [Crowther, Small, Tiny]")
		exit(1)
	else:
		game_name = argv[1]

	# Load synonyms for user interface
	synonyms = load_synonyms('data/Synonyms.dat')

	# Create game
	adventure = Adventure(game_name)

	# Welcome user
	print("Welcome to Adventure.\n")

	# Print very first room description
	print(adventure.get_description())

	# Prompt the user for commands until they type QUIT
	while True:

		# Prompt
		command = input("> ").upper()

		# Check if synonym is used as command
		if command in synonyms:
			command = synonyms[command]

		# Perform move or other commands
		if command == 'HELP':
			help()
		elif command == 'LOOK':
			print(adventure.get_long_description())
		elif command == 'BACK':
			adventure.move_back()
			print(adventure.get_description())
		elif command == 'QUIT':
			quit()
		elif command == 'INVENTORY':
			if adventure.inventory.empty():
				print("Your inventory is empty")
			else:
				print(adventure.inventory)
		elif 'TAKE' in command:
			if adventure.take_item(command[5:]):
				print(f'{command[5:]} taken.')
			else:
				print("No such item")
		elif 'DROP' in command:
			if adventure.drop_item(command[5:]):
				print(f'{command[5:]} dropped.')
			else:
				print("No such item")
		elif adventure.move(command):
			if adventure.is_forced():
				print(adventure.get_long_description())
				while adventure.move('FORCED'):
					pass
			print(adventure.get_description())
		else:
			print("Invalid command. ")

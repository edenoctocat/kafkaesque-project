import os
from time import sleep
import getch
import sys
import random

class Room:
	def __init__(self, width, height, level, entrance):
		self.width = width
		self.height = height
		self.level = level
		self.entrance = entrance
		self.field = [['. ' for x in range(self.width)] for y in range(self.height)]
		self.exit = random.choice([[0, 2], [0, 5], [0, 6], [0, 8], [1, 14], [3, 14], [4, 14], [6, 14], [9, 2], [9, 6], [9, 9]])
		self.coins = 0
		self.toll = False
		self.message = ''
		self.generate_field()
		self.generate_coins()

	def generate_field(self):
		for y in range(self.height):
			self.field[y][0] = '| '
			self.field[y][self.width - 1] = '| '		
		for x in range(self.width):
			self.field[0][x] = '--'
			self.field[self.height - 1][x] = '--'
		self.field[self.exit[0]][self.exit[1]] = '  '
		self.field[self.entrance[0]][self.entrance[1]] = '  '

	def generate_coins(self):
		for i in range(random.randint(2, 5)):
			self.field[random.randint(1, 8)][random.randint(1, 13)] = '$ '

	def action(self, char_position):
		if not self.message == '':
			char_reply = input(self.message)
			if self.toll:
				if char_reply == 'ok' or char_reply == 'yes' or char_reply == 'y':
					if self.coins >= self.toll:
						self.coins -= self.toll
						print('coins:', self.coins)
						char_position = list(self.newroom(char_position))
					else:
						print('you do not have enough coins to continue.')
				self.toll = False
			self.message = ''
			print(char_position)
			return char_position

	def newroom(self, char_position):
		self.level += 1
		print(self.exit)
		if self.exit[0] == 0:
			self.entrance = [9, self.exit[1]]
		elif self.exit[0] == 9:
			self.entrance = [0, self.exit[1]]
		elif self.exit[1] == 0: 
			self.entrance = [self.exit[0], 14]
		elif self.exit[1] == 14: 
			self.entrance = [self.exit[0], 0]
		print(self.entrance)
		self.exit = random.choice([[0, 2], [0, 5], [0, 6], [0, 8], [1, 14], [3, 14], [4, 14], [6, 14], [9, 2], [9, 6], [9, 9]])
		self.field = [['. ' for x in range(self.width)] for y in range(self.height)]
		self.generate_field()
		self.generate_coins()
		char_position = list(self.entrance)
		return char_position

	def render(self, char_position, char_prev_position):
		if self.field[char_position[0]][char_position[1]] == '$ ':
			self.coins += 1

		if char_position == self.exit:
			self.toll = (self.level)**2 - 2*self.level//3
			self.message = 'to continue, pay ' + str(self.toll) + ' coins \n'

		self.field[char_prev_position[0]][char_prev_position[1]] = '. '
		self.field[char_position[0]][char_position[1]] = '@ '

	def display(self):
		print('room:', self.level)
		print('coins:', self.coins)
		print(''.join([''.join(row + ['\n']) for row in self.field]))


class Character:
	def __init__(self, room):
		self.position = [1, 1]
		self.prev_position = [1, 1]
		self.direction = 'd'
		self.room = room

	def check_position(self, position, exit, entrance):
		if not(position[0] > 8 or position[1] > 13 or position[0] < 1 or position[1] < 1):
			return True
		elif position ==  exit:
			return True
		elif position ==  entrance:
			return True
		else:
			return False

	def set_direction(self, key):
		self.direction = key

	def move(self, exit, entrance):
		self.prev_position = list(self.position)

		if self.direction == 'w':
			self.position[0] -= 1
		elif self.direction == 's':
			self.position[0] += 1
		elif self.direction == 'a':
			self.position[1] -= 1
		elif self.direction == 'd':
			self.position[1] += 1

		if self.check_position(self.position, exit, entrance):
			pass
		else:
			self.position = list(self.prev_position)
def main():
	os.system('clear')
	f = open('opening-text.txt', 'r')
	print(f.read())
	f.close()
	sleep(3)
	for i in range(3):
		os.system('clear')
		print('\n' + (' ' * 36) + ('. ' * (i%3)) + 'O ' + ('. ' * (2 - i%3)))
		sleep(.5)

	os.system('clear')
	room = Room(15, 10, 1, [1, 1])
	char = Character(room.field)
	room.render(char.position, char.prev_position)
	room.display()

	print('\npress w to move up. \npress s to move down. \npress a to move left. \npress d to move right. \n\npress h for help. \npress q to quit.')
	print('\npress any key to continue...')

	rounds = 0
	ch = getch.getch()

	while ch != 'q':
		os.system('clear')
		char.set_direction(ch)
		char.move(room.exit, room.entrance)
		room.render(char.position, char.prev_position)
		room.display()
		action = room.action(char.position)
		if type(action) == list:
			char.position = list(action)
			print(char.position)
		if ch == 'h':
			print('\npress w to move up. \npress s to move down. \npress a to move left. \npress d to move right. \n\npress h for help. \npress q to quit.')
			print('\npress any key to continue...')

		ch = getch.getch()
		sleep(.2)
		rounds += 1

main()


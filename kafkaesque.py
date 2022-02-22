import os
from time import sleep
import getch
import sys
import random
import math

class Room:
	def __init__(self, width, height, level, entrance):
		self.width = width
		self.height = height
		self.level = level
		self.entrance = entrance
		self.field = [['. ' for x in range(self.width)] for y in range(self.height)]
		self.exit = random.choice([[0, 2], [0, 6], [0, 12], [2, 14], [6, 14], [9, 4], [9, 8], [9, 10], [4, 0], [8, 0]])
		self.coins = 0
		self.energy = 100
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
		for i in range(random.randint(5, 10)):
			self.field[random.randint(2, 7)][random.randint(2, 12)] = random.choice(['--', '| '])

	def generate_coins(self):
		for i in range(random.randint(3, 8)):
			self.field[random.randint(1, 8)][random.randint(1, 13)] = '$ '

	def check_toll(self, char_position):
		if not self.message == '':
			char_reply = input(self.message)
			if self.coins >= self.toll:
				self.coins -= self.toll
				print('coins:', self.coins)
				char_position = list(self.newroom(char_position))
			else:
				print('you do not have enough coins to continue.')
			self.toll = False
		self.message = ''
		return char_position

	def newroom(self, char_position):
		self.level += 1
		if self.exit[0] == 0:
			self.entrance = [9, self.exit[1]]
		elif self.exit[0] == 9:
			self.entrance = [0, self.exit[1]]
		elif self.exit[1] == 0: 
			self.entrance = [self.exit[0], 14]
		elif self.exit[1] == 14: 
			self.entrance = [self.exit[0], 0]
		self.exit = random.choice([[0, 2], [0, 6], [0, 12], [2, 14], [6, 14], [9, 4], [9, 8], [9, 10], [4, 0], [8, 0]])
		self.field = [['. ' for x in range(self.width)] for y in range(self.height)]
		self.generate_field()
		self.generate_coins()
		char_position = list(self.entrance)
		print(self.entrance, self.exit)
		return char_position

	def render(self, char_position, char_prev_position):
		if self.energy == 0:
			f = open('game-over.txt', 'r')
			print(f.read())
			f.close()
			sys.exit()

		if self.field[char_position[0]][char_position[1]] == '$ ':
			self.coins += 1

		if char_position == self.exit:
			self.toll = (self.level)**2 - (5*self.level)//2 + 2
			self.message = 'to continue, pay ' + str(self.toll) + ' coins \n'

		self.field[char_prev_position[0]][char_prev_position[1]] = '. '
		self.field[char_position[0]][char_position[1]] = '@ '

	def display(self):
		print('room:', self.level)
		print('coins:', self.coins)
		print('energy:', math.ceil(self.energy/10))
		print(''.join([''.join(row + ['\n']) for row in self.field]))
		self.energy -= 1

class Character:
	def __init__(self, room):
		self.position = [1, 1]
		self.prev_position = [1, 1]
		self.direction = 'd'

	def check_position(self, position, room):
		if position[0] > 8 or position[1] > 13 or position[0] < 1 or position[1] < 1:
			if position == room.entrance or position == room.exit: 
				return True
			else:
				return False
		elif room.field[position[0]][position[1]] == '| ' or room.field[position[0]][position[1]] == '--':
			return False
		else:
			return True

	def set_direction(self, key):
		self.direction = key

	def move(self, room):
		self.prev_position = list(self.position)

		if self.direction == 'w':
			self.position[0] -= 1
		elif self.direction == 's':
			self.position[0] += 1
		elif self.direction == 'a':
			self.position[1] -= 1
		elif self.direction == 'd':
			self.position[1] += 1

		if self.check_position(self.position, room):
			pass
		else:
			self.position = list(self.prev_position)
def main():
	os.system('clear')
	f = open('opening-text.txt', 'r')
	welcome = ''
	for i in range(6):
		welcome += f.readline()
	kproject = f.read()
	f.close()
	for i in range(3):
		os.system('clear')
		print(welcome)
		print('\n' + (' ' * 36) + ('. ' * (i%3)) + 'O ' + ('. ' * (2 - i%3)))
		sleep(.5)
	os.system('clear')
	print(kproject)
	sleep(5)
	os.system('clear')
	f = open('game-info.txt', 'r')
	info = input(f.read())
	f.close()
	os.system('clear')
	room = Room(15, 10, 1, [1, 1])
	char = Character(room.field)
	room.render(char.position, char.prev_position)
	room.display()

	rounds = 0
	ch = getch.getch()

	while ch != 'q':
		os.system('clear')
		char.set_direction(ch)
		char.move(room)
		room.render(char.position, char.prev_position)
		room.display()
		char_position = room.check_toll(char.position)
		char.position = list(char_position)

		if ch == 'h':
			print('\npress w to move up. \npress s to move down. \npress a to move left. \npress d to move right. \n\npress b to buy food. \npress q to quit.')

		elif ch == 'b':
			tobuy = input('would you like to buy some food? ')
			if tobuy == 'ok' or tobuy == 'yes' or tobuy == 'y':
				print('\neach food item costs 2 coins and restores 2 energy')
				howmany = int(input('\nhow many food items would you like to buy? '))
				if howmany * 2 <= room.coins:
					room.coins -= 2 * howmany
					room.energy += 20 * howmany
					print('\ncoins:', room.coins) 
					print('energy:', math.ceil(room.energy/10))
				else:
					print('you do not have enough coins to buy', howmany, 'food item(s)')
			else:
				pass

		ch = getch.getch()
		sleep(.2)
		rounds += 1

main()

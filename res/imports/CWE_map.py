import random
import CWE_terrain
import CWE_units
		
class UnitError(Exception):
	def __init__(self, Value):
		self.value = Value
	def __str__(self):
		return str(self.value)

class Player(object):
	def __init__(self, name):
		self.name = name
		self.funds = 0
		self.color = None
	def salary(self):
		return self.funds
	
	def change_money(self, amount):
		if self.funds + amount < 0:
			return False
		elif self.funds + amount >= 0:
			return True

class Map(object):
	def __init__(self, player_list = ["Player 1", "Player 2"]):
		self.squares = []
		self.selected = [0,0]

		self.player_list = []
		for player_name in player_list:
		    self.player_list.append( Player(player_name) )
		self.color_list = ["orange", "blue", "red", "black"]

		for player_index in range(len(self.player_list)):
			self.player_list[player_index].color = self.color_list[player_index]
		self.turn_count = 0
		self.units = set()
		self.buildings = set()
		self.squares = self.create_grid(10)
		self.test_map_one()
		self.repair_types = {\
		"Port": ["Ship", "Transport"],\
		"Airport": ["Air", "Copter"],\
		"City": ["Tires", "Treads", "Infantry", "Mech"],\
		"Base": ["Tires", "Treads", "Pipe", "Infantry", "Mech"],\
		"Capitol": ["Tires", "Treads", "Infantry", "Mech"] }
		
	def eradicate_units(self, player):
		for unit in self.units:
			if unit.controller == player:
				unit.square.remove_unit()
	
	#returns true if someone has won and the game is over and returns false if nobody has won yet.
	def win_check():
		if len(self.player_list) == 1:
			return true
		else:
			return false

	def get_square(self, coordinate_list):
		return self.squares[coordinate_list[0]][coordinate_list[1]]
	
	def turn_upkeep():
		for player in self.player_list:
			has_units = False
			for unit in self.units:
				if unit.controller == player:
					has_units = True
			if has_units == False:
				player_list.remove(player)
		if win_check():
			print player_list[0] + "won!!!!  " * 200
		
	
	def refresh_units(self):
		for unit in self.units:
			if unit.player == self.current_player:
				unit.has_moved = False
				unit.moves_left = unit.move_range
				unit.fuel -= unit.fuel_per_turn
				if unit.fuel <= 0: unit.die()

		
	def test_map_one(self):
		test_map = self.create_grid(10)
		for list_of_squares in self.squares:
			for square in list_of_squares:
				num = random.randrange(1, 10)
				if num >= 1 and num <= 3:
					square.terrain = CWE_terrain.Plains(square)
				if num >= 4 and num <= 6:
					square.terrain = CWE_terrain.Forest(square)
				if num >= 7 and num <= 8:
					square.terrain = CWE_terrain.Mountain(square)
				if num >= 9 and num <= 10:
					square.terrain = CWE_terrain.Road(square)
		self.get_square([0,9]).add_terrain(CWE_terrain.Capitol(self.get_square([0,9]), self.player_list[0]))
		self.get_square([9,0]).add_terrain(CWE_terrain.Capitol(self.get_square([9,0]), self.player_list[1]))
		self.get_square([1,8]).create_unit("Infantry")
		self.get_square([2,7]).add_terrain(CWE_terrain.Base(self.get_square([2,7])))
		self.get_square([4,5]).add_terrain(CWE_terrain.Base(self.get_square([4,5]), self.player_list[0]))
		self.get_square([7,2]).add_terrain(CWE_terrain.Base(self.get_square([7,2]), self.player_list[1]))
		
	
	def create_grid(self, grid_width_and_height):
		map_squares = []
		for x in range(grid_width_and_height):
			x_list = []
			for y in range(grid_width_and_height):
				x_list.append(Square(self, (x,y)))
			map_squares.append(x_list)
		return map_squares
	
	#takes a tuple of (x,y) coordinates
	def find_square(coordinates):
		return self.squares[coordinates[0]][coordinates[1]]
		
	def add_unit(self, unit_instance, coordinates):
		self.find_square(coordinates).unit = unit_instance
		self.units.add(unit_instance)
	
	def remove_unit(self, coordinates):
		unit_instance = self.find_square(coordinates).unit
		self.find_square(coordinates).unit = None
		self.units.remove(unit_instance)
	
	def move_unit(self, unit , fst_coordinates, end_coordinates):
		if self.find_square(end_coordinates).unit == None:
			self.find_square(end_coordinates) == unit
			if hasattr(self.find_square(fst_coordinates).terrain, "HP"):
				self.find_square(fst_coordinates).terrain.HP = 20
			self.find_square(fst_coordinates) == False
	
	def unit_count(self, player):
		count = 0
		for unit in self.units:
			if unit.controller == player:
				count += 1
		return 
	
	def add_building(self, building_instance):
		self.buildings.add(building_instance)
	
	def remove_building(self, building_instance):
		self.buildings.remove(building_instance)
	
	def building_count(self, player):
		count = 0
		for building in self.buildings:
			if building.controller == player:
				count += 1
				
	def current_player(self):
		return self.player_list[self.turn_count % 2]

	def game_move_up(self):
		try:
			# calculates new indices
			newx = self.selected[0]
			newy = self.selected[1] - 1
			
			#FIXME: this is hackish right now because using negative integers as list indices makes python access the
			# list backwards.  This will work for now but it may need a more permanent fix.
			if newy < 0:
				raise IndexError

			# selects new square.  This is where the IndexError is thrown if no square exists
			newsquare = self.squares[newx][newy]
			# resets the coords of the selector
			self.selected = [newx, newy]
			# finally moves the cursor
			return True
		# catches the error thrown when no square exists
		except IndexError:
			pass
	def game_move_left(self):
		try:
			# calculates new indices
			newx = self.selected[0] - 1
			newy = self.selected[1]
			
			#FIXME: this is hackish right now because using negative integers as list indices makes python access the
			# list backwards.  This will work for now but it may need a more permanent fix.
			if newx < 0:
				raise IndexError
			
			# selects new square.  This is where the IndexError is thrown if no square exists
			newsquare = self.squares[newx][newy]
			# resets the coords of the selector
			self.selected = [newx, newy]
			# finally moves the cursor
			return True
		# catches the error thrown when no square exists
		except IndexError:
			pass
	def game_move_right(self):
		try:
			# calculates new indices
			newx = self.selected[0]+1
			newy = self.selected[1]
			# selects new square.  This is where the IndexError is thrown if no square exists
			newsquare = self.squares[newx][newy]
			# resets the coords of the selector
			self.selected = [newx, newy]
			# finally moves the cursor
			return True
		# catches the error thrown when no square exists
		except IndexError:
			pass
	def game_move_down(self):
		try:
			# calculates new indices
			newx = self.selected[0]
			newy = self.selected[1] + 1
			# selects new square.  This is where the IndexError is thrown if no square exists
			newsquare = self.squares[newx][newy]
			# resets the coords of the selector
			self.selected = [newx, newy]
			# finally moves the cursor
			return True
		# catches the error thrown when no square exists
		except IndexError:
			pass


		
class Square(object):
	def __init__(self, Map,  Position):
		self.Map = Map
		self.position = Position
		self.initial_terrain = None
		self.terrain = None
		self.unit = None
		self.adjacent_squares = []
		
	
	def distance_to(self, square):
	#	for i in range(100):
	#		if square.position in self.find_unrestricted_range(i):
	#			return i
	#	return false
		x_distance = abs( self.position[0] - square.position[0] )
		y_distance = abs( self.position[1] - square.position[1] )
		return x_distance + y_distance
	#self.get_square([1,8]).add_unit(CWE_units.Unit("(Infantry", square = self.get_square([1,8]), player = self.player_list[0]))
	
	def create_unit(self, unit_type):
		print 'create unit'
		print 'current player: ', self.Map.current_player()
		self.add_unit(CWE_units.Unit(unit_type, square = self, controller = self.Map.current_player))
	
	def add_unit(self, unit_instance):
		print 'unit before: ', self.unit

		if self.unit == None:
			self.unit = unit_instance
			print "unit after: ", self.unit
			return True
		else:
			return False
		
	def remove_unit(self):
		if self.unit != None:
			self.unit = None
			return True
		else:
			return False
			#raise UnitError("A unit was not on the square yet remove_unit was called on the square...")
	
	def add_terrain(self, terrain):
		self.initial_terrain = self.terrain
		self.terrain = terrain
	
	def remove_building(self):
		self.terrain = initial_terrain
		
	def find_adjacent(self):
		adjacent = [[0,1], [-1,0], [0,-1], [1,0]]
		for i in adjacent:
			try:
				self.adjacent_squares.append(self.Map.squares[self.position[0] + adjacent[0]][self.position[1] + adjacent[1]])
			except IndexError:
				pass
				
	
	def find_unrestricted_range(self, Range):
		coordinates = set()
		for i in range(Range + 1):
			for j in range(Range + 1 - i):
				for coordinate in [(i,j), (-i,j), (-i,-j), (-i,j)]:
					coordinates.add((self.position[0] + coordinate[0], self.position[1] + coordinate[1]))
		#make the coordinates stop repeating
		return coordinates
	
	def coord_to_square(coordinates):
		squares = []
		for pair in coordinates:
			squares.append(self.Map.squares[pair[0]][pair[1]])
	
	#takes a tuple of the range beginning and end values (in that order) and should return a list of square instances that are in the specified range, but now it just gives coordinates...
	def find_range(self, range_begin, range_end):
		coordinates = self.find_unrestricted_range(range_end)
		for pair in self.find_unrestricted_range(range_begin):
			if pair in coordinates:
				coordinates.remove(pair)
		return coordinates
		#squares = self.coord_to_square(coordinates)
	def can_build(self):
		if isinstance( self.terrain, CWE_terrain.Building ) and self.terrain.unit_list != set():
			return self.terrain.unit_list
		else: return False
# PLEASE NOTE THAT THESE DON'T WORK PROPERLY, PLEASE DON'T RELY ON THEM
def code_check():
	x = Map()
	y = 0
	print "test of find_rage(1,3):", x.squares[3][3].find_unrestricted_range(1)
	print "test of square.distance_to (should be 5) :", x.squares[3][3].distance_to(x.squares[6][5])
	print "test of print_map: \n", print_map(x)

def print_map(a_map):
	print "Printing map to console.\n\nBeep beep, boop boop..."
	counter = 0
	for x in range(len(a_map.squares)):
		for y in range(len(a_map.squares[0])-1, -1, -1):
			counter += 1
			print a_map.get_square([x,y]).terrain.label[0:1],
			if counter == len(a_map.squares):
				counter = 0
				print ""
	#for x in a_map.squares:
		## this is supposed to iterate down columns
		#for y in x:
			## but it prints down rows
			#print str(y.terrain)[10:14] , 
			#counter += 1
			#if counter == 10:
				#counter = 0
				#print ""



if __name__ == "__main__":
	code_check()
	


		
		
		
		
		

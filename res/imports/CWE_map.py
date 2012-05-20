import random
import CWE_terrain
import CWE_units

class CursorError(Exception):
	def __init__(self, Value):
		self.value = Value
	def __str__(self):
		return str(self.value)
		
class UnitError(Exception):
	def __init__(self, Value):
		self.value = Value
	def __str__(self):
		return str(self.value)
		

class Map(object):
	
	def __init__(self, players_list):
		self.squares = []
		self.cursor = [0, 0]
		self.player_list = players_list
		self.turn_count = 0
		self.units = set()
		self.buildings = set()
		self.squares = self.create_grid(10)
		self.test_map_one()
	
	def get_square(self, coordinate_list):
		return self.squares[coordinate_list[0]][coordinate_list[1]]
 
	def refresh_units(self):
		for unit in self.units:
			if unit.player == self.current_player:
				unit.has_moved = False
				
	def cursor_square(self):
		return self.find_square(self.cursor)
		
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
		self.find_square(coordinates).unit = False
		self.units.remove(unit_instance)
	
	def move_unit(self, unit , fst_coordinates, end_coordinates):
		if self.find_square(end_coordinates).unit == False:
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
			
	def move_cursor(self, direction):
		if direction == "up":
			if len(self.squares[0]) > self.cursor[1]:
				self.cursor[1] += 1
		elif direction == "right":
			if len(self.squares) > self.cursor[0]:
				self.cursor[0]+= 1
		elif direction  == "left":
			if self.cursor[0] > 0:
				self.cursor[0] -= 1
		elif direction == "down":
			if self.cursor[1] > 0:
				self.cursor -= 1
		else:
			return False
				
	def current_player(self):
		return self.player_list[self.turn_count % 2]
		
class Square(object):
	def __init__(self, Map,  Position):
		self.Map = Map
		self.position = Position
		self.initial_terrain = False
		self.terrain = False
		self.unit = False
		self.adjacent_squares = []
		moove_num = 0
	
	def distance_to(self, square):
		for i in range(100):
			if square.position in self.find_unrestricted_range(i):
				return i
		return false
		
	#self.get_square([1,8]).add_unit(CWE_units.Unit("(Infantry", square = self.get_square([1,8]), player = self.player_list[0]))
	
	def create_unit(self, unit_type):
		self.add_unit(CWE_units.Unit(unit_type, square = self, player = self.Map.current_player))
	
	def add_unit(self, unit_instance):
		if self.unit != False:
			self.unit = unit_instance
			return true
		elif self.unit == False:
			return False
		
	def remove_unit(self):
		if self.unit != False:
			self.unit = False
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
			
# PLEASE NOTE THAT THESE DON'T WORK PROPERLY, PLEASE DON'T RELY ON THEM
def code_check():
	x = Map(["Player 1", "Player 2"])
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


		
		
		
		
		

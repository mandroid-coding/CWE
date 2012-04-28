

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
	
	def __init__(self, players):
		self.squares = []
		self.cursor = [0, 0]
		self.player_list = players
		self.turn_count = 0
		self.units = set()
		self.buildings = set()
		self.create_map()
	
	def create_map(self):
		for x in range(10):
			x_list = []
			for y in range(10):
				x_list.append(Square(self, (x,y)))
			self.squares.append(x_list)
	
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
			self.find_square(fst_coordinates) == False
	
	def unit_count(self, player):
		count = 0
		for unit in self.units:
			if unit.player == player:
				count += 1
		return 
	
	def add_building(self, building_instance):
		self.buildings.add(building_instance)
	
	def remove_building(self, building_instance):
		self.buildings.remove(building_instance)
	
	def building_count(self, player):
		count = 0
		for building in self.buildings:
			if building.player == player:
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
		
	def add_unit(self, unit_instance):
		if self.units != None:
			self.unit = unit_instance
			
		elif self.units == None:
			return False
		
	def remove_unit(self):
		if self.unit != None:
			self.unit = none
		else:
			raise UnitError("A unit was not on the square yet remove_unit was called on the square...")
	
	def add_terrain(self, terrain):
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
					coordinates.add(coordinate)
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
			
		
		
x = Map(["Calvin", "Megan"])
x.squares[3][3].find_range(1,3)



##class Terrain(object):
	##def __init__(self, 
		
		
		
		
		

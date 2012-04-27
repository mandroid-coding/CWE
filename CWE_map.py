

class CursorError(Exception):
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
		
	def add_unit(self, unit_instance):
		self.units.add(unit_instance)
	
	def remove_unit(self, unit_instance):
		self.units.remove(unit_instance)
	
	def unit_count(self, player):
		count = 0
		for unit in self.units:
			if unit.player == player:
				count += 1
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
			raise Cursor_Error("value out of range")
				
	def current_player(self):
		return self.player_list[self.turn_count % 2]
		
class Square(object):
	def __init__(self, Position):
		self.position = Position
		self.terrain = None
		self.unit = None
		
	def add_unit(self, unit_instance):
		self.unit = unit_instance
		
		

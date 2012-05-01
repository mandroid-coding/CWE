

class Terrain(object):
	def __init__(self, square, defence):
		self.square = square
		self.defence = defence

class Forrest(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 2)
		
class Plains(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 1)
		
class Mountain(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 4)
		
class Sea(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 1)
		
class Reef(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 2)
		
class River(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
	
class Road(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		

	
		
class Building(Terrain):
	def __init__(self, square, defence, controller = False):
		Terrain.__init__(square, defence)
		self.HP = 20
		self.controller = controller
		
	def capture(self, unit):
		self.HP -= unit.hp
		if self.controller == unit.controller:
			return false
		elif self.HP < 0 or self.HP == 0:
			self.controller = unit.controller
			self.HP = 20
		
		
class City(Building):
	def __init__(self, square, controller):
		Building.__init__(self, square, 3, controller)
		
class Base(Building):
	def __init__(self, square, controller):
		Building.__init__(self, square, 3, controller)
		
class Airport(Building):
	def __init__(self, square, controller):
		Building.__init__(self, square, 3, controller)
		
class Port(Building):
	def __init__(self, square, controller):
		Building.__init__(self, square, 3, controller)
	
	
	
	

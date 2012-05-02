

class Terrain(object):
	def __init__(self, square, defense):
		self.square = square
		self.defense = defense

class Forest(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 2)
		self.color = 'darkgreen'
		
class Plains(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 1)
		self.color = "lightgreen"
		
class Mountain(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 4)
		self.color = "chocolate"
		
class Sea(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 1)
		self.color = "blue"
		
class Reef(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 2)
		self.color = "turquoise"
		
class River(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "lightblue"
	
class Road(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "grey90"

class Beach(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "tan"

	
		
class Building(Terrain):
	def __init__(self, square, defense, controller = False):
		Terrain.__init__(square, defense)
		self.HP = 20
		self.controller = controller
		
	def capture(self, unit):
		if self.controller == unit.controller:
			return False
		self.HP -= unit.hp
		if self.HP < 0 or self.HP == 0:
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
	

	
	

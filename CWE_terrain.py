

class Terrain(object):
	def __init__(self, square, defense):
		self.square = square
		self.defense = defense
		self.label = "none"
	def __str__(self):
		return self.label
		
class Forest(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 2)
		self.color = 'darkgreen'
		self.label = 'Forest'
		
class Plains(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 1)
		self.color = "lightgreen"
		self.label = "Plains"
		
class Mountain(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 4)
		self.color = "brown"
		self.label = "Mountain"
		
class Sea(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 1)
		self.color = "blue"
		self.label = "Sea"
		
class Reef(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 2)
		self.color = "turquoise"
		self.Reef = "Reef"
		
class River(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "lightblue"
		self.label = "River"
		
class Road(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "grey"
		self.label = "Road"

class Beach(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "tan"
		self.label = "Beach"

	
		
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
		self.label = 'City'
		
class Base(Building):
	def __init__(self, square, controller):
		Building.__init__(self, square, 3, controller)
		self.label = 'base'
		
class Airport(Building):
	def __init__(self, square, controller):
		Building.__init__(self, square, 3, controller)
		self.label = "Airport"
		
class Port(Building):
	def __init__(self, square, controller):
		Building.__init__(self, square, 3, controller)
		self.label = 'Port'

	
	



class Terrain(object):
	def __init__(self, square, defense):
		self.square = square
		self.defense = defense
		self.label = "None"
	def __str__(self):
		return self.label
	
class Forest(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 2)
		self.color = 'darkgreen'
		self.label = "Forest"
	
class Plains(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 1)
		self.color = "lightgreen"
		self.label = 'Plains'
	
class Mountain(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 4)
		self.color = "chocolate"
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
		self.label = "Reef"
	
class River(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "lightblue"
		self.label = "River"
	
class Bridge(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "grey90"
		self.label = "Bridge"
	
class Road(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "grey90"
		self.label = "Road"
	
class Beach(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "tan"
		self.label = "Beach"
	
class Pipeline(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.color = "red"
		self.label = "Pipeline"
	
class Pipe_Seam(Terrain):
	def __init__(self, square):
		Terrain.__init__(self, square, 0)
		self.HP = 100
		self.color = "red"
		self.label = "Pipe_Seam"
		self.square = self
		self.armor_type = "Medium_Tank"
	def attacked(self, unit):
		self.hp = self.HP
		self.max_hp = 100
		unit.attack(self)
	def die(self):
		self.label = "Road"
		self.color = "grey90"
		del self.HP, self.square, self.armor_type, self.hp, self.max_hp
	
class Building(Terrain):
	def __init__(self, square, defense, controller):
		Terrain.__init__(self, square, defense)
		self.HP = 20
		self.controller = controller
		self.color = "grey20"
		self.unit_list = set()
		self.being_captured = False
	def capture(self, unit):
		if self.controller == unit.controller:
			return False
		self.HP -= unit.hp
		self.being_captured = True
		if self.HP < 0 or self.HP == 0:
			self.controller = unit.controller
			self.HP = 20
<<<<<<< HEAD
	        self.being_captured = False
=======
			self.being_captured = False
>>>>>>> 4b212cd3aa7ddb7961c3a1c21f66c749e3a6aca3

class Capitol(Building):
	def __init__(self, square, controller):
		Building.__init__(self, square, 4, controller)
		self.label = "Capitol"
	def capture(self, unit):
		if self.controller == unit.controller:
			return False
		self.HP -= unit.hp
		if self.HP < 0 or self.HP == 0:
			self.square.Map.eradicate_units(self.controller)
			self.square.Map.player_list.remove(self.controller)
			##
			self.controller = unit.controller
			self.HP = 20
	
class City(Building):
	def __init__(self, square, controller = None):
		Building.__init__(self, square, 3, controller)
		self.label = "City"
	
class Base(Building):
	def __init__(self, square, controller = None):
		Building.__init__(self, square, 3, controller)
		self.label = "Base"
		self.unit_list = [["Anti-Air", "8000"], ["APC", "5000"],  ["Artillery", "6000"], 
		["Infantry", "1000"], ["Mech", "3000"], ["Medium_Tank", "16000"], ["Megatank" ,"28000"], 
		["Missiles","12000"], ["Neotank", "22000"], ["Piperunner", "20000"], ["Recon","4000"], 
		["Rockets", "12000"], ["Tank", "7000"]]
		
class Airport(Building):
	def __init__(self, square, controller = None):
		Building.__init__(self, square, 3, controller)
		self.label = "Airport"
		self.unit_list = [["B-Copter", "9000"], ["Bomber", "28000"], ["Fighter", "22000"], ["Stealth", "24000"], ["T-Copter", "5000"]]
class Port(Building):
	def __init__(self, square, controller = None):
		Building.__init__(self, square, 3, controller)
		self.label = "Port"
		self.unit_list = [["Battleship", "28000"], ["Black_Boat", "7500"], ["Carrier", "30000"], ["Cruiser", "18000"], ["Lander", "12000"], ["Sub", "20000"]]

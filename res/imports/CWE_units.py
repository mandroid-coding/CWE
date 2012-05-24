#Important note!  When a unit stealths,
#it must change its armor type to "Stealthed_X"
#For example, Stealthed_Sub
import os.path
from CWE_units import __file__
import CWE_map
module_folder = os.path.dirname( __file__ )
resource_folder = os.path.abspath( os.path.join( module_folder, os.path.pardir) )
unit_folder = os.path.join( resource_folder, "units" )
class Unit:
#Current kwargs are controller, and cost.
    def __init__(self, typename = "", **kwargs):
        #Default to the generic unit description (a mech).
        if typename == "":
            typename = "Generic"
        #Import the unit from a file.
        filepath = os.path.join( unit_folder, (typename + ".unit") )
        unit_source = open(filepath, "r")
        fields = {}
        #Parse the unit's file into fields, which will be read to generate the unit.
        for line in unit_source.readlines():
            #Allow comment lines
            if line[0] == "#": continue
            parsed_line = line.strip().split("\t")
            fields[ parsed_line[0] ] = parsed_line[1]
        #Allow the method caller to specify a controller
        if "controller" in kwargs.keys():
            self.controller = kwargs["controller"]
        else:
            raise TypeError("Controller is mandatory")
        #Allow the method caller to override the default cost
        if "cost" in kwargs.keys():
            self.cost = kwargs["cost"]
        else:
            self.cost = int(fields["Base_Cost"])
        #Allow the method caller to supply a custom name
        if "name" in kwargs.keys():
            self.name = kwargs["name"]
        else:
            self.name = fields["Name"]
        #Allow units to be created on or off squares
        #(an example of the latter is the unit from Days of Ruin, Seaplanes
        #which go into the inventory of their carrier.
        #Seaplanes do not exist in this game.)
        if "square" in kwargs.keys():
            self.square = kwargs["square"]
        else:
            self.square = None
        self.max_hp = int(fields["Max_HP"])
        self.hp = int(self.max_hp)
        self.move_type = fields["Move_Type"]
        # All units have a move_type, which determines their movement costs.
        x = self.move_type
        if x == "Air" or x == "Copter": self.terrain_costs = {
        "Airport":1,
        "Base":1,
        "Bridge":1,
        "Beach":1,
        "Capitol":1,
        "City":1,
        "Forest":1,
        "Mountain":1,
        "Pipeline":"N/A",
        "Pipe_Seam":"N/A",
        "Plains":1,
        "Port":1,
        "Reef":1,
        "River":1,
        "Road":1,
        "Sea":1,
        }
        elif x == "Infantry": self.terrain_costs = {
        "Airport":1,
        "Base":1,
        "Bridge":1,
        "Beach":1,
        "Capitol":1,
        "City":1,
        "Forest":1,
        "Mountain":2,
        "Pipeline":"N/A",
        "Pipe_Seam":"N/A",
        "Plains":1,
        "Port":1,
        "Reef":"N/A",
        "River":2,
        "Road":1,
        "Sea":"N/A",
        }
        elif x == "Mech": self.terrain_costs = {
        "Airport":1,
        "Base":1,
        "Bridge":1,
        "Beach":1,
        "Capitol":1,
        "City":1,
        "Forest":1,
        "Mountain":1,
        "Pipeline":"N/A",
        "Pipe_Seam":"N/A",
        "Plains":1,
        "Port":1,
        "Reef":"N/A",
        "River":1,
        "Road":1,
        "Sea":"N/A",
        }
        elif x == "Pipe": self.terrain_costs = {
        "Airport":"N/A",
        "Base":1,
        "Bridge":"N/A",
        "Beach":"N/A",
        "Capitol":"N/A",
        "City":"N/A",
        "Forest":"N/A",
        "Mountain":"N/A",
        "Pipeline":1,
        "Pipe_Seam":1,
        "Plains":"N/A",
        "Port":"N/A",
        "Reef":"N/A",
        "River":"N/A",
        "Road":"N/A",
        "Sea":"N/A",
        }
        elif x == "Ship": self.terrain_costs = {
        "Airport":"N/A",
        "Base":"N/A",
        "Bridge":"N/A",
        "Beach":"N/A",
        "Capitol":"N/A",
        "City":"N/A",
        "Forest":"N/A",
        "Mountain":"N/A",
        "Pipeline":"N/A",
        "Pipe_Seam":"N/A",
        "Plains":"N/A",
        "Port":1,
        "Reef":2,
        "River":"N/A",
        "Road":"N/A",
        "Sea":1,
        }
        elif x == "Tires": self.terrain_costs = {
        "Airport":1,
        "Base":1,
        "Bridge":1,
        "Beach":1,
        "Capitol":1,
        "City":1,
        "Forest":3,
        "Mountain":"N/A",
        "Pipeline":"N/A",
        "Pipe_Seam":"N/A",
        "Plains":2,
        "Port":1,
        "Reef":"N/A",
        "River":"N/A",
        "Road":1,
        "Sea":"N/A",
        }
        elif x == "Transport": self.terrain_costs = {
        "Airport":"N/A",
        "Base":"N/A",
        "Bridge":"N/A",
        "Beach":1,
        "Capitol":"N/A",
        "City":"N/A",
        "Forest":"N/A",
        "Mountain":"N/A",
        "Pipeline":"N/A",
        "Pipe_Seam":"N/A",
        "Plains":"N/A",
        "Port":1,
        "Reef":2,
        "River":"N/A",
        "Road":"N/A",
        "Sea":1,
        }
        elif x == "Treads": self.terrain_costs = {
        "Airport":1,
        "Base":1,
        "Bridge":1,
        "Beach":1,
        "Capitol":1,
        "City":1,
        "Forest":2,
        "Mountain":"N/A",
        "Pipeline":"N/A",
        "Pipe_Seam":"N/A",
        "Plains":1,
        "Port":1,
        "Reef":"N/A",
        "River":"N/A",
        "Road":1,
        "Sea":"N/A",
        }
        else:
            raise Exception("Unrecognized movement type: {}".format(x))
        #Some units have an additional upkeep fuel cost.
        if x in ["Transport", "Ship"]:
            self.fuel_per_turn = 1
        elif x == "Copter":
            self.fuel_per_turn = 2
        elif x == "Air":
            self.fuel_per_turn = 5
        else:
            self.fuel_per_turn = 0
        self.max_fuel = int(fields["Max_Fuel"])
        #Units start with full fuel.
        self.fuel = self.max_fuel
        self.move_range = int(fields["Move_Range"])
        #Units do not, however, start with full movement
        #(it is replenished at the beginning of a turn)
        self.moves_left = 0
        #Armor type determines how much damage a unit takes.
        #Non-unit buildings have the "Medium_Tank" armor type.
        self.armor_type = fields["Armor_Type"]
        #Some units have a primary weapon.  They will preferentially
        #use this weapon in combat, if possible.
        self.primary_name = fields["Primary_Name"]
        if self.primary_name != "N/A":
            #Weapons haver a maximum and minimum range (<= and >=)
            range_tuple = fields["Primary_Range"][1:-1].split(",")
            self.primary_range = ( int(range_tuple[0]), int(range_tuple[1]) )
            #Weapons deal damage as determined by a dictionary of unit types.
            #Weapons cannot fire on units that are not in this table.
            self.primary_table = {}
            for pair in fields["Primary_Table"].split(", "):
                #Look into generic.unit to see why this code is required.
                realpair = pair.split("=")
                self.primary_table[ realpair[0] ] = int(realpair[1])
            #Primary weapons have ammo.  If they have no ammo, they cannot be fired.
            self.max_ammo = int(fields["Ammo"])
            self.ammo = self.max_ammo
        self.secondary_name = fields["Secondary_Name"]
        if self.secondary_name != "N/A":
            range_tuple = fields["Secondary_Range"][1:-1].split(",")
            self.secondary_range = ( int(range_tuple[0]), int(range_tuple[1]) )
            self.secondary_table = {}
            for pair in fields["Secondary_Table"].split(", "):
                realpair = pair.split("=")
                self.secondary_table[ realpair[0] ] = int(realpair[1])
        #Some units can carry other units.
        self.carry_types = fields["Carry_Types"].split(", ")
        if self.carry_types != ["N/A"]:
            self.carry_count = int(fields["Carry_Count"])
            #"None" is the CWE_units default for 'no unit'.
            #It is required here as a placeholder to keep the list a fixed length.
            self.carried_units = [None] * self.carry_count
        else:
            self.carry_types = []
            self.carried_units = []
        #Units can see a certain distance in fog of war.
        self.vision_range = int(fields["Vision_Range"])
        #Air units can see through trees without being adjacent.
        if self.move_type in ["Air", "Copter"]:
            self.bypass_fog = True
        else:
            self.bypass_fog = False
        #All units have an image_type, a (hopefully) unique image representation.
        #The format is "[color]_[unit].gif", e.g. "blue_tank.gif"
        self.image_type = fields["Image_Type"]
        if fields["Can_Stealth"] == "True":
            self.can_stealth = True
            self.stealthed_image = "stealthed_" + self.image_type
        else:
            self.can_stealth = False
        if fields["Can_Capture"] == "True":
            self.can_capture = True
        else:
            self.can_stealth = False
        if fields["Can_Resupply"] == "True":
            self.can_resupply = True
        else:
            self.can_resupply = False
        if fields["Can_Launch"] == "True":
            self.can_launch = True
        else:
            self.can_launch = False
        if fields["Can_Explode"] == "True":
            self.can_explode = True
        else:
            self.can_explode = False
        if fields["Can_Repair"] == "True":
            self.can_repair = True
        else:
            self.can_repair = False
        #Even stealth-capable units start out unstealthed.
        self.stealthed = False
    #A unit's string representation is its name followed by its health percent.
    #e.g. Tank (50%)
    def __str__(self):
        return self.name + "({health}%)".format(health = int((self.hp / self.max_hp) * 100))
    #An attack returns "True" if the enemy unit survived for a manual counterattack.
    #It returns "False" if the enemy unit died.
    def attack(self, target):
        damage = 0
        distance = self.square.distance_to(target.square)
        #Check the following conditions (primary weapon can fire on the enemy)
        if self.primary_name != "N/A" and (self.ammo > 0)\
        and (target.armor_type in self.primary_table)\
        and ( distance >= self.primary_range[0] )\
        and ( distance <= self.primary_range[1] ):
            #Use the damage calculation determined by Advance Wars DS.
            b = self.primary_table[ target.armor_type ]
            a = float(self.hp)/self.max_hp
            r = target.square.terrain.defense
            t = ( b * a * 0.1 )
            h = ((target.max_hp - target.hp) / target.max_hp) * 100
            damage = t - (r * ( (t * 0.1) - (h * t * 0.1) ) )
            self.ammo -= 1
        #If an attack with the primary weapon could not be completed,
        #Try an attack with the secondary weapon.
        elif self.secondary_name != "N/A"\
        and (target.armor_type in self.secondary_table)\
        and ( distance >= self.secondary_range[0] )\
        and ( distance <= self.secondary_range[1] ):
            b = self.secondary_table[ target.armor_type ]
            a = float(self.hp)/self.max_hp
            r = target.square.terrain.defense
            t = ( b * a * 0.1 )
            h = ((target.max_hp - target.hp) / target.max_hp) * 100
            damage = t - (r * ( (t * 0.1) - (h * t * 0.1) ) )
        #Apply damage
        target.hp -= damage
        survived = True
        if target.hp <= 0:
            target.die()
            survived = False
        return survived
    def die(self):
        #Units do not leave behind baggage when they die, so unit death
        #can be as simple as (square ->)self.unit = None
        self.square.remove_unit()
    def stealth(self):
        #Stealthed fuel cost per turn is determined by the unit
        if self.move_type == "Ship":
            #(currently the only ships that can stealth are subs)
            self.stealth_cost = 5
        elif self.move_type == "Air":
            #(currently the only air units that can stealth are stealth bombers)
            self.stealth_cost = 8
        else: raise AttributeError( str(self) + "units cannot enter stealth" )
        #Hold on to the old fuel cost and update the unit's attributes
        self.normal_fuel_cost = self.fuel_per_turn
        self.fuel_per_turn = self.stealth_cost
        self.stealthed = True
        self.real_image = self.image_type
        self.image_type = self.stealthed_image
    def unstealth(self):
        if not unit.stealthed:
            raise AttributeError( "Non-stealthed units cannot use the unstealth command" )
        #Return everything to normal.
        self.fuel_per_turn = self.normal_fuel_cost
        self.stealthed = True
        self.image_type = self.real_image
        #Enable the following line if units are taking up too much space.
        #del self.normal_fuel_fost, real_image
    def begin_turn(self):
        #Assorted beginning-of-turn bookkeeping.
        self.fuel -= self.fuel_per_turn
        if self.fuel <= 0: self.die()
        self.moves_left = self.move_range
    #Method to handle unit carriers to drop units (loading must be done manually)
    def drop_unit(self, index, square):
        #Ensure that there exists a unit to be dropped, and that the carrier
        #is in the proper state to drop the unit (transport copters must drop from land)
        if self.carried_units[index] and self.square.terrain in\
        self.carried_units[index].terrain_costs.keys():
            #Ensure that the target square is unoccupied and is exactly one square
            #away (you cannot drop a unit onto the same square as you)
            if not square.unit and self.square.distance_to( square ) == 1:
                square.unit = self.carried_units[index]
                self.carried_units[index] = None
total_unit_types = set(
    ("Infantry, Mech, Recon, Tank, Medium_Tank, Neotank, Megatank, APC, "+
     "Artillery, Rockets, Anti-Air, Missiles, Piperunner, Fighter, "+
     "Bomber, Stealth, B-Copter, T-Copter, Battleship, Cruiser, Lander, "+
     "Sub, Black_Boat, Carrier").split(", ")
                        )
if __name__ == "__main__":
    unit_list = set()
    missing_images = set()
    for unit_type in total_unit_types:
        current = Unit(unit_type)
        unit_list.add( current )
        print str(current), " -- initialization successful "
        print current.name
        for color in ["orange", "blue"]:
            filename = os.path.join( resource_folder,\
            "images", "{color}_{unit_type}.gif".format\
            (color=color, unit_type=current.image_type) )
            if not os.path.exists( filename ):
                print ( ("{color} {unit_type} image not found at expected"+
                " directory {directory}").format( color=color,\
                unit_type=current.image_type, directory=filename ) )
                missing_images.add( str(filename) )
            else:
                print "Unit has an image (OK!)"
    for file_name in missing_images:
        print file_name

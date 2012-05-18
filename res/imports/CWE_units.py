#Important note!  When a unit stealths,
#it must change its armor type to "Stealthed_X"
#For example, Stealthed_Sub
import os.path
from CWE_units import __file__
module_folder = os.path.dirname( __file__ )
resource_folder = os.path.abspath( os.path.join( module_folder, os.path.pardir) )
unit_folder = os.path.join( resource_folder, "units" )
class Unit:
#Current kwargs are controller, and cost.
    def __init__(self, typename = "", **kwargs):
        #Default to the generic unit description.
        if typename == "":
            typename = "generic"
        #Import the unit from a file.
        filepath = os.path.join( unit_folder, (typename + ".unit") )
        unit_source = open(filepath, "r")
        fields = {}
        for line in unit_source.readlines():
            if line[0] == "#": continue
            parsed_line = line.strip().split("\t")
            fields[ parsed_line[0] ] = parsed_line[1]

        if "controller" in kwargs.keys():
            self.controller = kwargs["controller"]
        else:
            self.controller = "Nobody"

        if "cost" in kwargs.keys():
            self.cost = kwargs["cost"]
        else:
            self.cost = int(fields["Base_Cost"])
   
        if "name" in kwargs.keys():
            self.name = kwargs["name"]
        else:
            self.name = fields["Name"]
        if "square" in kwargs.keys():
            self.square = kwargs["square"]
        else:
            self.square = None
        self.max_hp = int(fields["Max_HP"])
        self.hp = int(self.max_hp)
        self.move_type = fields["Move_Type"]
        x = self.move_type
        if x == "Air": self.terrain_costs = {
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
        self.max_fuel = int(fields["Max_Fuel"])
        self.fuel = self.max_fuel
        self.move_range = int(fields["Move_Range"])
        self.armor_type = fields["Armor_Type"]
        self.primary_name = fields["Primary_Name"]
        if self.primary_name != "N/A":
            range_tuple = fields["Primary_Range"][1:-1].split(",")
            self.primary_range = ( int(range_tuple[0]), int(range_tuple[1]) )
            self.primary_table = {}
            for pair in fields["Primary_Table"].split(", "):
                realpair = pair.split("=")
                self.primary_table[ realpair[0] ] = int(realpair[1])
            self.ammo = int(fields["Ammo"])
        self.secondary_name = fields["Secondary_Name"]
        if self.secondary_name != "N/A":
            range_tuple = fields["Secondary_Range"][1:-1].split(",")
            self.secondary_range = ( int(range_tuple[0]), int(range_tuple[1]) )
            self.secondary_table = {}
            for pair in fields["Secondary_Table"].split(", "):
                realpair = pair.split("=")
                self.secondary_table[ realpair[0] ] = int(realpair[1])
        self.carry_types = fields["Carry_Types"].split(", ")
        if self.carry_types != ["N/A"]:
            self.carry_count = int(fields["Carry_Count"])
        else:
            self.carry_types = []
        self.vision_range = int(fields["Vision_Range"])
        self.image_type = fields["Image_Type"]
        if fields["Can_Stealth"] == "True":
            self.can_stealth = True
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
    def __str__(self):
        return self.name
    def attack(self, target):#Return true/false
        damage = 0
        distance = self.square.distance_to(target.square)
        if self.primary_name != "N/A" and (self.ammo > 0) and (target.armor_type in self.primary_table) and ( distance >= self.primary_range[0] ) and ( distance <= self.primary_range[1] ):
            b = self.primary_table[ target.armor_type ]
            a = float(self.hp)/self.max_hp
            r = target.square.terrain.defense
            t = ( b * a * 0.1 )
            h = ((target.max_hp - target.hp) / target.max_hp) * 100
            f = t - (r * ( (t * 0.1) - (h * t * 0.1) ) )
        elif self.secondary_name != "N/A"\
        and (target.armor_type in self.secondary_table)\
        and ( distance >= self.secondary_range[0] )\
        and ( distance <= self.secondary_range[1] ):
            b = self.secondary_table[ target.armor_type ]
            a = float(self.hp)/self.max_hp
            r = target.square.terrain.defense
            t = ( b * a * 0.1 )
            h = ((target.max_hp - target.hp) / target.max_hp) * 100
            f = t - (r * ( (t * 0.1) - (h * t * 0.1) ) )
        else:
            f = 0
        target.hp -= f
        survived = True
        if target.hp <= 0:
            target.die()
            survived = False
        return survived
    def die(self):
        self.square.remove_unit()
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

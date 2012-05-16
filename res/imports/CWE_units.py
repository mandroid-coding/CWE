import os.path


project_root = os.path.curdir
resource_folder = os.path.join( project_root, "res" )
image_folder = os.path.join( resource_folder, "images" )
unit_folder = os.path.join( resource_folder, "units" )
class Unit:
#Current kwargs are controller, and cost.
    def __init__(self, filename = "", **kwargs):
        if filename == "":#Default to the generic unit description.
            filename = "generic.unit"
        filepath = os.path.join( unit_folder, filename )#Import the unit from a file.
        unit_source = open(filepath, "r")
        fields = {}
        for line in unit_source.readlines():
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
        self.terrain_costs = {}
        for item in fields["Terrain_Costs"].split(", "):
            pair = item.split("=")
            pair[0] = pair[0]
            if pair[1] == "N/A":
                self.terrain_costs[ pair[0] ] = "n/a"
            else:
                self.terrain_costs[ pair[0] ] = int(pair[1])
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
                primary_table[ realpair[0] ] = int(realpair[1])
            self.ammo = int(fields["Ammo"])
        self.secondary_name = fields["Secondary_Name"]
        if self.secondary_name == "N/A":
            range_tuple = fields["Secondary_Range"][1,-1].split(", ")
            self.secondary_range = ( int(range_tuple[0]), int(range_tuple[1]) )
            self.secondary_table = {}
            for pair in fields["Secondary_Table"].split(", "):
                realpair = pair.split("=")
                secondary_table[ realpair[0] ] = int(realpair[1])
        self.carry_types = fields["Carry_Types"].split(", ")
        if self.carry_types != ["N/A"]:
            self.carry_count = int(fields["Carry_Count"])
        else:
            self.carry_types = []
        self.vision_range = int(fields["Vision_Range"])
        self.image_name = fields["Image_Name"]
        if fields["Can_Stealth"] == "True":#They insisted that these "Can_X" be this way, and I was already drained enough from trying to convince them that hard-coding unit definitions for 20+ units is a Bad Idea
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
    def __str__(self):
        return self.name
    def attack(self, target):#Return true/false
        damage = 0
        distance = self.square.distance_to(target.square)
        if self.primary_name != "N/A":
            if (self.ammo > 0) and (target.armor_type in self.primary_table) and ( distance >= self.primary_range[0] ) and ( distance <= self.primary_range[1] ):
                b = self.primary_table[ target.armor_type ]
                a = double(self.hp)/self.max_hp
                r = target.square.terrain.defense
                t = ( b * a * 0.1 )
                h = ((target.max_hp - target.hp) / target.max_hp) * 100
                f = t - (r * ( (t * 0.1) - (h * t * 0.1) ) )
        elif self.secondary_name != "N/A":
            if (target.armor_type in self.secondary_table) and ( distance >= self.secondary_range[0] ) and ( distance <= self.secondary_range[1] ):
                b = self.secondary_table[ target.armor_type ]
                a = double(self.hp)/self.max_hp
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

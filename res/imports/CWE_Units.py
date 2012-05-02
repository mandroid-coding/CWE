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
            self.primary_type = fields["Primary_Type"]
            self.primary_power = int(fields["Primary_Power"])
            range_tuple = fields["Primary_Range"][1:-1].split(",")
            self.primary_range = ( int(range_tuple[0]), int(range_tuple[1]) )
            self.primary_can_attack = set()
            for receiver in fields["Primary_Can_Attack"].split(", "):
                self.primary_can_attack.add( receiver )
            self.ammo = int(fields["Ammo"])
        self.secondary_name = fields["Secondary_Name"]
        if self.secondary_name == "N/A":
            self.secondary_type = fields["Secondary_Type"]
            self.secondary_power = int(fields["Secondary_Power"])
            range_tuple = fields["Secondary_Range"][1,-1].split(", ")
            self.secondary_range = ( int(range_tuple[0]), int(range_tuple[1]) )
            self.secondary_can_attack = set()
            for receiver in fields["Secondary_Can_Attack"]:
                self.secondary_can_attack.add( receiver )
        self.carry_types = fields["Carry_Types"].split(", ")
        if self.carry_types != ["N/A"]:
            self.carry_count = int(fields["Carry_Count"])
        else:
            self.carry_types = []
        if fields["Can_Stealth"] == "True":
            self.can_stealth = True
        else:
            self.can_stealth = False
        self.vision_range = int(fields["Vision_Range"])
        self.image_name = fields["Image_Name"]
        self.custom_commands = fields["Custom_Commands"].split(", ")
        
        self.has_moved = False
    def __str__(self):
        return self.name
    #need functions: attack(), 

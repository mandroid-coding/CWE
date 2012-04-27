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
        filepath = os.path.join( image_folder, filename )#Import the unit from a file.
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
            self.cost = fields["Base_Cost"]
        
        if "name" in kwargs.keys():
            self.name = kwargs["name"]
        else:
            self.name = fields["name"]

        self.max_hp = fields["Max_HP"]
        self.hp = self.max_hp

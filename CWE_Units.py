import os.path
project_root = os.path.curdir
resource_folder = os.path.join( project_root, "res" )
image_folder = os.path.join( project_root, "images" )
#don't forget cost
class Unit:
    def __init__(self, filename = "", **kwargs):
        if filename == "":
            filename = "generic.unit"
        filepath = os.path.join( image_folder, filename )

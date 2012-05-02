#Ignore this comment

class Menu:
    
    def __init__(self,board):
        self.parts,self.titles = MenuOptions.getOptions(board)
        #Need exception handling for empty lists
        self.selected = 0
        print("Menu initialized")
        
    def scroll_increment(self,inc):
        self.selected = (self.selected + inc) % len(self.parts)
        
    def select(self):
        self.parts[self.selected]()

class MenuOptions:
    
    #Will cause unit to attack another???
    def attack(self,board):
        pass
    
    #Does nothing, as it should
    def exitMenu(self,cords,board):
        pass

    #Unit movement functionality--called by graphics
    def getHighlightCords(self,board):
        unit = board.cursor_square().unit
        self.recursiveHighlight(board.cursor,board,unit)
        
        cordarray = []
        
        for col in range(len(board.squares)):
            for sq in range(len(col)):
                if board.squares[col][sq].move_num>0:
                    cordarray.append([col,sq])
                    board.squares[col][sq].move_num=0
        
        return cordarray
    
    def recursiveHighlight(self,cords,board,unit):
        
        #Current moves left at center square
        center = board.find_square(cords).move_num
        
        #Conditional check of grid bounds
        if cords[0] > 0:
            #Moves left at adjacent square, after moving from center
            cost = unit.terrain_costs[board.find_square(cords[0]-1,cords[1]).terrain]
            left = center - cost if cost != "n/a" else 0
        
            #If the adjacent square's moves left are greater than above, do nothing
            #Otherwise, overwrite it
            if(board.find_square(cords[0]-1,cords[1]).move_num<left):
                board.find_square(cords[0]-1,cords[1]).move_num = left
                self.recursiveHighlight((cords[0]-1,cords[1]),board,unit)
        
        if cords[1] > 0:
            cost = unit.terrain_costs[board.find_square(cords[0],cords[1]-1).terrain]
            up = center - cost if cost != "n/a" else 0
        
            if(board.find_square(cords[0],cords[1]-1).move_num<up):
                board.find_square(cords[0],cords[1]-1).move_num = up
                self.recursiveHighlight((cords[0],cords[1]-1),board,unit)
        
        if (cords[0] + 1) < len(board.squares):
            cost = unit.terrain_costs[board.find_square(cords[0]+1,cords[1]).terrain]
            right = center - cost if cost != "n/a" else 0
        
            if(board.find_square(cords[0]+1,cords[1]).move_num<right):
                board.find_square(cords[0]+1,cords[1]).move_num = right
                self.recursiveHighlight((cords[0]+1,cords[1]),board,unit)
        
        if (cords[1] + 1) < len(board.squares[cords[0]]):
            cost = unit.terrain_costs[board.find_square(cords[0],cords[1]+1).terrain]
            down = center - cost if cost != "n/a" else 0
        
            if(board.find_square(cords[0],cords[1]+1).move_num<down):
                board.find_square(cords[0],cords[1]+1).move_num = down
                self.recursiveHighlight((cords[0],cords[1]+1),board,unit)
        
        
    #Get list of building options
    def getBuildOptions(self,board):
        build_opt_list = []
        build_txt_list = []
        for u in board.unit_types:
            if ((u.cost <= board.players[board.current_player].money)):
                b_o = BuildOption.__init__(u)
                build_opt_list.add(b_o.getBuildOpt())
                build_txt_list.add(b_o.getBuildTxt())
        
        #Since this function is directly returned by getOptions, append exit menu right here
        build_opt_list.append(self.exit_menu)
        build_txt_list.append("Nothing")
        
        return build_opt_list,build_txt_list
    
    #End turn and perform passive building actions
    def endTurn(self,board):
        for bldg in board.buildings:
            #If it's controlled by the current player,
            if(bldg.controller == board.current_player()):
                #Then if it's a factory and has a unit on it owned by the player,
#FIX: assumptions about name storage
                if (any([bldg.name=="base",bldg.name=="airport",bldg.name=="port"]) and (bldg.square.unit!=None and bldg.square.unit.controller==board.current_player)):
                    #Then if that unit's damaged,
                    if(bldg.square.unit.hp < bldg.square.unit.max_hp):
                        #Repair it by 20% of its max hp.
                        bldg.square.unit.hp += (bldg.square.unit.max_hp*.2)
                        #If that brings it above full health,
                        if(bldg.square.unit.hp>bldg.square.unit.max_hp):
                            #Set its health back to full.
                            bldg.square.unit.hp = bldg.square.unit.max_hp
                        #Deduct costs of repair from controller's finances.
#FIX: doesn't check if player can afford
                        bldg.square.unit.controller.money -= (bldg.square.unit.cost * 0.2)
                        
                #If it's a city, is controlled by the current player and isn't covered by an enemy unit,
                elif ((bldg.name == "city") and not (bldg.square.unit!=None and bldg.square.unit.controller!=board.current_player())):
                    #Give the current player one MILLION thousandths of a dollar
                    board.current_player().money += 1000
            
        #Increment turn by one
        board.turn += 1
    
    #Will show view options
    def seeOptionsMenu(self,board):
        pass
    
    #Will pickle board & exit to menu -- this may be better in front-end code
    def saveAndQuit(self,board):
        pass

    #Grab top-level action menu
    def getMenuOptions(self,board):
        #Methods that the menu can access
        opts_list = []
        #Descriptive text for each method
        titles_list = []
        
        sqr = board.cursor_square()
        if((sqr.unit!=None) and (sqr.unit.player == board.current_player())):
            pass
#FIX: assumptions about terrain naming
        elif((sqr.unit==None) and (any([str(sqr.terrain)=="base",str(sqr.terrain)=="airport",str(sqr.terrain)=="port"]))):
            return self.getBuildOptions(board)
        
        else:
            opts_list.extend([self.endTurn,self.seeOptionsMenu,self.saveAndQuit])
            titles_list.extend(["End turn","Options","Save and quit"])
        
        #By default return an option to exit the menu
        opts_list.append(self.exit_menu)
        titles_list.append("Nothing")
        
        return opts_list,titles_list

class BuildOption:
    
    def __init__(self,unit_type):
        self.which = unit_type
        
    def build(self,board):
        board.add_unit(self.which,board.cursor)
        board.players[board.current_player()].money -= self.which.cost
        
    def getBuildOpt(self):
        if self.which != None:
            return self.build
        else:
            return None
        
    def getBuildTxt(self):
        if self.which != None:
            return (self.which.name + ": " + self.which.cost)
        else:
            return "Empty build option"

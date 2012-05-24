class Menu:
    
    def __init__(self,board):
		# fetches lists
        # changing this for now since it doesn't seem to point to the right method...
        #self.parts,self.titles = MenuOptions.getOptions(board)
        self.parts,self.titles = MenuOptions().getMenuOptions()
        #Need exception handling for empty lists
        self.selected = 0
        print "Menu initialized"
        
    def scroll_increment(self,inc):
        self.selected = (self.selected + inc) % len(self.parts)
        
    def select(self):
        self.parts[self.selected]()

class MenuOptions:
    
    #Will cause unit to attack another???
    def attack(self,board,cord1,cord2):
        aggressor = board.find_square(cord1).unit
        defender = board.find_square(cord2).unit
        
        if(aggressor.attack(defender) and self.inAttackRange(board,cord1,cord2)):
            defender.attack(aggressor)
        
    
    #Unit capture functionality
    def capture(self,board):
        pass
    
    #Does nothing, as it should
    def exitMenu(self,cords,board):
        pass

    #Unit movement functionality--called by graphics
    def getMoveHighlights(self,board):
        unit = board.cursor_square().unit
#FIX: no handling for missing unit
        self.recursiveHighlight(board.cursor,board,unit)
        
        move_array = []
        
        for col in range(len(board.squares)):
            for sq in range(len(board.squares[col])):
                if board.squares[col][sq].move_num>0:
                    move_array.append([col,sq])
        
        return move_array
    
    #Get the range in which a unit can attack from current position
    def getRangeHighlights(self,board):
        unit = board.cursor_square().unit
#FIX: no handling for missing unit
        return board.cursor_square().find_range(unit.primary_range[0],unit.primary_range[1])
    
    def inAttackRange(self,board, agg_cords, def_cords):
        unit = board.cursor_square().unit
        x_dist = abs(agg_cords[0] - def_cords[0])
        y_dist = abs(agg_cords[1] - def_cords[1])
        return (((x_dist+y_dist) >= unit.primary_range[0]) and ((x_dist+y_dist) <= unit.primary_range[1]))
    
    def getAttackableCords(self,board):
        range_array = self.getRangeHighlights(board)
        
        target_array = []
        
        for cords in range_array:
            if board.find_square(cords).unit != None:
                target_array.append(cords)
        
        return target_array
    
    #Get the range in which a unit can move and the range in which it can attack from movable spaces
    def getMoveAttackHighlights(self,board):
#FIX: no handling for missing unit
        self.recursiveHighlight(board.cursor,board,board.cursor_square().unit)
        
        move_array = []
        attack_array = []
        
        for col in range(len(board.squares)):
            for sq in range(len(board.squares[col])):
                if board.squares[col][sq].move_num != None:
                    if board.squares[col][sq].move_num>0:
                        move_array.append([col,sq])
                    else:
                        attack_array.append([col,sq])
        return move_array,attack_array
    
    def recursiveHighlight(self,cords,board,unit):
        #Reset board move_num state
        for col in board.squares:
            for sq in col:
                sq.move_num = None
        
        #Current moves left at center square
        center = board.find_square(cords).move_num
        
        #Increase the move highlight at an adjacent square, if possible, and return true if successful
        def specificHighlight(specific_cords):
            #Moves remaining at adjacent square, after moving from center
            cost = unit.terrain_costs[board.find_square(specific_cords).terrain]
            moves_left_at = center - cost if cost != "n/a" else 0
            
            specific_square = board.find_square(specific_cords)
            
            #If the value is None, set the value to moves_left_at
            if (specific_square.move_num == None):
                specific_square.move_num = moves_left_at
                #No need to continue recursion if moves_left_at < 0
                return (moves_left_at > 0)
            #If the value exits, (set it to moves_left_at and continue recursion) if moves_left_at is greater
            else:
                if specific_square.move_num < moves_left_at:
                    specific_square.move_num = moves_left_at 
                    return True
                else:
                    return False
            
        #If left adjacent square is in bounds, then if left square can be moved to more efficiently,
        if (cords[0] > 0) and (specificHighlight(cords[0]-1,cords[1])):
            #Highlight left
            self.recursiveHighlight((cords[0]-1,cords[1]),board,unit)
        
        if (cords[1] > 0) and (specificHighlight(cords[0],cords[1]-1)):
            self.recursiveHighlight((cords[0],cords[1]-1),board,unit)
        
        if ((cords[0] + 1) < len(board.squares)) and (specificHighlight(cords[0]+1,cords[1])):
            self.recursiveHighlight((cords[0]+1,cords[1]),board,unit)
        
        if ((cords[1] + 1) < len(board.squares[cords[0]])) and (specificHighlight(cords[0],cords[1]+1)):
            self.recursiveHighlight((cords[0],cords[1]+1),board,unit)
    
    #Get list of building options
    def getBuildOptions(self,board):
		# 
        build_opt_list = []
        # list of strings to pass to the menu constructor
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
        """
        for bldg in board.buildings:
            #If it's controlled by the current player,
            if(bldg.controller == board.current_player()):
                #Then if it's a factory and has a unit on it owned by the player,
                if (any([bldg.name=="Base",bldg.name=="Airport",bldg.name=="Port"]) and (bldg.square.unit!=None and bldg.square.unit.controller==board.current_player)):
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
                #(TV: Instead of the last two, just make sure it's not being 
                captured.)
                elif ((bldg.name == "city") and\
                #not (bldg.square.unit!=None and\
                #bldg.square.unit.controller!=board.current_player())):
                not bldg.being_captured:
                    #Give the current player one MILLION thousandths of a dollar
                    board.current_player().money += 1000
        """
        #Check each building for units to repair
        for current_building in board.buildings:
            #(only check buildings owned by the current player)
            if( current_building.controller == board.current_player() ):
                #Check for a unit at all
                if current_building.square.unit != None:
                    #Match the correct type of unit with the building type
                    current_unit = current_building.square.unit
                    #Ensure the unit can be repaired by the building
                    if current_building.name in board.repair_types.keys() and\
                    current_unit.move_type in board.repair_types[current_building.name]:
                        hp = current_unit.hp
                        max_hp = current_unit.max_hp
                        regen_amount = round(float(max_hp)/10)
                        regen_cost = int(round(0.1 * current_unit.cost))
                        if board.current_player().funds >= regen_cost:
                            if hp + regen_amount >= max_hp:
                                current_unit.hp = current_unit.max_hp
                            else:
                                current_unit.hp += regen_amount
                                boards.current_player().funds -= regen_cost
                #(TV: captured buildings still provide income, and all buildings provide 1000 income.)
                board.current_player().funds += 1000
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
        
        # square has a unit and unit is owned by active player
        # FIXME: add check for the unit having moved already.
        if((sqr.unit!=None) and (sqr.unit.player == board.current_player())):
            opts_list = self.getUnitOptions(sqr.unit)
            pass
		# square has no unit but does have a building that the current player owns
        elif((sqr.unit==None) and (any([str(sqr.terrain.label)=="Base",str(sqr.terrain.label)=="Airport",str(sqr.terrain.label)=="Port"]))) and sqr.controller==board.current_player:
            # return the build menu options
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

# testing block...
if __name__=='__main__':
	import CWE_map
	n = CWE_map.Map('derp')
	m = Menu(n)

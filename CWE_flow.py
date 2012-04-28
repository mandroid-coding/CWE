class Menu:
    
    def __init__(self,cords,board):
        self.parts,self.titles = MenuOptions.getOptions(cords,board)
        #Need exception handling for empty lists
        self.selected = 0
        print("Menu initialized")
        
    def scroll_increment(self,inc):
        self.selected = (self.selected + inc) % len(self.parts)
        
    def select(self):
        self.parts[self.selected]()

class MenuOptions:

#Unit Options
    def move(self,cords,board):
        print("move is working")
    
    def attack(self,cords,board):
        print("attack is working")
    
    def exit_menu(self,cords,board):
        print("exit_menu is working")

#Building options
    def getBuildOptions(self,cords,board):
        build_opt_list = []
        build_txt_list = []
        for u in board.unit_types:
            if ((u.cost <= board.players[board.current_player].money)):
                b_o = BuildOption.__init__(u)
                build_opt_list.add(b_o.getBuildOpt())
                build_txt_list.add(b_o.getBuildTxt())
                
        build_opt_list.append(self.exit_menu)
        build_txt_list.append("Nothing")
        
        return build_opt_list,build_txt_list

#General options
    def endTurn(self,cords,board):
        pass
    
    def seeOptionsMenu(self,cords,board):
        pass
    
    def saveAndQuit(self,cords,board):
        pass

#Grab top-level action menu
    def getOptions(self,cords,board):
        opts_list = []
        titles_list = []
        
        sqr = board.squares[cords[0]][cords[1]]
        if((sqr.unit!=None) and (sqr.unit.player == board.current_player()) and (not sqr.unit.hasMoved)):
            opts_list.append(self.move)
            titles_list.append("Move")
            
        elif((sqr.unit==None) and (any(t==sqr.terrain for t in [1,2,3]))):
            return self.getBuildOptions(cords,board)
        
        else:
            opts_list.extend([self.endTurn,self.seeOptionsMenu,self.saveAndQuit])
            titles_list.extend(["End turn","Options","Save and quit"])
        
        opts_list.append(self.exit_menu)
        titles_list.append("Nothing")
        
        return opts_list,titles_list
    
class BuildOption:
    
    def __init__(self,unit_type):
        self.which = unit_type
        
    def build(self,cords,board):
        board.add_unit(self.which,cords)
        board.players[board.current_player].money -= self.which.cost
        
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
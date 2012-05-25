import sys, Tkinter, pickle, os, tkFileDialog
sys.path.append('./res/imports')
import CWE_map, CWE_terrain, CWE_flow

class Cwe():	
	def __init__(self):
		# how long one side of the square is, referenced in constructing the map and moving the cursor and pieces
		self.side_len = 25
		
		# init root and frame
		self.main = Tkinter.Tk()
		self.frame = Tkinter.Frame(self.main, width=800, height=600, background="black")

		# packs frame
		self.frame.pack()

		# init canvas & place it
		self.canvas = Tkinter.Canvas(self.frame, width=800, height=600, background="darkgreen")
		self.canvas.place(x=0,y=0)
				
		# calls function to display main menu
		self.display_main()

		# main loop called
		self.main.mainloop()
	###################################
	# main menu display and functions #
	###################################
	def display_main(self):
		# sets location
		self.location = 'Main'
		
		# resets the canvas, useful for when there is a need to wipe away the rest of what's on the screen in one fell swoop
		self.canvas = Tkinter.Canvas(self.frame, width=800, height=600, background="darkgreen")
		self.canvas.place(x=0,y=0)
		
		# init variable to track which option is selected
		self.selected=0

		# loading image files to display in main menu
		# saved in self.images for calling later
		self.images = {}
		self.images['title1'] = Tkinter.PhotoImage(file="res/images/title1.gif")
		self.images['new'] = Tkinter.PhotoImage(file="res/images/new_game.gif")
		self.images['load'] = Tkinter.PhotoImage(file="res/images/load_game.gif")
		self.images['exit'] = Tkinter.PhotoImage(file="res/images/exit.gif")
		self.images['selector'] = Tkinter.PhotoImage(file="res/images/tank.gif")		

		# drawing them on teh canvas
		self.selector = self.canvas.create_image(100, 200, anchor="nw", image=self.images['selector'])
		
		# store everything here for easy iteration for changing menu screens
		self.displayed = [self.canvas.create_image(10, 10, anchor="nw", image=self.images['title1']), self.canvas.create_image(200, 200, anchor="nw", image=self.images['new']), self.canvas.create_image(200, 325, anchor="nw", image=self.images['load']), self.canvas.create_image(200, 450, anchor="nw", image=self.images['exit']), self.selector]

		# bindings
		self.main.bind("<Return>", self.main_select)
		self.main.bind("<Up>", self.main_move_up)
		self.main.bind("<Down>", self.main_move_down)
		self.bindings = ["<Return>","<Up>","<Down>"]
	def main_move_up(self, event):
		if self.selected != 0:
			self.canvas.move(self.selector, 0, -125)
			self.selected -= 1
		else:
			self.canvas.move(self.selector, 0, 250)
			self.selected = 2
	def main_move_down(self, event):
		if self.selected != 2:
			self.canvas.move(self.selector, 0, 125)
			self.selected += 1
		else:
			self.canvas.move(self.selector, 0, -250)
			self.selected = 0
	def main_select(self, event):
		# new game
		if self.selected == 0:
			# deletes everything which is currently displayed & clears bindings
			self.clear_all_displayed()
			self.clear_bindings()

			# displays the config menu for new game, just a placeholder right now
			self.display_new_config()
			
			self.new_game(CWE_map.Map(["Player1", "Player2"]))

		# load game
		elif self.selected == 1:
			# clears the images off the screen
			self.clear_all_displayed()
			
			# calls the function to display the save files
			game = tkFileDialog.askopenfilename(filetypes=[('SAV','.sav')], initialdir='./res/save_games', title="Select game to load")
			
			# change var's type
			game.encode('utf-8')
			
			# user canceled
			if game=='':
				self.display_main()
			
			# user selected files
			else:
				# redeclares game as the opened file
				game = open(game, 'r')
				
				# unpickles the instance from the file on disk
				maps = pickle.load(game)
							
				# starts the game
				self.new_game(maps)

		# exit
		elif self.selected == 2:
			self.display_confirmation()
	
	# functions to display pregame config menu
	def display_new_config(self):
		# just a placeholder right now since getting the other stuff done is more important for everyone else.
		pass

	#####################
	# in-game functions #
	#####################
	def new_game(self, game_map):		
		self.location = "Ingame"
		
		self.selected = [0,0]

		# defines testing map		
		# listing each row...
#		col1 = [[0,0,'green'],[0,1,'red'],[0,2,'green'],[0,3,'red']]
#		col2 = [[1,0,'green'],[1,1,'red'],[1,2,'green'],[1,3,'red']]
#		col3 = [[2,0,'green'],[2,1,'red'],[2,2,'green'],[2,3,'red']]
#		col4 = [[3,0,'green'],[3,1,'red'],[3,2,'green'],[3,3,'red']]
#		self.maps = [col1,col2,col3,col4]		


		self.maps = game_map
#		self.maps = CWE_map.Map(["Player1", "Player2"])
		
		
		# bindings
		self.main.bind("<Up>", self.game_move_up)
		self.main.bind("<Left>", self.game_move_left)
		self.main.bind("<Right>", self.game_move_right)
		self.main.bind("<Down>", self.game_move_down)
		self.main.bind("<Return>", self.game_select)
		
		self.bindings = ["<Up>", "<Left>", "<Right>", "<Down>", "<Return>"]
		
		# draws the map
		# iterates through each column
		for i in range(len(self.maps.squares)):
			
			# iterates through each square from the top
			for j in range(len(self.maps.squares[i])):
				self.draw_square(i, j, self.maps.squares[i][j].terrain.color)
				#(TV: Also need to attach unit image here)
				current_square = self.maps.squares[i][j]
				if current_square.unit:
					shown_unit = current_square.unit
					# hande neutral units here
					if shown_unit.controller == None:
						unit_color = "Gray"
					else:
						unit_color = shown_unit.controller.color
					image_filename = "{color}_{unit_type}.gif".format(\
					color = unit_color,\
					unit_type = shown_unit.image_type )
		# Loads selector image
		self.images['game_selector'] = Tkinter.PhotoImage(file="res/images/game_selector.gif")
		self.game_selector = self.canvas.create_image(0, 0, anchor="nw", image=self.images['game_selector'])
		self.displayed.append(self.game_selector)
	
	# fix this
	def draw_square(self, x, y, color):
		self.canvas.create_rectangle(self.side_len*x, self.side_len*y, self.side_len*x+self.side_len, self.side_len*y+self.side_len, fill=color)
	def game_move_up(self, event):
		try:
			# calculates new indices
			newx = self.selected[0]
			newy = self.selected[1] - 1
			
			#FIXME: this is hackish right now because using negative integers as list indices makes python access the
			# list backwards.  This will work for now but it may need a more permanent fix.
			if newy < 0:
				raise IndexError

			# selects new square.  This is where the IndexError is thrown if no square exists
			newsquare = self.maps.squares[newx][newy]
			# resets the coords of the selector
			self.selected = [newx, newy]
			# finally moves the cursor
			self.canvas.move(self.game_selector, 0, -self.side_len)
		# catches the error thrown when no square exists
		except IndexError:
			pass
	def game_move_left(self, event):
		try:
			# calculates new indices
			newx = self.selected[0] - 1
			newy = self.selected[1]
			
			#FIXME: this is hackish right now because using negative integers as list indices makes python access the
			# list backwards.  This will work for now but it may need a more permanent fix.
			if newx < 0:
				raise IndexError
			
			# selects new square.  This is where the IndexError is thrown if no square exists
			newsquare = self.maps.squares[newx][newy]
			# resets the coords of the selector
			self.selected = [newx, newy]
			# finally moves the cursor
			self.canvas.move(self.game_selector, -self.side_len, 0)
		# catches the error thrown when no square exists
		except IndexError:
			pass
	def game_move_right(self, event):
		try:
			# calculates new indices
			newx = self.selected[0]+1
			newy = self.selected[1]
			# selects new square.  This is where the IndexError is thrown if no square exists
			newsquare = self.maps.squares[newx][newy]
			# resets the coords of the selector
			self.selected = [newx, newy]
			# finally moves the cursor
			self.canvas.move(self.game_selector, self.side_len, 0)
		# catches the error thrown when no square exists
		except IndexError:
			pass
	def game_move_down(self, event):
		try:
			# calculates new indices
			newx = self.selected[0]
			newy = self.selected[1] + 1
			# selects new square.  This is where the IndexError is thrown if no square exists
			newsquare = self.maps.squares[newx][newy]
			# resets the coords of the selector
			self.selected = [newx, newy]
			# finally moves the cursor
			self.canvas.move(self.game_selector, 0, self.side_len)
		# catches the error thrown when no square exists
		except IndexError:
			pass
	def game_select(self, event):
		# FIXME: add check for if there's no unit and no building
		self.display_game_menu()
		menu=CWE_flow.MenuOptions().getMenuOptions(self.maps)
		

	########################
	# ingame menu functions#
	########################
	def display_game_menu(self):
		self.menu_selector = 0
		
		#update bindings
		self.clear_bindings()			
		self.main.bind("<Up>", self.game_menu_up)
		self.main.bind("<Down>", self.game_menu_down)
		self.main.bind("<Return>", self.game_menu_select)
		self.bindings = ["<Up>","<Down>","<Return>"]

		self.images['ingame_menu'] = self.canvas.create_rectangle(600, 485, 800, 600, outline='white', fill="red")
		self.images['ingame_back_to_game'] = self.canvas.create_text(700,505, text="Back To Game", fill='green')
		self.images['ingame_end_turn'] = self.canvas.create_text(700,525, text="End Turn", fill='green')
		self.images['ingame_stats'] = self.canvas.create_text(700,545, text="Stats", fill='green')
		self.images['ingame_save'] = self.canvas.create_text(700,565, text="Save", fill='green')
		self.images['ingame_quit'] = self.canvas.create_text(700,585, text="Main Menu", fill='green')
		self.images['ingame_selector'] = self.canvas.create_rectangle(650,495,755,515, outline='green')

		self.game_menu_imgs = [self.images['ingame_selector'],self.images['ingame_quit'],self.images['ingame_back_to_game'],self.images['ingame_menu'],self.images['ingame_end_turn'],self.images['ingame_stats'],self.images['ingame_save']]
	def game_menu_up(self, event):
		if self.menu_selector!=0:
			self.menu_selector -= 1
			self.canvas.move(self.images['ingame_selector'], 0, -20)
		else: 
			self.menu_selector = 4
			self.canvas.move(self.images['ingame_selector'], 0, 80)
	def game_menu_down(self, event):
		if self.menu_selector!=4:
			self.menu_selector += 1
			self.canvas.move(self.images['ingame_selector'], 0, 20)
		else: 
			self.menu_selector = 0
			self.canvas.move(self.images['ingame_selector'], 0, -80)
	def game_menu_select(self, event):
		# back to game
		if self.menu_selector==0:
			for i in self.game_menu_imgs:
				self.canvas.delete(i)
			# bindings
			self.main.bind("<Up>", self.game_move_up)
			self.main.bind("<Left>", self.game_move_left)
			self.main.bind("<Right>", self.game_move_right)
			self.main.bind("<Down>", self.game_move_down)
			self.main.bind("<Return>", self.game_select)
			
			self.bindings = ["<Up>", "<Left>", "<Right>", "<Down>", "<Return>"]
			
		# end turn
		if self.menu_selector==1:
			print "end turn"

		# stats menu
		if self.menu_selector==2:
			print "stats menu"
			
		# save game
		if self.menu_selector==3:
			self.display_save()
			
		# end game
		if self.menu_selector == 4:
			self.display_confirmation()


	##############################
	# exit confirmation functions#
	##############################
	def display_confirmation(self):
		# displays confirmation message
		
		# clears old bindings
		self.clear_bindings()
			
		# keeps track of where the selector is
		self.confirmation_selection = 1
			
		# makes new bindings
		self.main.bind("<Return>", self.confirmation_select)
		self.main.bind("<Left>", self.confirmation_left)
		self.main.bind("<Right>", self.confirmation_right)
		self.bindings = ["<Return>", "<Left>", "<Right>"]

		# adds images to working canvas list
		self.images['confirm_box'] = self.canvas.create_rectangle(200, 200, 600, 400, outline='white', fill="red")
		self.images['yesno'] = Tkinter.PhotoImage(file='res/images/yesno.gif')
		self.images['exit_selector'] = self.canvas.create_rectangle(420, 335, 465, 365, outline='darkgreen')
		self.images['confirm_text'] = Tkinter.PhotoImage(file="res/images/confirm.gif")
		
		self.confirmation_images = [self.canvas.create_image(203, 202, anchor="nw", image=self.images['confirm_text'])]
		self.confirmation_images += [self.images['exit_selector'], self.images['confirm_box'], self.canvas.create_image(325, 325, anchor="nw", image=self.images['yesno'])]
	def confirmation_right(self, event):
		# it can only move right if it selects the 0th element because there are only 2 elements
		if self.confirmation_selection == 0:
			self.canvas.move(self.images['exit_selector'], 91, 0)
			self.confirmation_selection = 1
	def confirmation_left(self,event):
		if self.confirmation_selection == 1:
			self.canvas.move(self.images['exit_selector'], -91, 0)
			self.confirmation_selection = 0
	def confirmation_select(self, event):		
		# fork for main menu
		if self.location=='Main':
			if self.confirmation_selection==0:
				print 'Come play again soon!!'
				self.main.destroy()
			elif self.confirmation_selection==1:
				self.clear_all_displayed()
				self.clear_bindings()
				self.display_main()

		# fork for ingame
		elif self.location=='Ingame':
			if self.confirmation_selection==0:
				self.display_main()
			elif self.confirmation_selection==1:
				self.clear_confirmation()
				
				# rebind ingame menu bindings
				self.clear_bindings()			
				self.main.bind("<Up>", self.game_menu_up)
				self.main.bind("<Down>", self.game_menu_down)
				self.main.bind("<Return>", self.game_menu_select)
				self.bindings = ["<Up>","<Down>","<Return>"]
	def clear_confirmation(self):
		for i in self.confirmation_images:
			self.canvas.delete(i)
	
	###############################
	# save confirmation functions #
	###############################	
	# saves the game
	def game_save(self):
		# build directory
		directory = './res/save_games/'+self.images['save_entry'].get()+'.sav'
		
		# open file and save
		fileobj = open(directory, 'w')
		pickle.dump(self.maps, fileobj)
		fileobj.close()
		
		# closes the save confirmation window
		self.save_cancel()
	# displays the save confirmation
	def display_save(self):
		# clears old bindings
		self.clear_bindings()
			
		# keeps track of where the selector is
		self.confirmation_selection = 1

		# display images
		self.images['confirm_box'] = self.canvas.create_rectangle(250, 200, 550, 400, outline='white', fill="red")
		self.images['iputatexonimaeg'] = self.canvas.create_text(400, 225, text="Enter a name", fill='green', font=("Arial", 30))
		
		# build widgets
		self.images['save_entry'] = Tkinter.Entry(self.canvas)
		self.images['save_entry'].place(x=320,y=275)
		self.images['confirm'] = Tkinter.Button(self.canvas, text='Save', background='darkgreen', foreground='red', command=self.game_save)
		self.images['confirm'].place(x=320, y=340)
		self.images['cancel'] = Tkinter.Button(self.canvas, text='Cancel', background='darkgreen', foreground='red', command=self.save_cancel)
		self.images['cancel'].place(x=425, y=340)
		
		self.save_images = [self.images['confirm_box'],self.images['iputatexonimaeg'],self.images['save_entry']]
	# removes the save confirmation
	def save_cancel(self):
		# destroy the widgets
		self.images['confirm'].destroy()
		self.images['cancel'].destroy()
		self.images['save_entry'].destroy()
		
		# delete the canvas images
		for i in self.save_images:
			self.canvas.delete(i)

		# update bindings
		self.clear_bindings()			
		self.main.bind("<Up>", self.game_menu_up)
		self.main.bind("<Down>", self.game_menu_down)
		self.main.bind("<Return>", self.game_menu_select)
		self.bindings = ["<Up>","<Down>","<Return>"]


	###################################################
	# functions able to be called from any game state #
	###################################################
	def clear_all_displayed(self):
		# deletes canvas images and resets iterator
		for i in self.displayed:
			self.canvas.delete(i)
		self.displayed = []
		
		# resets images loaded
		self.images = {}
	def clear_bindings(self):
		for i in self.bindings:
			self.main.unbind(i)
		self.bindings=[]
	
		
if __name__=="__main__":
	app = Cwe()

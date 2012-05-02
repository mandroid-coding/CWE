import Tkinter
import math, sys

root = Tkinter.Tk()
hex_side=30
height = 2*30*.866
width = 30*1.5
imported = [[100,100,"Green","Plains", None],[100,100+height,"DarkGreen","Woods", None],[100+width,100+height/2,"#DB0F47","Factory", 0],[100+width,100-height/2,"Green","Plains", None],[100,100-height,"LightBlue","Factory", 1],[100-width,100-height/2,"Green","Plains", None],[100-width,100+height/2,"Green","Plains", None]]

class Application():
	##WIDGETS##
	def rightwidgets(self):
		global turn_label
		turn_label = Tkinter.Label(text="Player {}'s Turn".format(self.current_player + 1))
		turn_label.place(x=1000, y=0, anchor="ne")
		global current_turn_label
		current_turn_label = Tkinter.Label(text="Current Turn: {}".format(self.current_turn))
		current_turn_label.place(x=1000, y=22, anchor="ne")
		
		
		b = Tkinter.Button(frame, text="End Turn", command=self.EndTurn)
		b.place(x=915, y=0, anchor="ne")
		b = Tkinter.Button(frame, text="Properties", command=self.properties)
		b.place(x=1000, y=90, anchor="ne")	
		b = Tkinter.Button(frame, text="Capture", command=self.capture)
		b.place(x=935, y=90, anchor="ne")
		b = Tkinter.Button(frame, text="Attack", command=self.attack)
		b.place(x=880, y=90, anchor="ne")
		
		##UNIT MOVEMENT##
		l = Tkinter.Label(frame, text="Unit\nMovement:")
		l.place(x=895, y=640, anchor="se")		
		b = Tkinter.Button(frame, text="", width=2, command=self.MoveUnitDownLeft)
		b.place(x=845, y=700, anchor="se")
		b = Tkinter.Button(frame, text="", width=2, command=self.MoveUnitDown)
		b.place(x=875, y=700, anchor="se")
		b = Tkinter.Button(frame, text="", width=2, command=self.MoveUnitDownRight)
		b.place(x=905, y=700, anchor="se")
		b = Tkinter.Button(frame, text="", width=2, command=self.MoveUnitUpRight)
		b.place(x=905, y=670, anchor="se")
		b = Tkinter.Button(frame, text="", width=2, command=self.MoveUnitUp)
		b.place(x=875, y=670, anchor="se")
		b = Tkinter.Button(frame, text="", width=2, command=self.MoveUnitUpLeft)
		b.place(x=845, y=670, anchor="se")		
		
		##CURSOR MOVEMENT##
		l = Tkinter.Label(frame, text="Cursor\nMovement:")
		l.place(x=990, y=640, anchor="se")		
		b = Tkinter.Button(frame, text="", width=2, command=self.downleft)
		b.place(x=940, y=700, anchor="se")
		b = Tkinter.Button(frame, text="", width=2, command=self.down)
		b.place(x=970, y=700, anchor="se")
		b = Tkinter.Button(frame, text="", width=2, command=self.downright)
		b.place(x=1000, y=700, anchor="se")
		b = Tkinter.Button(frame, text="", width=2, command=self.upright)
		b.place(x=1000, y=670, anchor="se")
		b = Tkinter.Button(frame, text="", width=2, command=self.up)
		b.place(x=970, y=670, anchor="se")
		b = Tkinter.Button(frame, text="", width=2, command=self.upleft)
		b.place(x=940, y=670, anchor="se")
	def leftwidgets(self):
		global money_label
		money_label = Tkinter.Label(frame, width=12, height=1, text="Money: {}".format(self.playermoney[self.current_player]))
		money_label.place(x=0, y=0, anchor="nw")
		Tkinter.Label(frame, width=12, height=1, text="Build:").place(x=0, y=22, anchor="nw")
		b = Tkinter.Button(frame, width=12, height=1, text="Light Inf.", command=self.BuildLightInf)
		b.place(x=0, y=44, anchor="nw")
		b = Tkinter.Button(frame, width=12, height=1, text="Heavy Inf.", command=self.BuildHeavyInf)
		b.place(x=0, y=70, anchor="nw")
		b = Tkinter.Button(frame, width=12, height=1, text="Light Cav.", command=self.BuildLightCav)
		b.place(x=0, y=96, anchor="nw")
		b = Tkinter.Button(frame, width=12, height=1, text="Heavy Cav.", command=self.BuildHeavyCav)
		b.place(x=0, y=122, anchor="nw")		
		b = Tkinter.Button(frame, width=12, height=1, text="Archers", command=self.BuildArchers)
		b.place(x=0, y=148, anchor="nw")
		
	##METHODS##
	def BuildLightInf(self):
		if self.cursor.terrain != "Factory":
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot build unless on Factory.")
		elif self.current_player != self.cursor.controller:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot build on opponent's Factory.")			
		elif self.playermoney[self.current_player] - 100 <0:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Not enough money.")
		elif self.cursor.unit == None and self.cursor.terrain=="Factory":
			self.cursor.unit = LightInf(self.current_player)
			self.Map[self.cursor.Map_index].unit = self.cursor.unit
			self.DrawUnit(self.cursor.unit.color)
			self.playermoney[self.current_player] -= self.cursor.unit.price
			money_label.configure(text="Money: {}".format(self.playermoney[self.current_player]))
		elif self.cursor.unit!=None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Unit already occupying hex.")
	def BuildHeavyInf(self):
		if self.cursor.terrain != "Factory":
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot build unless on Factory.")
		elif self.current_player != self.cursor.controller:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot build on opponent's Factory.")	
		elif self.playermoney[self.current_player] - 300 <0:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Not enough money.")
		elif self.cursor.unit == None and self.cursor.terrain=="Factory":
			self.cursor.unit = HeavyInf(self.current_player)
			self.Map[self.cursor.Map_index].unit = self.cursor.unit
			self.DrawUnit(self.cursor.unit.color)
			self.playermoney[self.current_player] -= self.cursor.unit.price
			money_label.configure(text="Money: {}".format(self.playermoney[self.current_player]))
		elif self.cursor.unit!=None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Unit already occupying hex.")
	def BuildLightCav(self):
		if self.cursor.terrain != "Factory":
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot build unless on Factory.")
		elif self.current_player != self.cursor.controller:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot build on opponent's Factory.")	
		elif self.playermoney[self.current_player] - 800 <0:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Not enough money.")
		elif self.cursor.unit == None and self.cursor.terrain=="Factory":
			self.cursor.unit = LightCav(self.current_player)
			self.Map[self.cursor.Map_index].unit = self.cursor.unit
			self.DrawUnit(self.cursor.unit.color)
			self.playermoney[self.current_player] -= self.cursor.unit.price
			money_label.configure(text="Money: {}".format(self.playermoney[self.current_player]))
		elif self.cursor.unit!=None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Unit already occupying hex.")
	def BuildHeavyCav(self):
		if self.cursor.terrain != "Factory":
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot build unless on Factory.")
		elif self.current_player != self.cursor.controller:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot build on opponent's Factory.")	
		elif self.playermoney[self.current_player] - 700 <0:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Not enough money.")
		elif self.cursor.unit == None and self.cursor.terrain=="Factory":
			self.cursor.unit = HeavyCav(self.current_player)
			self.Map[self.cursor.Map_index].unit = self.cursor.unit
			self.DrawUnit(self.cursor.unit.color)
			self.playermoney[self.current_player] -= self.cursor.unit.price
			money_label.configure(text="Money: {}".format(self.playermoney[self.current_player]))
		elif self.cursor.unit!=None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Unit already occupying hex.")
	def BuildArchers(self):
		if self.cursor.terrain != "Factory":
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot build unless on Factory.")
		elif self.current_player != self.cursor.controller:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot build on opponent's Factory.")	
		elif self.playermoney[self.current_player] - 600 <0:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Not enough money.")
		elif self.cursor.unit == None and self.cursor.terrain=="Factory":
			self.cursor.unit = Archers(self.current_player)
			self.Map[self.cursor.Map_index].unit = self.cursor.unit
			self.DrawUnit(self.cursor.unit.color)
			self.playermoney[self.current_player] -= self.cursor.unit.price
			money_label.configure(text="Money: {}".format(self.playermoney[self.current_player]))
		elif self.cursor.unit!=None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Unit already occupying hex.")

	def DrawUnit(self, color):
		canvas.create_rectangle(self.cursor.vertex[0]+hex_side/2, self.cursor.vertex[1]+15, self.cursor.vertex[0]+1.5*hex_side, self.cursor.vertex[1]-15, fill=color)		# 30x30 square
	
	def capture(self):
		if self.cursor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot capture unless using L. or H. Infantry.")				
		elif self.cursor.unit.name != "Light Infantry" and self.cursor.unit.name != "Heavy Infantry":
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot capture unless using L. or H. Infantry.")		
		elif self.cursor.terrain != "Factory" and self.cursor.terrain != "City" and self.cursor.terrain != "Capitol":
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot capture unless on a Factory, City or Capitol.")			
		elif self.cursor.unit.controller != self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot capture with opponent's units.")
		elif self.cursor.controller==self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot capture your own territory.")
		elif self.cursor.unit.captured == 1:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot capture more than once per unit per turn.")	
		else:
			self.cursor.hp -= self.cursor.unit.health/2
			self.cursor.unit.captured = 1
			if self.cursor.hp <= 0:
				self.cursor.controller = self.cursor.unit.controller
				self.cursor.hp = 10
				text.delete(1.0, "end")
				text.insert(1.0, "Success! Territory captured!.")				
		print "working"
	def attack(self):
		if self.cursor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack without a unit.")
		elif self.cursor.unit.attacked == 1:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Units can only attack once per turn.")
		elif self.cursor.unit.controller != self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot use opponent's units.")
		else:
			t = Tkinter.Toplevel()
			l = Tkinter.Label(t, text="Attack which direction?")
			l.grid(columnspan=3, row=0, column=0)		
			b = Tkinter.Button(t, width=2, text="", command=self.attackupleft)
			b.grid(row=1, column=0)
			b = Tkinter.Button(t, width=2, text="", command=self.attackup)
			b.grid(row=1, column=1)		
			b = Tkinter.Button(t, width=2, text="", command=self.attackupright)
			b.grid(row=1, column=2)
			b = Tkinter.Button(t, width=2, text="", command=self.attackdownleft)
			b.grid(row=2, column=0)
			b = Tkinter.Button(t, width=2, text="", command=self.attackdown)
			b.grid(row=2, column=1)
			b = Tkinter.Button(t, width=2, text="", command=self.attackdownright)
			b.grid(row=2, column=2)
			print "working"
	def EndTurn(self):
		for i in range(len(self.numberofplayers)):
			if self.current_player==self.numberofplayers[i]:
				print "working"
				print self.playermoney[0], self.playermoney[1]
				try:
					self.current_player = self.numberofplayers[i+1]
					money_label.configure(text="Money: {}".format(self.playermoney[i+1]))
					turn_label.configure(text="Player {}'s Turn".format(self.numberofplayers[i+1]+1))
					self.playermoney[i+1] += 100*self.player_buildings[i+1]
					for i in self.Map:
						if i.unit != None:
							i.unit.movement_left = i.unit.movement
					break
				except:
					self.current_player = self.numberofplayers[0]
					money_label.configure(text="Money: {}".format(self.playermoney[0]))
					turn_label.configure(text="Player {}'s Turn".format(self.numberofplayers[0]+1))
					self.playermoney[0] += 100*self.player_buildings[0]
					for i in self.Map:
						if i.unit != None:
							i.unit.movement_left = i.unit.movement
					break
		for i in self.Map:
			if i.unit == None:
				pass
			else:
				i.unit.attacked=0
			if i.unit != None and i.unit.name=="Light Infantry" or i.unit != None and i.unit.name=="Heavy Infantry":
				i.unit.captured = 0
		self.current_turn += 1
		print self.current_turn
		current_turn_label.configure(text="Current Turn: {}".format(self.current_turn))

	##ATTACK DIRECTIONS##
	def attackupleft(self):
		if self.cursor.unit.attacked == 1:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Units can only attack once per turn.")		
		elif self.cursor.upleft_neighbor == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack a hex that doesn't exist.")
		elif self.cursor.upleft_neighbor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit exists in specified attack coordinates.")
		elif self.cursor.upleft_neighbor.unit.controller==self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack your own units.")
		else:
			print "working"
			self.cursor.unit.attacked = 1
	def attackup(self):
		if self.cursor.unit.attacked == 1:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Units can only attack once per turn.")	
		elif self.cursor.up_neighbor == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack a hex that doesn't exist.")
		elif self.cursor.up_neighbor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit exists in specified attack coordinates.")
		elif self.cursor.up_neighbor.unit.controller==self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack your own units.")
		else:
			print "working"
			self.cursor.unit.attacked = 1
	def attackupright(self):
		if self.cursor.unit.attacked == 1:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Units can only attack once per turn.")	
		elif self.cursor.upright_neighbor == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack a hex that doesn't exist.")
		elif self.cursor.upright_neighbor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit exists in specified attack coordinates.")
		elif self.cursor.upright_neighbor.unit.controller==self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack your own units.")
		else:
			print "working"
			self.cursor.unit.attacked = 1
	def attackdownleft(self):
		if self.cursor.unit.attacked == 1:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Units can only attack once per turn.")	
		elif self.cursor.downleft_neighbor == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack a hex that doesn't exist.")
		elif self.cursor.downleft_neighbor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit exists in specified attack coordinates.")
		elif self.cursor.downleft_neighbor.unit.controller==self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack your own units.")
		else:
			print "working"
			self.cursor.unit.attacked = 1
	def attackdown(self):
		if self.cursor.unit.attacked == 1:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Units can only attack once per turn.")	
		elif self.cursor.down_neighbor == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack a hex that doesn't exist.")
		elif self.cursor.down_neighbor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit exists in specified attack coordinates.")
		elif self.cursor.down_neighbor.unit.controller==self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack your own units.")
		else:
			print "working"
			self.cursor.unit.attacked = 1
	def attackdownright(self):
		if self.cursor.unit.attacked == 1:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Units can only attack once per turn.")	
		elif self.cursor.downright_neighbor == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack a hex that doesn't exist.")
		elif self.cursor.downright_neighbor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit exists in specified attack coordinates.")
		elif self.cursor.downright_neighbor.unit.controller==self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: Cannot attack your own units.")
		else:
			print "working"
			self.cursor.unit.attacked = 1	

	##CURSOR MOVEMENT##
	def upleft(self):
		if self.cursor.upleft_neighbor==None:
			text.delete(1.0, END)
			text.insert(1.0, "Error: No adjacent hex to move to.")
			
		elif self.cursor.unit == None and self.cursor.upleft_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.upleft_neighbor
			self.cursor.draw_red_hex()
			
		elif self.cursor.unit == None and self.cursor.upleft_neighbor.unit != None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.upleft_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
		
		elif self.cursor.unit != None and self.cursor.upleft_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.upleft_neighbor
			self.cursor.draw_red_hex()
			
		else:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.upleft_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
	def up(self):
		if self.cursor.up_neighbor==None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No adjacent hex to move to.")
			
		elif self.cursor.unit == None and self.cursor.up_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.up_neighbor
			self.cursor.draw_red_hex()
			
		elif self.cursor.unit == None and self.cursor.up_neighbor.unit != None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.up_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
		
		elif self.cursor.unit != None and self.cursor.up_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.up_neighbor
			self.cursor.draw_red_hex()
			
		else:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.up_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
	def upright(self):
		if self.cursor.upright_neighbor==None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No adjacent hex to move to.")
			
		elif self.cursor.unit == None and self.cursor.upright_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.upright_neighbor
			self.cursor.draw_red_hex()
			
		elif self.cursor.unit == None and self.cursor.upright_neighbor.unit != None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.upright_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
		
		elif self.cursor.unit != None and self.cursor.upright_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.upright_neighbor
			self.cursor.draw_red_hex()
			
		else:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.upright_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
	def downright(self):
		if self.cursor.downright_neighbor==None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No adjacent hex to move to.")
			
		elif self.cursor.unit == None and self.cursor.downright_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.downright_neighbor
			self.cursor.draw_red_hex()
			
		elif self.cursor.unit == None and self.cursor.downright_neighbor.unit != None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.downright_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
		
		elif self.cursor.unit != None and self.cursor.downright_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.downright_neighbor
			self.cursor.draw_red_hex()
			
		else:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.downright_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
	def down(self):
		if self.cursor.down_neighbor==None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No adjacent hex to move to.")
			
		elif self.cursor.unit == None and self.cursor.down_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.down_neighbor
			self.cursor.draw_red_hex()
			
		elif self.cursor.unit == None and self.cursor.down_neighbor.unit != None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.down_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
		
		elif self.cursor.unit != None and self.cursor.down_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.down_neighbor
			self.cursor.draw_red_hex()
			
		else:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.down_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
	def downleft(self):
		if self.cursor.downleft_neighbor==None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No adjacent hex to move to.")
			
		elif self.cursor.unit == None and self.cursor.downleft_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.downleft_neighbor
			self.cursor.draw_red_hex()
			
		elif self.cursor.unit == None and self.cursor.downleft_neighbor.unit != None:
			self.cursor.draw_black_hex()
			self.cursor = self.cursor.downleft_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)
		
		elif self.cursor.unit != None and self.cursor.downleft_neighbor.unit == None:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.downleft_neighbor
			self.cursor.draw_red_hex()
			
		else:
			self.cursor.draw_black_hex()
			self.DrawUnit(self.cursor.unit.color)
			self.cursor = self.cursor.downleft_neighbor
			self.cursor.draw_red_hex()
			self.DrawUnit(self.cursor.unit.color)

	##UNIT MOVEMENT##
	def MoveUnitDownLeft(self):
		if self.cursor.unit != None and self.cursor.unit.movement_left > 0:
			if self.cursor.downleft_neighbor ==None:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: No adjacent hex")
			elif self.cursor.unit.controller != self.current_player:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: You may only move your own units.")
			elif self.cursor.downleft_neighbor.unit == None:
				self.cursor.draw_black_hex()
				self.cursor.downleft_neighbor.unit = self.cursor.unit
				self.cursor.unit = None 
				self.cursor = self.cursor.downleft_neighbor
				self.cursor.draw_red_hex()
				self.DrawUnit(self.cursor.unit.color)
				self.cursor.unit.movement_left -= (1 + self.cursor.unit.movement_modifiers[self.cursor.terrain])
			else:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: Hex already occupied.")
		elif self.cursor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit to move.")
		else:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No movement left this turn for this unit.")
	def MoveUnitDown(self):
		if self.cursor.unit != None and self.cursor.unit.movement_left > 0:
			if self.cursor.down_neighbor ==None:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: No adjacent hex")		
			elif self.cursor.unit.controller != self.current_player:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: You may only move your own units.")
			elif self.cursor.down_neighbor.unit == None:
				self.cursor.draw_black_hex()
				self.cursor.down_neighbor.unit = self.cursor.unit
				self.cursor.unit = None 
				self.cursor = self.cursor.down_neighbor
				self.cursor.draw_red_hex()
				self.DrawUnit(self.cursor.unit.color)
				self.cursor.unit.movement_left -= (1 + self.cursor.unit.movement_modifiers[self.cursor.terrain])
			else:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: Hex already occupied.")
		elif self.cursor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit to move.")
		elif self.cursor.unit.controller != self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: You may only move your own units.")
		else:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No movement left this turn for this unit.")
	def MoveUnitDownRight(self):
		if self.cursor.unit != None and self.cursor.unit.movement_left > 0:
			if self.cursor.downright_neighbor ==None:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: No adjacent hex")		
			elif self.cursor.unit.controller != self.current_player:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: You may only move your own units.")
			elif self.cursor.downright_neighbor.unit == None:
				self.cursor.draw_black_hex()
				self.cursor.downright_neighbor.unit = self.cursor.unit
				self.cursor.unit = None 
				self.cursor = self.cursor.downright_neighbor
				self.cursor.draw_red_hex()
				self.DrawUnit(self.cursor.unit.color)
				self.cursor.unit.movement_left -= (1 + self.cursor.unit.movement_modifiers[self.cursor.terrain])
			else:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: Hex already occupied.")
		elif self.cursor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit to move.")
		elif self.cursor.unit.controller != self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: You may only move your own units.")
		else:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No movement left this turn for this unit.")
	def MoveUnitUpRight(self):
		if self.cursor.unit != None and self.cursor.unit.movement_left > 0:
			if self.cursor.upright_neighbor ==None:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: No adjacent hex")		
			elif self.cursor.unit.controller != self.current_player:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: You may only move your own units.")
			elif self.cursor.upright_neighbor.unit == None:
				self.cursor.draw_black_hex()
				self.cursor.upright_neighbor.unit = self.cursor.unit
				self.cursor.unit = None 
				self.cursor = self.cursor.upright_neighbor
				self.cursor.draw_red_hex()
				self.DrawUnit(self.cursor.unit.color)
				self.cursor.unit.movement_left -= (1 + self.cursor.unit.movement_modifiers[self.cursor.terrain])
			else:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: Hex already occupied.")
		elif self.cursor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit to move.")
		elif self.cursor.unit.controller != self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: You may only move your own units.")
		else:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No movement left this turn for this unit.")
	def MoveUnitUp(self):
		if self.cursor.unit != None and self.cursor.unit.movement_left > 0:
			if self.cursor.up_neighbor ==None:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: No adjacent hex")
			elif self.cursor.unit.controller != self.current_player:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: You may only move your own units.")
			elif self.cursor.up_neighbor.unit == None:
				self.cursor.draw_black_hex()
				self.cursor.up_neighbor.unit = self.cursor.unit
				self.cursor.unit = None 
				self.cursor = self.cursor.up_neighbor
				self.cursor.draw_red_hex()
				self.DrawUnit(self.cursor.unit.color)
				self.cursor.unit.movement_left -= (1 + self.cursor.unit.movement_modifiers[self.cursor.terrain])
			else:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: Hex already occupied.")
		elif self.cursor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit to move.")
		elif self.cursor.unit.controller != self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: You may only move your own units.")
		else:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No movement left this turn for this unit.")
	def MoveUnitUpLeft(self):
		if self.cursor.unit != None and self.cursor.unit.movement_left > 0:
			if self.cursor.upleft_neighbor == None:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: No adjacent hex.")
			elif self.cursor.unit.controller != self.current_player:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: You may only move your own units.")
			elif self.cursor.upleft_neighbor.unit == None:
				self.cursor.draw_black_hex()
				self.cursor.upleft_neighbor.unit = self.cursor.unit
				self.cursor.unit = None 
				self.cursor = self.cursor.upleft_neighbor
				self.cursor.draw_red_hex()
				self.DrawUnit(self.cursor.unit.color)
				self.cursor.unit.movement_left -= (1 + self.cursor.unit.movement_modifiers[self.cursor.terrain])
			else:
				text.delete(1.0, "end")
				text.insert(1.0, "Error: Hex already occupied.")
		elif self.cursor.unit == None:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No unit to move.")
		elif self.cursor.unit.controller != self.current_player:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: You may only move your own units.")
		else:
			text.delete(1.0, "end")
			text.insert(1.0, "Error: No movement left this turn for this unit.")



	def properties(self):
		text.delete(1.0, "end")
		if self.cursor.unit==None and self.cursor.controller==None:
			text.insert(1.0,"Properties of current hex:\n\nTerrain: {}\nControlling Player: {}\nUnit: None".format(self.cursor.terrain, self.cursor.controller))
		elif self.cursor.unit==None:
			text.insert(1.0,"Properties of current hex:\n\nTerrain: {}\nControlling Player: {}\nTerrain HP: {}\nUnit: None".format(self.cursor.terrain, self.cursor.controller+1, self.cursor.hp))
		elif self.cursor.controller==None:
			text.insert(1.0,"Properties of current hex:\n\nTerrain: {}\nControlling Player: {}\nTerrain HP: {}\n\nUnit Stats:\nType: {}\nController: Player {}\nMovement/Turn: {}\nMovement Left: {}\nAttack: {}\nDefense: {}\nAttack Range: {}\n\nUnit Movement Modifiers:\nPlains: {}\nWoods: {}\nMountains: {}".format(self.cursor.terrain, self.cursor.controller, self.cursor.hp, self.cursor.unit.name, self.cursor.unit.controller+1, self.cursor.unit.movement, self.cursor.unit.movement_left, self.cursor.unit.attack, self.cursor.unit.defense, self.cursor.unit.attack_range, self.cursor.unit.movement_modifiers["Plains"], self.cursor.unit.movement_modifiers["Woods"], self.cursor.unit.movement_modifiers["Mountains"]))
		else:
			text.insert(1.0,"Properties of current hex:\n\nTerrain: {}\nControlling Player: {}\nTerrain HP: {}\n\nUnit Stats:\nType: {}\nController: Player {}\nMovement/Turn: {}\nMovement Left: {}\nAttack: {}\nDefense: {}\nAttack Range: {}\n\nUnit Movement Modifiers:\nPlains: {}\nWoods: {}\nMountains: {}".format(self.cursor.terrain, self.cursor.controller+1, self.cursor.hp, self.cursor.unit.name, self.cursor.unit.controller+1, self.cursor.unit.movement, self.cursor.unit.movement_left, self.cursor.unit.attack, self.cursor.unit.defense, self.cursor.unit.attack_range, self.cursor.unit.movement_modifiers["Plains"], self.cursor.unit.movement_modifiers["Woods"], self.cursor.unit.movement_modifiers["Mountains"]))

	def import_map(self, imported):				# Imports a map which is a list of the coordinates of the leftmost vertex of the hex and
		for i in range(len(imported)):								# other data associated with the hexagon  # draws them
			new_hex = Hex(imported[i][0], imported[i][1], imported[i][2], imported[i][3], i, u=imported[i][4])
			self.Map.append(new_hex)
			print self.Map[i].Map_index
		for i in self.Map:
			x = 0
			if i.terrain=="City" or i.terrain=="Factory" or i.terrain=="Capitol":
				i.hp = 10
			for j in self.Map:
				if round(i.vertex[0]) == round(j.vertex[0]) and round(i.vertex[1]) == round(j.vertex[1] + height):
					i.up_neighbor = j
					x += 1
					print i.up_neighbor
				elif round(i.vertex[0]) == round(j.vertex[0] + width) and round(i.vertex[1]) == round(j.vertex[1] + height/2):
					i.upleft_neighbor = j
					x += 1
				elif round(i.vertex[0]) == round(j.vertex[0] + width) and round(i.vertex[1]) == round(j.vertex[1] - height/2):
					i.downleft_neighbor = j
					x += 1
				elif round(i.vertex[0]) == round(j.vertex[0]) and round(i.vertex[1]) == round(j.vertex[1] - height):
					i.down_neighbor = j
					x += 1
				elif round(i.vertex[0]) == round(j.vertex[0] - width) and round(i.vertex[1]) == round(j.vertex[1] - height/2):
					i.downright_neighbor = j
					x += 1
				elif round(i.vertex[0]) == round(j.vertex[0] - width) and round(i.vertex[1]) == round(j.vertex[1] + height/2):
					i.upright_neighbor = j
					x += 1
			print x

	def __init__(self):
		self.numberofplayers = [0,1]
		self.playermoney=[1000]*len(self.numberofplayers)
		self.player_buildings = [1,1]
		self.current_player = 0
		self.current_turn = 1
		global frame
		frame = Tkinter.Frame(width=1000, height=700, background="Purple")
		frame.pack()
		self.leftwidgets()
		global canvas
		canvas = Tkinter.Canvas(frame, width=700, height=700, background="black")
		canvas.place(x=100,y=0)
		self.rightwidgets()
		global text
		text = Tkinter.Text(frame, width=23, height=30, wrap="word")
		text.place(x=1000, y=600, anchor="se")
		self.Map = []
		self.import_map(imported)
		self.cursor = self.Map[0]
#		x = self.Map[0].vertex[0]
#		y = self.Map[0].vertex[1]
#		hex_side = 30
#		canvas.create_polygon([[x, y], [x+hex_side*.5, y+hex_side*.866], [x+hex_side*.5+hex_side, y+hex_side*.866], [x+2*hex_side, y], [x+hex_side*.5+hex_side, y-hex_side*.866], [x+hex_side*.5, y-hex_side*.866]], outline="red", fill=self.Map[0].color)
		self.cursor.draw_red_hex()
		frame.mainloop()

class LightInf:
	def __init__(self, controller):
		self.movement = 3
		self.attack = 1
		self.defense = 1
		self.movement_modifiers = {"Plains" : 0, "Woods" : 0, "Mountains":1, "Factory":.5, "Road":.5}
		self.attack_range = 1
		self.movement_left = 3
		self.controller = controller
		self.price = 100
		self.health = 10.0
		self.color = "White"
		self.name = "Light Infantry"
		self.captured = 0
		self.attacked = 0

class HeavyInf:
	def __init__(self, controller):
		self.movement = 2
		self.attack = 2
		self.defense = 2
		self.movement_modifiers = {"Plains" : 0, "Woods" : 0, "Mountains":1, "Factory":.5, "Road":.5}
		self.attack_range = 1
		self.movement_left = 2
		self.controller = controller
		self.price = 300
		self.health = 10.0
		self.color = "Black"
		self.name = "Heavy Infantry"
		self.captured = 0
		self.attacked = 0

class LightCav:
	def __init__(self, controller):
		self.movement = 6
		self.attack = 3
		self.defense = 1
		self.movement_modifiers = {"Plains" : 0, "Woods" : 1, "Mountains":None, "Factory":.5, "Road":.5}
		self.attack_range = 1
		self.movement_left = 6
		self.controller = controller
		self.price = 800
		self.health = 10.0
		self.color = "LightGrey"
		self.name = "Light Cavalry"
		self.attacked = 0

class HeavyCav:
	def __init__(self, controller):
		self.movement = 6
		self.attack = 3
		self.defense = 2
		self.movement_modifiers = {"Plains" : 0, "Woods" : 1, "Mountains":None, "Factory":.5, "Road":.5}
		self.attack_range = 1
		self.movement_left = 6
		self.controller = controller
		self.price = 700
		self.health = 10.0
		self.color = "DarkGrey"
		self.name = "Heavy Cavalry"
		self.attacked = 0
			
class Archers:
	def __init__(self, controller):
		self.movement = 4
		self.attack = 3
		self.defense = 1
		self.movement_modifiers = {"Plains" : 0, "Woods" : 0, "Mountains":1, "Factory":.5, "Road":.5}
		self.attack_range = 2
		self.movement_left = 3
		self.controller = controller
		self.price = 600
		self.health = 10.0
		self.color = "Red"
		self.name = "Archers"
		self.attacked = 0

class Hex:
	def __init__(self, x, y, z, T, i, u=None, hp=None):
		self.vertex = [x,y]
		self.color = z
		self.terrain = T
		self.draw_black_hex()
		self.unit = None
		self.upleft_neighbor = None
		self.up_neighbor = None
		self.upright_neighbor = None
		self.downright_neighbor = None
		self.down_neighbor = None
		self.downleft_neighbor = None
		self.Map_index = i
		self.controller = u
		self.hp = hp

	def draw_red_hex(self):
		hex_side = 30
		x = self.vertex[0]
		y = self.vertex[1]
		z = self.color
		canvas.create_polygon([[x, y], [x+hex_side*.5, y+hex_side*.866], [x+hex_side*.5+hex_side, y+hex_side*.866], [x+2*hex_side, y], [x+hex_side*.5+hex_side, y-hex_side*.866], [x+hex_side*.5, y-hex_side*.866]], outline="red", fill=z)

	def draw_black_hex(self):		
		hex_side = 30
		x = self.vertex[0]
		y = self.vertex[1]
		z = self.color
		canvas.create_polygon([[x, y], [x+hex_side*.5, y+hex_side*.866], [x+hex_side*.5+hex_side, y+hex_side*.866], [x+2*hex_side, y], [x+hex_side*.5+hex_side, y-hex_side*.866], [x+hex_side*.5, y-hex_side*.866]], outline="black", fill=z)

app = Application()

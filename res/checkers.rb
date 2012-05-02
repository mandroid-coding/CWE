#1. This program will let you:
#* have fun
#* play checkers
#More fun[www.addictinggames.com]


class Piece
	def initialize(color)
		@color = color
	end
	
	def show_color
		return @color
	end
end

class Square
	def initialize(x, y, board)
		@board = board
		@position  = [x,y]
		@adjacent_sqrs = Array.new
		@jump_sqrs = Array.new
	end
	
	##def find_adjacent
		##adjacent = [[1,1],[1,-1],[-1,1],[-1,-1]]
		##adjacent.each {|x|
		##if @board.get_position(x[0] += @position[0], x[1] += @position[1]) != nil
			##puts "getting position: " + "("+(x[0] += @position[0]).to_s+ ", " + (x[1] += @position[1]).to_s + ")"
			##puts "position: " + @board.get_position(x[0] += @position[0], x[1] += @position[1]).to_s
			##@adjacent_sqrs << @board.get_position(x[0] += @position[0], x[1] += @position[1])
		##end
		##}
		##jumps = [[2,2],[2,-2],[-2,2],[-2,-2]]
		##jumps.each {|x|
		##if @board.get_position(x[0] += @position[0], x[1] += @position[1]) != nil
			##@jump_sqrs << @board.get_position(x[0] += @position[0], x[1] += @position[1])
		##end
		##}
		###@adjacent_squares.each {|x|
		###x << @jump_sqrs.shift
		###}
	##end
	
	def adjacent_squares
		return @adjacent_squares
	end
	
	def jump_squares
		return @jump_sqrs
	end
	
	def to_s
		puts @position
	end
end

class BlackSquare < Square
	def initialize(x, y, board)
		super
		@current_peice = nil
	end
	
	def add_peice(piece)
		@current_piece = piece
	end
	
	def remove_piece(piece)
		@current_piece = nil
	end
end

class WhiteSquare < Square
	def initialize(x, y, board)
		super
	end
end
		
class Board
	def initialize
		@square_list = Array.new
		@board_state = nil 
		initiate_board
	end
	
	#This method prints a string representation of the board (that is saved 
	#under @board_state)
	def print_board
		if @board_state != nil
			puts @board_state
		else
			puts "There is no @board_state"
		end
	end
	
	#This method returns a square of the color and position specfied 
	#while also adding the square to the list new_square
	def CreateSquare(x, y, color)
		if color == "white"
			new_square = WhiteSquare.new(x, y, self)
		elsif color == "black"
			new_square = BlackSquare.new(x,y, self)
		end
		#puts new_square.methods.sort
		#puts new_square.class
		@square_list << new_square
		return new_square
	end

	#This method returns a list of 8 squares in an alternating pattern 
	#starting with first_color(black or white) and alternating with the 
	#second color (black or white but not first color.)
	def square_array_maker( x, first_color, second_color)
		return [0,2,4,6].map {|y| 
		self.CreateSquare(x, y, first_color)}.zip(
		[1,3,5,7].map {|y|
		self.CreateSquare(x, y, second_color)}
		).reduce([]) {|a,b| a + b }
	end
	
	#This method sets the instance variable @board_state equal to a list of lists 
	#of black and white squares that are arranged in a checker board pattern
	def initiate_board
		@board_state = Array.new(8) {|x| 
			if x % 2 == 0
				square_array_maker( x, "white", "black")
			else
				square_array_maker( x, "black", "white")
			end
			}
		##@board_state.each {|y|
			##y.each {|z|
				##z.find_adjacent
			##}
	end

	#This method returns the square on the board in the position specified
	def get_position(x,y)
		print "check"
		return @board_state[x][y]
	end
end

first = Board.new
print first.get_position(0,0)
##print first.get_position(2,3).adjacent_squares


import turtle


SQUARE = 50
TILE = 20
BOARD_COLOR = 'blue2'
LINE_COLOR = 'black'
TILE_COLORS = ['black', 'white']

class Board:

    def __init__(self, n):
       
        self.n = n
        self.board = [[0] * n for i in range(n)]
        self.square_size = SQUARE
        self.board_color = BOARD_COLOR
        self.line_color = LINE_COLOR
        self.tile_size = TILE
        self.tile_colors = TILE_COLORS
        self.move = ()

    def draw_board(self):
   
        turtle.setup(self.n * self.square_size + self.square_size, 
                    self.n * self.square_size + self.square_size)
        turtle.screensize(self.n * self.square_size, self.n * self.square_size)
        turtle.bgcolor('white')

       
        othello = turtle.Turtle(visible = False)
        othello.penup()
        othello.speed(0)
        othello.hideturtle()

       
        othello.color(self.line_color, self.board_color)
        
      
        corner = -self.n * self.square_size / 2
        othello.setposition(corner, corner)
        
       
        othello.begin_fill()
        for i in range(4):
            othello.pendown()
            othello.forward(self.square_size * self.n)
            othello.left(90)
        othello.end_fill()
        
      
        for i in range(self.n + 1):
            othello.setposition(corner, self.square_size * i + corner)
            self.draw_lines(othello)
        
       
        othello.left(90)
        for i in range(self.n + 1):
            othello.setposition(self.square_size * i + corner, corner)
            self.draw_lines(othello)

    def draw_lines(self, turt):
      
        turt.pendown()
        turt.forward(self.square_size * self.n)
        turt.penup()

    def is_on_board(self, x, y):
       
        bound = self.n / 2 * self.square_size
        
        if - bound < x < bound and - bound < y < bound:
            return True
        return False

    def is_on_line(self, x, y):
     
        if self.is_on_board(x, y):   
            if x % self.square_size == 0 or y % self.square_size == 0:
                return True
        return False

    def convert_coord(self, x, y):
        
        if self.is_on_board(x, y):
            row = int(self.n / 2 - 1 - y // self.square_size)
            col = int(self.n / 2 + x // self.square_size)
            return (row, col)
        return ()

    def get_coord(self, x, y):
        
        if self.is_on_board(x, y) and not self.is_on_line(x, y):
            self.move = self.convert_coord(x, y)
        else:
            self.move = ()

    def get_tile_start_pos(self, square):
       
        if square == ():
            return ()
        
        for i in range(2):
            if square[i] not in range(self.n):
                return ()

        row, col = square[0], square[1]

        y = ((self.n - 1) / 2 - row) * self.square_size
        if col < self.n / 2:
            x = (col - (self.n - 1) / 2) * self.square_size - self.tile_size
            r = - self.tile_size
        else:
            x = (col - (self.n - 1) / 2) * self.square_size + self.tile_size
            r = self.tile_size
        
        return ((x, y), r)

    def draw_tile(self, square, color):
        
        pos = self.get_tile_start_pos(square)
        if pos:
            coord = pos[0]
            r = pos[1]
        else:
            print('Error drawing the tile...')
            return
        
       
        tile = turtle.Turtle(visible = False)
        tile.penup()
        tile.speed(0)
        tile.hideturtle()

      
        tile.color(self.tile_colors[color])

    
        tile.setposition(coord)
        tile.setheading(90)
        
       
        tile.begin_fill()
        tile.pendown()
        tile.circle(r)
        tile.end_fill()

    def __str__(self):
       
        explanation = 'State of the board:\n'
        board_str = ''
        for row in self.board:
            board_str += str(row) + '\n' 
        printable_str = explanation + board_str

        return printable_str

    def __eq__(self, other):
      
        return self.board == other.board

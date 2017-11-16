import game
from tkinter import *

def draw_sqare(canvas, width, margin,col, row,number):
    ''' this function will take in 4 arguments:
        1. the canvas on which the square will be drawn
        the color of the square (which will be both the
        fill color and the outline color)
        2. the width and height of the square
        (in pixels); these are obviously the same since it's a square
        3. the position of the center of the square,
        represented as a tuple of two integers representing
        4. the horizontal and vertical position of the center in pixels

    and will draw a square with those specificaitons and return a
    handle to that object
    '''
    colors = {'0':'#CDC1B5',
              '2':'#EEE4DA',
              '4':'#EDE0C7',
              '8':'#f78e48',
              '16':'#fc5e2e',
              '32':'#ff3333',
              '64':'#ff0000',
              '128':'#75a7f1',
              '256':'#4585f2',
              '512':'#edcf72',
              '1024':'#edc53f'}
    color = colors.get(number,'#CDC1B5')
    if int(number) > 1024:
        color = '#BCAFA1'
    if int(number) == 0:
        number =''
    
    xpos = row
    ypos = col
    centerx = (margin + width) * (xpos + 1) - width / 2
    centery = (margin + width) * (ypos + 1) - width / 2
    print(str(row) + str(col))
    x1center = centerx - width / 2
    y1center = centery - width / 2
    x2center = centerx + width / 2
    y2center = centery + width / 2
    
    return canvas.create_rectangle((x1center), (y1center),
                                (x2center), (y2center),
                                fill = color, outline = color),\
                                 canvas.create_text(
                                    centerx,centery,text = str(number), 
                                    fill = '#808080',font=("Purisa", 
                                    int(width * .2)))

def displayGFKs(board,cell_size,padding,canvas):
    '''thus function takes in a board - python dictionary,
	the size specified by each cell, padding - size of the padding, 
	and a canvas object on which the tiles of game will be drawn'''
    for row in range(4):
        for col in range(4):
            
            num = board.get((row, col), 0)
            print(num)
            draw_sqare(canvas,cell_size,padding,row,col, str(num))

def updateimage(board,key,c,dim):
    '''this function takes in a board, a key press character,
	a canvas object where the image will be updated on, and a dimension value
	dim for the size of the canvas'''
    if not game.game_over(board):
        game.update(board, key)
        c.delete('all')
        c.create_rectangle(0, 0, dim, dim, fill='#BCAFA1', outline='#BCAFA1')
        displayGFKs(board,cell_size,padding,c)
    
def updatefirsttime(board,c,dim):
    '''this function takes in a board, a canvas object, and a dimension value 
	to refresh the game screen for the first time '''
    c.create_rectangle(0, 0, dim, dim, fill='#BCAFA1', outline='#BCAFA1')
    displayGFKs(board,cell_size,padding,c)

def quitgame(myroot):
    '''this function quits the game on key press'''
    root.destroy()

    

def clear(b):
    '''this function clears the board,
	however it currently does not work, this will
	be fixed in the beta'''
    b = game.make_board()

if __name__ == '__main__':
    '''main function to run the game'''
    cell_size = 100
    padding = 5
    dim = padding * 5 + 4 * cell_size
    root = Tk()
    root.geometry(str(dim)+'x'+str(dim))
    c = Canvas(root,width = dim, height = dim)
    c.pack()
    c.create_rectangle(0, 0, dim, dim, fill='#BCAFA1', outline='#BCAFA1')
    b = game.make_board()
       
    root.bind('<w>', lambda event: updateimage(b,'w',c,dim))
    root.bind('<a>', lambda event: updateimage(b,'a',c,dim))
    root.bind('<s>', lambda event: updateimage(b,'s',c,dim))
    root.bind('<d>', lambda event: updateimage(b,'d',c,dim))
    root.bind('<g>', lambda event: updatefirsttime(b,c,dim))
    root.bind('<r>', lambda event: clear(b))

    root.bind('<q>', quitgame)
    c.create_text(int(dim/2),int(dim/4),text = "2048", 
                                    fill = '#808080',font=("Purisa", 
                                    int(dim/10)))
    c.create_text(int(dim/2),int(dim/2),text =
     "by HSQ8 \n \n\'g\' to start \n\'q\' to quit \
     \n\'w\',\'a\',\'s\',\'d\' to move around", 
                                    fill = '#808080',font=("Purisa", 
                                    int(dim/20)))
        
    while True:
        if game.game_over(b):
            c.delete('all')
            c.create_rectangle(0, 0, dim, dim, fill='#BCAFA1',\
             outline='#BCAFA1')
            c.create_text(int(dim/2),int(dim/2),\
            text = "game over\n \'q\' to quit ", 
                                    fill = '#808080',font=("Purisa", 
                                    int(dim/20)))
        root.update()
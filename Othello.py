# Updated Animation Starter Code
import math
import random
from tkinter import *
import copy
import time
####################################
# Here is the beginning of the Othello code
####################################

class Box(object):
    #Model
    def __init__(self,x,y,color,row,col):
        self.x = x
        self.y = y
        self.color = color
        self.hasPiece = False
        self.pieceColor = None
        self.row = row
        self.col = col

        # deal moves and flipp

        self.possibleMove = False
        self.willFlip = False
        self.numberOfFlippingPieces = 0
        self.piecesToFlip = []

    def setRadius(self,radius):
        self.radius = radius
        self.innerRadius = self.radius*80/100

        return self.radius, self.innerRadius




    def flipPiece(self,true = False, d = None):

        for piece in self.piecesToFlip:

            count = 0
            if true == True: #this is suppose to animate pieces but not ones in the minimax
                count = 0

                radius = piece.radius
                innerRadius = piece.innerRadius
                while piece.radius > 1:


                    if piece.innerRadius < 2:
                        piece.innerRadius = 1

                    for i in range(int(radius)):
                        time.sleep(0.001)
                        piece.radius -= 1

                if piece.pieceColor == 'black':
                    piece.pieceColor = 'white'
                elif piece.pieceColor == 'white':
                    piece.pieceColor = 'black'

                while piece.radius < radius:
                    for i in range(int(radius)):
                        time.sleep(0.01)
                        piece.radius += 1

            else:
                if piece.pieceColor == 'black':
                    piece.pieceColor = 'white'
                elif piece.pieceColor == 'white':
                    piece.pieceColor = 'black'
        self.piecesToFlip = []


    def contains(self,radius,x,y):
        return ((self.x - x)**2 + (self.y - y)**2)**0.5 < radius







    #View

    def drawBox(self,canvas,data):
        canvas.create_rectangle(self.x-data.side/2, self.y-data.side/2, self.x+data.side/2, self.y+data.side/2, fill = self.color, outline = 'paleTurquoise')
        canvas.create_rectangle(self.x-data.side/2.3, self.y-data.side/2.3, self.x+data.side/2.3, self.y+data.side/2.3, fill = 'grey', outline =self.color ,stipple="gray25")



#TODO: Time for making the piece looking good #### double pieces would look awesome I guess
    def drawPiece(self,canvas,data):

        if self.hasPiece:
            radius,innerRadius = self.setRadius(data.side/2)

            if self.pieceColor == 'black':
                canvas.create_oval(self.x-radius, self.y-data.side/2, self.x+radius, self.y+data.side/2, fill =  self.pieceColor, outline = '#110F0F')
                canvas.create_oval(self.x- innerRadius, self.y-innerRadius, self.x+ innerRadius, self.y+ innerRadius, fill = '#110F0F' , outline = 'black')
            else:
                canvas.create_oval(self.x-radius, self.y-radius, self.x+radius, self.y+radius, fill = self.pieceColor, outline = '#F9FAFA')
                canvas.create_oval(self.x-innerRadius, self.y-innerRadius, self.x+innerRadius, self.y+innerRadius, fill = '#F9FAFA', outline = 'white')




    def drawPossibleMove(self,canvas,data):

        canvas.create_oval(self.x-data.side/2, self.y-data.side/2, self.x+data.side/2, self.y+data.side/2, fill = None, outline = 'darkCyan')
        canvas.create_text(self.x,self.y, text = '+' + str(self.numberOfFlippingPieces))



    def checkTheEndOfTheLine(self,board,nextPieceColor,a,b, moves=[(0,-1),(-1,-1),(-1,0),(1,-1),(0,1),(1,1),(1,0),(-1,1)],flippingpieces=0):
        numberOfRow = len(board)
        i = a
        j = b
        board[a][b].numberOfFlippingPieces = 0
        for move in moves:
            count = 0
            flippingPieces = []
            while i+move[0] < numberOfRow and i >= 0 and j >= 0 and j+move[1] < numberOfRow and board[i+move[0]][j+move[1]].hasPiece:

                i += move[0]
                j += move[1]

                if board[i][j].pieceColor != nextPieceColor and board[i][j].pieceColor != None:
                    count += 1
                    flippingPieces += [board[i][j]]
                    if i+move[0] >= numberOfRow or j+move[1] >= numberOfRow or i+move[0] < 0 or j+move[1] < 0  or board[i+move[0]][j+move[1]].pieceColor == None:
                        flippingPieces =[]
                        count = 0

                        break
                elif board[i][j].pieceColor == nextPieceColor and count > 0:
                    #append the piece in flipping pieces
                    board[a][b].willFlip = True
                    count = 0
                    for piece in flippingPieces:
                        if not piece in board[a][b].piecesToFlip:
                            board[a][b].piecesToFlip += [piece]


                    break
                elif board[i][j].pieceColor == nextPieceColor and count == 0:

                    break





            i = a
            j = b
            board[i][j].numberOfFlippingPieces = len(board[a][b].piecesToFlip) + 1

        return board[i][j].willFlip

def resetBoard(arguments):
    pass



def init(data):
    # load data.xyz as appropriate
    data.home = True
    data.board = []
    data.nextPieceColor = 'black'
    data.pVSc = False
    data.pVSp = False
    data.pVSpColor = 'mediumAquamarine'
    data.pVScColor = 'mediumAquamarine'
    data.level = 'Middle'
    data.numberOfRow = 8
    data.side = 60
    gridWidth = data.side*2*data.numberOfRow
    gridHeight = data.side*2*data.numberOfRow
    data.marginX = 300
    data.marginY = 100
    data.count =0


    #levels
    data.level = 'high'
    data.lowLevelColor = 'black'
    data.middleLevelColor = 'white'
    data.highLevelColor = 'black'
    data.lowLevelBoxColor = None
    data.middleLevelBoxColor = None
    data.highLevelBoxColor = None
    data.lowLevelFont = "Times 12 bold"
    data.middleLevelFont = "Times 12 bold underline"
    data.highLevelFont = "Times 12 bold"

    data.playButtonColor = 'black'
    data.radius = data.side/2

    data.validMoves = []
    data.otherPieceColor = None
    data.theWoulHavePiecesToFlip = []

    #MINIMAX
    data.minimax = False

#######################CREATING  A BOARD ################################################################


    data.board += [[] for i in range(data.numberOfRow)]
    for row in range(len(data.board)):
        data.board[row]+= [[] for col in range(data.numberOfRow)]

    nextColor = 'mediumAquamarine'

    for row in range(len(data.board)):
        if nextColor == 'lightSteelBlue':
            nextColor = 'mediumAquamarine'
        else:
            nextColor = 'lightSteelBlue'
        for col in range(len(data.board[row])):
            if nextColor == 'lightSteelBlue':
                nextColor = 'mediumAquamarine'
            else:
                nextColor = 'lightSteelBlue'
            data.board[row][col] = Box(data.marginX+ data.side*row, data.marginY+data.side*col  ,nextColor,row,col)


    count = 0
    fourPieces = [] # This is for four pieces that will start in the middle of the board
    for row in range(len(data.board)): #27 36 35  28
        for piece in range(len(data.board[row])):

            if count in (27,36,35,28):

                # data.pieces.append(data.board[piece])
                data.board[row][piece].hasPiece = True
                fourPieces.append(data.board[row][piece])

            count += 1
    fourPieces[0].pieceColor,data.nextPieceColor = getColor(fourPieces[0].pieceColor,fourPieces[0], data.nextPieceColor)
    fourPieces[2].pieceColor,data.nextPieceColor = getColor(fourPieces[2].pieceColor,fourPieces[2], data.nextPieceColor)
    fourPieces[3].pieceColor,data.nextPieceColor = getColor(fourPieces[3].pieceColor,fourPieces[3], data.nextPieceColor)
    fourPieces[1].pieceColor,data.nextPieceColor = getColor(fourPieces[1].pieceColor,fourPieces[1], data.nextPieceColor)
    data.nextPieceColor,data.blacks, data.whites,data.board,data.validMoves = validMove(data.board,data.nextPieceColor)

##########################################################################################################
#Fixme: need to remove "data" in arguments. ===========Probably==========
def drawHomeScreen(canvas,data):
    homePieces = [[[],[]],[[],[]]]
    size = 64
    for row in range(2):
        for col in range(2):
            if row == col:
                color = 'black'
            else:
                color = 'white'
            canvas.create_oval((data.width//5)+(row*size)-30,(data.height//7)+(col*size) -30,(data.width//5)+(row*size)+30,(data.height//7)+(col*size) +30, fill = color, outline= 'black' if color == 'white' else 'white', width = 2 )

    canvas.create_text(data.width//2,data.height//5, text = 'Othello', font = "Times 80 bold italic")
    canvas.create_text(data.width//2+5,data.height//5+5, text = 'Othello', fill = 'white',font = "Times 80 bold italic")
    canvas.create_text(data.width//2,data.height/3+10, text = 'Choose the Playing Mode', fill = 'white',font = "Times 30 bold underline")

    # Choosing a player
    canvas.create_rectangle((data.width//5)-150,(data.height//2) -30,(data.width//5)+150,(data.height//2)+30, fill = data.pVSpColor, outline= 'black' , width = 2 )
    canvas.create_text((data.width//5),(data.height//2),text = 'Player 1 VS Player 2',fill = data.nextPieceColor ,font = "Times 15 bold italic")

    canvas.create_rectangle(data.width -(data.width//5)-150,(data.height//2) -30,(data.width -data.width//5)+150,(data.height//2)+30, fill = data.pVScColor, outline= 'black' , width = 2 )

    canvas.create_text((data.width -data.width//5),(data.height//2),text = 'Player VS Computer',fill = data.nextPieceColor ,font = "Times 15 bold italic")

    if data.pVSp == True:
        canvas.create_oval(data.width//2 -data.side, data.height -
data.height//3-data.side, data.width//2 + data.side, data.height -data.height//3 + data.side, fill = None, outline = 'black', width = 5)
        canvas.create_polygon(data.width//2 -data.radius+10,data.height -
data.height//3-data.radius, data.width//2 +10+ data.radius,data.height -
data.height//3,data.width//2+10 -data.radius,data.height -
data.height//3+data.radius, fill = 'black' )
    elif data.pVSc == True:
        #low level
        canvas.create_rectangle(data.width -(data.width//5)-150,(data.height//2) -15+ data.height/10,(data.width -data.width//5)+150,(data.height//2)+20+data.height/10, fill = data.lowLevelBoxColor, outline= 'black' , width = 2 )
        canvas.create_text((data.width -data.width//5),(data.height//2)+data.height/10 , text= 'low level',fill = data.lowLevelColor, font = (data.lowLevelFont)  )

        # medium level
        canvas.create_rectangle(data.width -(data.width//5)-150,(data.height//2) -15+(data.height/10)*2,(data.width -data.width//5)+150,(data.height//2)+20+(data.height/10)*2, fill = data.middleLevelBoxColor, outline= 'black' , width = 2 )
        canvas.create_text((data.width -data.width//5),(data.height//2)+(data.height/10)*2 , text= 'Middle level',fill = data.middleLevelColor, font = (data.middleLevelFont)  )

        #high level
        canvas.create_rectangle(data.width -(data.width//5)-150,(data.height//2) -15 +data.height/10*3,(data.width -data.width//5)+150,(data.height//2)+20+data.height/10*3, fill = data.highLevelBoxColor, outline= 'black' , width = 2 )
        canvas.create_text((data.width -data.width//5),(data.height//2)+data.height/10*3, text= 'High level',fill = data.highLevelColor, font = (data.highLevelFont)  )
    if data.pVSc == True or data.pVSp == True:
        # Plya button
        canvas.create_oval(data.width//2 -data.side, data.height -
data.height//3-data.side, data.width//2 + data.side, data.height -data.height//3 + data.side, fill = None, outline = data.playButtonColor, width = 5)
        canvas.create_polygon(data.width//2 -data.radius+10,data.height -
data.height//3-data.radius, data.width//2 +10+ data.radius,data.height -
data.height//3,data.width//2+10 -data.radius,data.height -
data.height//3+data.radius, fill = data.playButtonColor )





def getColor(pieceColor,piece,nextPieceColor):
    pieceColor = nextPieceColor
    # Change color of the next piece
    if nextPieceColor == 'black':
        nextPieceColor = 'white'
    else: nextPieceColor = 'black'
    return pieceColor,nextPieceColor

def win(data):

    pass


def validMove(board,nextPieceColor):
    validMoves = None
    if validMoves == None:
        validMoves = []
    numberOfRow = len(board)
    whites = 0
    blacks = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col].pieceColor != nextPieceColor and board[row][col].pieceColor != None:

                for piece in [(0,-1),(-1,-1),(-1,0),(1,-1),(0,1),(1,1),(1,0),(-1,1)]:
                    if  row+piece[0] >= 0 and col+piece[1] >= 0 and row+piece[0] < numberOfRow and col+piece[1] < numberOfRow :

                        if  not board[row+piece[0]][col+piece[1]].hasPiece and board[row+piece[0]][col+piece[1]].checkTheEndOfTheLine(board,nextPieceColor,row+piece[0],col+piece[1]):
                            board[row+piece[0]][col+piece[1]].possibleMove = True

                            validMoves.append(board[row+piece[0]][col+piece[1]])
                        #the following doesn't seem to help anything
                        else:
                            board[row+piece[0]][col+piece[1]].piecesToFlip =[]




    for row in board:
        for col in row:
            if col.pieceColor == 'black':
                blacks += 1
            elif col.pieceColor == 'white':
                whites += 1

    return nextPieceColor,blacks, whites, board, validMoves

def noValidMoveForAll(board):
    newBoard = copy.deepcopy(board)
    movesForBlack = None
    movesForWhite = None
    _,_,_,_,movesForWhite = validMove(newBoard,'white')
    _,_,_,_,movesForBlack = validMove(newBoard,'black')
    if len(movesForWhite) == 0 and len(movesForBlack) == 0:
        return True
    return False



def randomMove(board,level,validMoves,nextPieceColor):#board,level, valideMoves, nextPieceColor
    numberOfRow = len(board)
    if level == 'low':
        if len(validMoves) != 0:
            piece = random.choice(validMoves)
            piece.hasPiece = True
            piece.pieceColor, nextPieceColor = getColor(piece.pieceColor,piece,nextPieceColor)
            piece.flipPiece()
    elif level == 'middle':
        if len(validMoves) !=0:
            for piece in ((0,0),(numberOfRow-1, numberOfRow-1),(numberOfRow-1,0),(0,numberOfRow-1)):
                i,j = piece
                if board[i][j] in validMoves:
                    board[i][j].hasPiece = True
                    board[i][j].pieceColor, nextPieceColor =getColor(board[i][j].pieceColor,board[i][j],nextPieceColor)
                    board[i][j].flipPiece()
                    return board
            for piece in validMoves:
                for i in range(0,numberOfRow):
                    for j in range(0,numberOfRow):
                        if (i == 0 or i == numberOfRow-1 or j == 0 or j == numberOfRow-1) and board[i][j] == piece:
                            piece.hasPiece = True
                            piece.pieceColor, nextPieceColor =getColor(piece.pieceColor,piece,nextPieceColor)
                            piece.flipPiece()
                            return board
            if not piece.hasPiece:
                piece = random.choice(validMoves)
                piece.hasPiece = True
                piece.pieceColor,nextPieceColor = getColor(piece.pieceColor,piece,nextPieceColor)
                piece.flipPiece()

    #TODO: TIME FOR MINIMAX YAY!!!!!!!
    else:
        _,piece = minimax(board, 3,True)
        print(piece.row, piece.col)
        piece = board[piece.row][piece.col]

        piece.hasPiece = True
        piece.pieceColor, nextPieceColor = getColor(piece.pieceColor,piece,nextPieceColor)
        piece.flipPiece()

    return board

def resetValidMoves(board,validMoves):

    for row in range(len(board)):
        for col in range(len(board[row])):
            board[row][col].willFlip = False
            board[row][col].possibleMove = False
            board[row][col].piecesToFlip=[]

    validMoves.clear()
    return board,validMoves

####
####Minimax
def evaluation(board):
    cornerScore = 10
    edgeScore = 8
    centerScore = 2
    result = 0
    for row in range(len(board)):
        for col in range(row):
            piece = board[row][col]
            if piece.hasPiece and  piece in (board[0][0],board[7][7], board[7][0], board[0][7]):
                if piece.pieceColor == 'white':
                    result += cornerScore
                else:
                    result -= cornerScore
            elif piece.hasPiece and (row == 0 or row == 7 or col == 0 or col == 7):
                if piece.pieceColor == 'white':
                    result += edgeScore
                else:
                    result -= edgeScore
            else:
                if piece.pieceColor == 'white':
                    result += centerScore
                else:
                    result -= centerScore
    return result

#return the best move for a player whose turn it is
def nextMoves(board,maximizingPlayer):
    if maximizingPlayer == True:
        nextPieceColor = 'white'
    else:
        nextPieceColor = 'black'
    validMoves = []
    _,_,_,_,validMoves = validMove(board,nextPieceColor)


    return validMoves



def createANewBoard(board,move, maximizingPlayer): # for minimax

    if maximizingPlayer == True:
        nextPieceColor = 'white'
    else:
        nextPieceColor = 'black'
    valideMoves = []
    _,_,_,newBoard,_ = validMove(board,nextPieceColor)
    return copy.deepcopy(newBoard)

def minimax(board, levelsLeft,maximizingPlayer):

    if levelsLeft  == 0 or gameOver(board):
        return evaluation(board),None


    if maximizingPlayer: #white player
        maxEval = -math.inf
        theBestMove = None
        for move in nextMoves(board,maximizingPlayer):

            newBoard = createANewBoard(board, move, maximizingPlayer)
            eval,_ = minimax(newBoard, levelsLeft - 1,False)
            if eval > maxEval:
                maxEval = eval
                theBestMove = move
        return  maxEval,theBestMove
    else:
        minEval = +math.inf
        theBestMove = None
        for move in nextMoves(board,maximizingPlayer):
            newBoard = createANewBoard(board, move, maximizingPlayer)
            eval,_ = minimax(newBoard, levelsLeft - 1,  True)
            if eval < minEval:
                theBestMove = move
                minEval = eval
        return minEval,theBestMove






def mousePressed(event, data):
    # use event.x and event.y
    #needs a condition
    if data.home == False: #during the play
        if data.pVSp == True:
            for row in data.board:
                for col in row:
                    if col.contains(data.radius,event.x,event.y) and col.hasPiece == False and col.possibleMove == True:
                        col.hasPiece = True
                        col.pieceColor,data.nextPieceColor = getColor(col.pieceColor,col, data.nextPieceColor)
                        print(row.index(col)+1,data.board.index(row)+1)
                        col.setRadius(data.side/2)
                        col.flipPiece(True)



            data.board,data.validMoves =resetValidMoves(data.board,data.validMoves)
            data.nextPieceColor,data.blacks, data.whites,data.board, data.validMoves = validMove(data.board,data.nextPieceColor)
            if len(data.validMoves) == 0 and data.blacks + data.whites <64:
                if data.nextPieceColor == 'black':
                    data.nextPieceColor = 'white'
                else: data.nextPieceColor = 'black'
                data.nextPieceColor,data.blacks, data.whites,data.board, data.validMoves = validMove(data.board,data.nextPieceColor)


        elif data.pVSc == True:
            if data.nextPieceColor == 'black':
                for row in data.board:
                    for col in row:
                        if col.contains(data.radius,event.x,event.y) and col.hasPiece == False and col.possibleMove == True:
                            col.hasPiece = True
                            col.pieceColor,data.nextPieceColor = getColor(col.pieceColor,col,data.nextPieceColor)
                            print(row.index(col)+1,data.board.index(row)+1)
                            col.setRadius(data.side/2)
                            col.flipPiece(True)




            data.board,data.validMoves = resetValidMoves(data.board,data.validMoves)
            data.nextPieceColor,data.blacks, data.whites,data.board, data.validMoves = validMove(data.board,data.nextPieceColor)
            if len(data.validMoves) == 0 and data.blacks + data.whites <64:
                if data.nextPieceColor == 'black':
                    data.nextPieceColor = 'white'
                else: data.nextPieceColor = 'black'
                data.nextPieceColor,data.blacks, data.whites,data.board, data.validMoves = validMove(data.board,data.nextPieceColor)


#fixme: After I change "or" instead of "and", there is a problem, a player mode can be updated during the game
##### IT SEEMS TO BE WORKING NOW THOUGH

    if (data.pVSc == False or data.pVSp == False) and data.home == True: # this is to avoid to be placed during the game
        if event.x >= 50 and event.x <= 350 and event.y>= 270 and event.y <= 330:
            data.pVSc = False
            data.pVSp = True


        elif event.x >= 650 and event.x <= 950 and event.y>= 270 and event.y <= 330:
            data.pVSc = True
            data.pVSp = False

    # Play button pressed
    if (data.pVSc==True or data.pVSp == True) and event.x >= data.width//2 -data.side  and event.y >= data.height - data.height//3-data.side  and data.width//2 + data.side >= event.x and data.height -data.height//3 + data.side >= event.y and data.home == True:
        data.home = False

    if data.home == True:
        #low level Button
        if (data.width -(data.width//5)-150) <= event.x and ((data.height//2) -15+ data.height/10) <= event.y and ((data.width -data.width//5)+150) >= event.x and ((data.height//2)+20+data.height/10) >= event.y :
            data.level = 'low'
            data.lowLevelColor = 'white'
            data.lowLevelFont = "Times 12 bold underline"
            data.highLevelColor = 'black'
            data.highLevelFont = "Times 12 bold"
            data.middleLevelColor = 'black'
            data.middleLevelFont = "Times 12 bold"


        # medium level
        elif(data.width -(data.width//5)-150) <= event.x and ((data.height//2) -15+ data.height/10*2) <= event.y and ((data.width -data.width//5)+150) >= event.x and ((data.height//2)+20+data.height/10*2) >= event.y:
            data.level = 'middle'
            data.middleLevelColor = 'white'
            data.middleLevelFont = "Times 12 bold underline"
            data.lowLevelColor = 'black'
            data.lowLevelFont = "Times 12 bold"
            data.highLevelColor = 'black'
            data.highLevelFont = "Times 12 bold"



        #high level
        elif(data.width -(data.width//5)-150) <= event.x and ((data.height//2) -15+ data.height/10*3) <= event.y and ((data.width -data.width//5)+150) >= event.x and ((data.height//2)+20+data.height/10*3) >= event.y:
            data.level = 'high'
            data.highLevelColor = 'white'
            data.highLevelFont = "Times 12 bold underline"
            data.lowLevelColor = 'black'
            data.lowLevelFont = "Times 12 bold"
            data.middleLevelColor = 'black'
            data.middleLevelFont = "Times 12"



    print(event.x,event.y)
def mouseMoved(event,data):

    # # use event.x and event.y
    if data.home == True:
        if event.x >= 50 and event.x <= 350 and event.y>= 270 and event.y <= 330:
            data.pVSpColor = 'lightblue'
        else: data.pVSpColor = 'mediumAquamarine'
        if event.x >= 650 and event.x <= 950 and event.y>= 270 and event.y <= 330:
            data.pVScColor = 'lightblue'
        else: data.pVScColor = 'mediumAquamarine'

#fixme: kfsdjlsa;fjk;asdljfl;afjsasd

        #Easy level
        if (data.width -(data.width//5)-150) <= event.x and ((data.height//2) -15+ data.height/10) <= event.y and ((data.width -data.width//5)+150) >= event.x and ((data.height//2)+20+data.height/10) >= event.y :
            data.lowLevelBoxColor = 'lightSteelBlue'
        else:
            data.lowLevelBoxColor = None

        # Normal level
        if(data.width -(data.width//5)-150) <= event.x and ((data.height//2) -15+ data.height/10*2) <= event.y and ((data.width -data.width//5)+150) >= event.x and ((data.height//2)+20+data.height/10*2) >= event.y:
            data.middleLevelBoxColor = 'lightSteelBlue'
        else:
            data.middleLevelBoxColor = None


        # Classic level




        #high level
        if(data.width -(data.width//5)-150) <= event.x and ((data.height//2) -15+ data.height/10*3) <= event.y and ((data.width -data.width//5)+150) >= event.x and ((data.height//2)+20+data.height/10*3) >= event.y:
            data.highLevelBoxColor = 'lightSteelBlue'
        else:
            data.highLevelBoxColor = None

        # when hovered play Button
        if data.pVSc == True or data.pVSp == True:
            if  ((data.width//2 - event.x)**2 + ((data.height -data.height//3) - event.y)**2)**0.5 < data.side :
                data.playButtonColor= 'lightSteelBlue'
            else:
                data.playButtonColor= 'black'

    pass

def keyPressed(event, data):
    # use event.char and event.keysym

    print
    pass
def go(data):
    data.count += 1
    if data.count%10 == 0:
        return
def timerFired(data):
    data.count += 1


    if data.pVSc == True:  #and data.count %10 == 0:
        if data.nextPieceColor == 'white':
            data.board = randomMove(data.board,data.level,data.validMoves,data.nextPieceColor)
            data.nextPieceColor = 'black'
        data.board,data.validMoves = resetValidMoves(data.board,data.validMoves)
        data.nextPieceColor,data.blacks, data.whites,data.board, data.validMoves = validMove(data.board,data.nextPieceColor)
    if len(data.validMoves) == 0 and data.blacks + data.whites <64:
        if data.nextPieceColor == 'black':
            data.nextPieceColor = 'white'
        else: data.nextPieceColor = 'black'
        data.nextPieceColor,data.blacks, data.whites,data.board, data.validMoves = validMove(data.board,data.nextPieceColor)



def gameOver(board):
    blacks = 0
    whites = 0
    for row in board:
        for piece in row:
            if piece.pieceColor == 'black':

                blacks += 1
            elif piece.pieceColor == 'white':

                whites += 1
    if blacks + whites == 64 or blacks == 0 or whites == 0 or noValidMoveForAll(board):
        if blacks == whites:
            return 'tie'
        win = max(blacks, whites)

        return 'black' if win == blacks else 'white'

    return None





def redrawAll(canvas, data):
    #
    #Open a home screen#######
    if data.home == True:
        drawHomeScreen(canvas,data)
    else:
        # if data.minimax == True:
        #     canvas.create_rectangle(data.width//2-80, data.height//2-80, data.width//2+80, data.height//2+80)
        # draw in canvas
        winner = gameOver(data.board)
        if winner != None:
            if not winner == 'tie':

                canvas.create_text(data.width//2, data.height/11, text = winner + ' won, Congratulations!' , fill = 'white', font=("Helvetica", 30))
            else:
                canvas.create_text(data.width//2, data.height/11, text = winner + ".Well done for both of you, It's a TIE" , fill = 'white', font=("Helvetica", 30))


        elif  winner == None:



            canvas.create_text(data.width//2, data.height/13, text=  data.nextPieceColor+"'s turn", font=("Helvetica", 30),fill= data.nextPieceColor)
        canvas.create_oval(data.width - data.width//6-data.side,data.height-data.height/6-data.side, data.width - data.width//6 + data.side,data.height-data.height/6 + data.side, fill = 'white')
        canvas.create_text(data.width - data.width//6,data.height-data.height/6 , text = data.whites, fill = 'black', font=("Helvetica", 30))

        canvas.create_oval(data.width//6-data.side,data.height-data.height/6-data.side, data.width//6 + data.side,data.height-data.height/6 + data.side, fill = 'black')
        canvas.create_text(data.width//6,data.height-data.height/6, text = data.blacks , fill = 'white', font=("Helvetica", 30))

        for row in data.board:
            for col in row:
                col.drawBox(canvas,data)
                col.drawPiece(canvas,data)
                if col.possibleMove == True:
                    col.drawPossibleMove(canvas,data)



####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='grey', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mouseMovedWrapper(event, canvas, data): # want to see if I can hover on a shape change a color
        mouseMoved(event,data)
        redrawAllWrapper(canvas,data)

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.title('Othello Game')
    root.resizable(width=True, height=True) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()

    # set up events
    root.bind("<Motion>", lambda event:
                            mouseMovedWrapper(event, canvas, data))

    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))

    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 600)

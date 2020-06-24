import pygame
pygame.init() # need to add other pawn promotion options and dots that show where to move

res = (800, 400)
win = pygame.display.set_mode(res)
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 30)

coolPic = pygame.image.load('Sprites/coolpic.png')
coolPicSmall = pygame.transform.scale(coolPic, (300, 300))
whiteSprites = [pygame.image.load('Sprites/w_p.png'), pygame.image.load('Sprites/w_r.png'), pygame.image.load('Sprites/w_b.png'), pygame.image.load('Sprites/w_n.png'), pygame.image.load('Sprites/w_k.png'), pygame.image.load('Sprites/w_q.png')]
blackSprites = [pygame.image.load('Sprites/b_p.png'), pygame.image.load('Sprites/b_r.png'), pygame.image.load('Sprites/b_b.png'), pygame.image.load('Sprites/b_n.png'), pygame.image.load('Sprites/b_k.png'), pygame.image.load('Sprites/b_q.png')]

class Board:
    def __init__(self, totalSize, lightColor, darkColor):
        self.totalSize = totalSize
        self.squareSize = totalSize // 8
        self.lightColor = lightColor
        self.darkColor = darkColor

    def draw(self):
        for row in range(8):
            for column in range(8):
                if (row + column) % 2 == 0:
                    pygame.draw.rect(win, self.lightColor, (column * self.squareSize, row * self.squareSize, self.squareSize, self.squareSize))
                else:
                    pygame.draw.rect(win, self.darkColor, (column * self.squareSize, row * self.squareSize, self.squareSize, self.squareSize))


board = Board(400, (118,150,86), (238,238,210))

class Piece:
    def __init__(self, teamColor):
        self.size = board.squareSize
        # self.font = pygame.font.Font('freesansbold.ttf', 55)
        self.teamColor = teamColor
        # if teamColor == 'w':
        #     self.teamColorrgb = (255, 255, 255)
        # else:
        #     self.teamColorrgb = (0, 0, 0)

    # def renderText(self, text):
    #     self.textSurface = self.font.render(text, True, self.teamColorrgb)

    def getPos(self):
        for row, rowPieces in enumerate(pieces):
            try:
                self.pos = (rowPieces.index(self), row)
            except:
                pass
        self.x = self.pos[0] * self.size
        self.y = self.pos[1] * self.size
        if type(self) is Pawn:
            if self.teamColor == 'w':
                if self.pos[1] == 0:
                    pieces[0][self.pos[0]] = Queen('w')
                    pieces[0][self.pos[0]].getPos()
            else:
                if self.pos[1] == 7:
                    pieces[7][self.pos[0]] = Queen('b')
                    pieces[7][self.pos[0]].getPos()

    def draw(self):
        win.blit(self.sprite, (self.x, self.y))


class Pawn(Piece):
    def __init__(self, teamColor):
        super().__init__(teamColor)
        # self.renderText('P')
        if self.teamColor == 'w':
            self.sprite = whiteSprites[0]
            self.name = 'P'
        else:
            self.sprite = blackSprites[0]
            self.name = 'p'
        self.isPassantable = False

    def testMoveSet(self, testx, testy):
        if self.teamColor == 'w':
            if self.pos[1] == 6:
                if (testy == 5 or testy == 4) and testx == self.pos[0] and pieces[testy][testx] == None and pieces[self.pos[1] - 1][self.pos[0]] == None:
                    if testy == 4:
                        self.isPassantable = True
                    return True
                elif pieces[testy][testx] != None:
                    if (testx - 1 == self.pos[0] or testx + 1 == self.pos[0]) and testy == 5:
                        return True
                return False
            else:
                if testy + 1 == self.pos[1] and testx == self.pos[0] and pieces[testy][testx] == None:
                    return True
                elif pieces[testy][testx] != None:
                    if (testx - 1 == self.pos[0] or testx + 1 == self.pos[0]) and testy + 1 == self.pos[1]:
                        return True
                elif self.pos[1] == 3 and type(pieces[3][testx]) is Pawn and testy == 2 and (testx == self.pos[0] + 1 or testx == self.pos[0] - 1):
                    if pieces[3][testx].isPassantable:
                        pieces[3][testx] = None
                        return True
                return False
        else:
            if self.pos[1] == 1:
                if (testy == 2 or testy == 3) and testx == self.pos[0] and pieces[testy][testx] == None and pieces[self.pos[1] + 1][self.pos[0]] == None:
                    if testy == 3:
                        self.isPassantable = True
                    return True
                elif pieces[testy][testx] != None:
                    if (testx - 1 == self.pos[0] or testx + 1 == self.pos[0]) and testy - 1 == 1:
                        return True
                return False
            else:
                if testy - 1 == self.pos[1] and testx == self.pos[0] and pieces[testy][testx] == None:
                    return True
                elif pieces[testy][testx] != None:
                    if (testx - 1 == self.pos[0] or testx + 1 == self.pos[0]) and testy - 1 == self.pos[1]:
                        return True
                elif self.pos[1] == 4 and type(pieces[4][testx]) is Pawn and testy == 5 and (testx == self.pos[0] + 1 or testx == self.pos[0] - 1):
                    if pieces[4][testx].isPassantable:
                        pieces[4][testx] = None
                        return True
                return False


class Rook(Piece):
    def __init__(self, teamColor):
        super().__init__(teamColor)
        # self.renderText('R')
        if self.teamColor == 'w':
            self.sprite = whiteSprites[1]
            self.name = 'R'
        else:
            self.sprite = blackSprites[1]
            self.name = 'r'
        self.notMoved = True
    
    def testMoveSet(self, testx, testy):
        rowDiff = abs(testy - self.pos[1])
        columnDiff = abs(testx - self.pos[0])
        if testy == self.pos[1]:
            for column in range(1, columnDiff):
                if testx > self.pos[0]:
                    if pieces[self.pos[1]][self.pos[0] + column] != None:
                        return False
                elif testx < self.pos[0]:
                    if pieces[self.pos[1]][self.pos[0] - column] != None:
                        return False
            self.notMoved = False
            return True
        elif testx == self.pos[0]:
            for row in range(1, rowDiff):
                if testy > self.pos[1]:
                    if pieces[self.pos[1] + row][self.pos[0]] != None:
                        return False
                elif testy < self.pos[1]:
                        if pieces[self.pos[1] - row][self.pos[0]] != None:
                            return False
            self.notMoved = False
            return True
        return False


class Bishop(Piece):
    def __init__(self, teamColor):
        super().__init__(teamColor)
        # self.renderText('B')
        if self.teamColor == 'w':
            self.sprite = whiteSprites[2]
            self.name = 'B'
        else:
            self.sprite = blackSprites[2]
            self.name = 'b'
    
    def testMoveSet(self, testx, testy):
        rowDiff = abs(testy - self.pos[1])
        columnDiff = abs(testx - self.pos[0])
        if rowDiff == columnDiff:
            for diagDiff in range(1, rowDiff):
                if testy > self.pos[1]:
                    if testx > self.pos[0]:
                        if pieces[self.pos[1] + diagDiff][self.pos[0] + diagDiff] != None:
                            return False
                    elif testx < self.pos[0]:
                        if pieces[self.pos[1] + diagDiff][self.pos[0] - diagDiff] != None:
                            return False
                elif testy < self.pos[1]:
                    if testx > self.pos[0]:
                        if pieces[self.pos[1] - diagDiff][self.pos[0] + diagDiff] != None:
                            return False
                    elif testx < self.pos[0]:
                        if pieces[self.pos[1] - diagDiff][self.pos[0] - diagDiff] != None:
                            return False
            return True
        return False


class Knight(Piece):
    def __init__(self, teamColor):
        super().__init__(teamColor)
        # self.renderText('N')
        if self.teamColor == 'w':
            self.sprite = whiteSprites[3]
            self.name = 'N'
        else:
            self.sprite = blackSprites[3]
            self.name = 'n'
    
    def testMoveSet(self, testx, testy):
        if testy + 1 == self.pos[1] or testy - 1 == self.pos[1]:
            if testx + 2 == self.pos[0] or testx - 2 == self.pos[0]:
                return True
        elif testy + 2 == self.pos[1] or testy - 2 == self.pos[1]:
            if testx + 1 == self.pos[0] or testx - 1 == self.pos[0]:
                return True
        return False


class King(Piece):
    def __init__(self, teamColor):
        super().__init__(teamColor)
        # self.renderText('K')
        if self.teamColor == 'w':
            self.sprite = whiteSprites[4]
            self.name = 'K'
        else:
            self.sprite = blackSprites[4]
            self.name = 'k'
        self.notMoved = True
    
    def testMoveSet(self, testx, testy):
        if (testy == self.pos[1] or testy + 1 == self.pos[1] or testy - 1 == self.pos[1]) and (testx == self.pos[0] or testx + 1 == self.pos[0] or testx - 1 == self.pos[0]):
            self.notMoved = False
            return True
        elif self.teamColor == 'w':
            if self.notMoved and type(pieces[7][7]) is Rook and pieces[7][7].notMoved and testy == 7 and testx == 6:
                if pieces[7][5] == None and pieces[7][6] == None:
                    pieces[7][7] = None
                    pieces[7][5] = Rook('w')
                    pieces[7][5].getPos()
                    pieces[7][5].notMoved = False
                    self.notMoved = False
                    return True
            if self.notMoved and type(pieces[7][0]) is Rook and pieces[7][0].notMoved and testy == 7 and testx == 2:
                if pieces[7][1] == None and pieces[7][2] == None and pieces[7][3] == None:
                    pieces[7][0] = None
                    pieces[7][3] = Rook('w')
                    pieces[7][3].getPos()
                    pieces[7][3].notMoved = False
                    self.notMoved = False
                    return True
        elif self.teamColor == 'b':
            if self.notMoved and type(pieces[0][7]) is Rook and pieces[0][7].notMoved and testy == 0 and testx == 6:
                if pieces[0][5] == None and pieces[0][6] == None:
                    pieces[0][7] = None
                    pieces[0][5] = Rook('b')
                    pieces[0][5].getPos()
                    pieces[0][5].notMoved = False
                    self.notMoved = False
                    return True
            if self.notMoved and type(pieces[0][0]) is Rook and pieces[0][0].notMoved and testy == 0 and testx == 2:
                if pieces[0][1] == None and pieces[0][2] == None and pieces[0][3] == None:
                    pieces[0][0] = None
                    pieces[0][3] = Rook('b')
                    pieces[0][3].getPos()
                    pieces[0][3].notMoved = False
                    self.notMoved = False
                    return True
        return False


class Queen(Piece):
    def __init__(self, teamColor):
        super().__init__(teamColor)
        # self.renderText('Q')
        if self.teamColor == 'w':
            self.sprite = whiteSprites[5]
            self.name = 'Q'
        else:
            self.sprite = blackSprites[5]
            self.name = 'q'

    def testMoveSet(self, testx, testy):
        rowDiff = abs(testy - self.pos[1])
        columnDiff = abs(testx - self.pos[0])
        if testy == self.pos[1]:
            for column in range(1, columnDiff):
                if testx > self.pos[0]:
                    if pieces[self.pos[1]][self.pos[0] + column] != None:
                        return False
                elif testx < self.pos[0]:
                    if pieces[self.pos[1]][self.pos[0] - column] != None:
                        return False
            return True
        elif testx == self.pos[0]:
            for row in range(1, rowDiff):
                if testy > self.pos[1]:
                    if pieces[self.pos[1] + row][self.pos[0]] != None:
                        return False
                elif testy < self.pos[1]:
                        if pieces[self.pos[1] - row][self.pos[0]] != None:
                            return False
            return True
        if rowDiff == columnDiff:
            for diagDiff in range(1, rowDiff):
                if testy > self.pos[1]:
                    if testx > self.pos[0]:
                        if pieces[self.pos[1] + diagDiff][self.pos[0] + diagDiff] != None:
                            return False
                    elif testx < self.pos[0]:
                        if pieces[self.pos[1] + diagDiff][self.pos[0] - diagDiff] != None:
                            return False
                elif testy < self.pos[1]:
                    if testx > self.pos[0]:
                        if pieces[self.pos[1] - diagDiff][self.pos[0] + diagDiff] != None:
                            return False
                    elif testx < self.pos[0]:
                        if pieces[self.pos[1] - diagDiff][self.pos[0] - diagDiff] != None:
                            return False
            return True
        return False


class Button(pygame.Rect):
    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height)
        self.text = font.render(text, True, (0, 0, 0))

    def draw(self):
        pygame.draw.rect(win, (0,0,0), self, 5)
        win.blit(self.text, (self.x + 7, self.y + 10))


def testCheck():
    if turn == 'w':
        for row in pieces:
            for piece in row:
                if piece != None:
                    if piece.teamColor == 'b':
                        if piece.testMoveSet(whiteKing.pos[0], whiteKing.pos[1]):
                            return True
        return False
    else:
        for row in pieces:
            for piece in row:
                if piece != None:
                    if piece.teamColor == 'w':
                        if piece.testMoveSet(blackKing.pos[0], blackKing.pos[1]):
                            return True
        return False

def testNoMoves():
    for rowPieces in pieces:
        for piece in rowPieces:
            if piece != None:
                if piece.teamColor == turn:
                    for row in range(8):
                        for column in range(8):
                            if pieces[row][column] != None:
                                if pieces[row][column].teamColor == piece.teamColor:
                                    continue
                            try:
                                if (type(pieces[row + 1][column]) is Pawn or type(pieces[row - 1][column]) is Pawn) and pieces[row + 1][column].isPassantable:
                                    continue
                            except:
                                pass
                            if piece.testMoveSet(column, row):
                                goToSquare = pieces[row][column]
                                prevRow, prevColumn = piece.pos[1], piece.pos[0]
                                pieces[prevRow][prevColumn] = None
                                pieces[row][column] = piece
                                piece.getPos()
                                if not testCheck():
                                    pieces[row][column] = goToSquare
                                    pieces[prevRow][prevColumn] = piece
                                    piece.getPos()
                                    return False
                                pieces[row][column] = goToSquare
                                pieces[prevRow][prevColumn] = piece
                                piece.getPos()
    return True

def turnSwitch():
    global turn
    if turn == 'w':
        turn = 'b'
    else:
        turn = 'w'

def restartBoard():
    global turn
    global whiteKing
    global blackKing
    global moveList
    whiteKing = King('w')
    blackKing = King('b')
    turn = 'w'
    moveList = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR']
    readFEN(moveList[0])

def generateFEN():
    FEN = []
    for row in pieces:
        rowFEN = ''
        empties = 0
        for piece in row:
            if piece == None:
                empties += 1
            else:
                if empties != 0:
                    rowFEN += str(empties)
                    empties = 0
                rowFEN += piece.name
        else:
            if empties != 0:
                rowFEN += str(empties)
                empties = 0
        FEN.append(rowFEN)
    return '/'.join(FEN)

def readFEN(FEN):
    global pieces
    pieces = [[], [], [], [], [], [], [], []]
    rowNum = 0
    for c in FEN:
        if c == 'p':
            pieces[rowNum].append(Pawn('b'))
        elif c == 'P':
            pieces[rowNum].append(Pawn('w'))
        elif c == 'r':
            pieces[rowNum].append(Rook('b'))
        elif c == 'R':
            pieces[rowNum].append(Rook('w'))
        elif c == 'n':
            pieces[rowNum].append(Knight('b'))
        elif c == 'N':
            pieces[rowNum].append(Knight('w'))
        elif c == 'b':
            pieces[rowNum].append(Bishop('b'))
        elif c == 'B':
            pieces[rowNum].append(Bishop('w'))
        elif c == 'q':
            pieces[rowNum].append(Queen('b'))
        elif c == 'Q':
            pieces[rowNum].append(Queen('w'))
        elif c == 'k':
            pieces[rowNum].append(blackKing)
        elif c == 'K':
            pieces[rowNum].append(whiteKing)
        elif c == '/':
            rowNum += 1
        else:
            for _ in range(int(c)):
                pieces[rowNum].append(None)
    for row in pieces:
        for piece in row:
            if piece != None:
                piece.getPos()

def undo():
    if len(moveList) != 1:
        moveList.pop()
        readFEN(moveList[-1])
        turnSwitch()

def updateDisplay():
    win.fill((255,255,255))
    board.draw()
    for row in pieces:
        for piece in row:
            if piece != None:
                piece.draw()
    resetButton.draw()
    undoButton.draw()
    win.blit(title, (450, 50))
    win.blit(coolPicSmall, (450, 50))
    pygame.display.update()

resetButton = Button(650, 300, 100, 50, 'Reset')
undoButton = Button(450, 300, 100, 50, 'Undo')
title = font.render('Jared\'s Chess Game', True, (0,0,0))
restartBoard()
mClick = False
clickedPiece = None
run = True
while run:
    clock.tick(60)

    mx, my = pygame.mouse.get_pos()
    mouseOnBoard = False
    if mx < board.totalSize:
        mColumn, mRow = (mx//board.squareSize, my//board.squareSize)
        mouseOnBoard = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if pygame.mouse.get_pressed()[0] and mouseOnBoard:
        if mClick == False:
            mClick = True
            offsetmx, offsetmy = mx % board.squareSize, my % board.squareSize
            clickedmRow, clickedmColumn = mRow, mColumn
            if pieces[mRow][mColumn] != None:
                if pieces[mRow][mColumn].teamColor == turn:
                    clickedPiece = pieces[mRow][mColumn]
                    clickedPieceRow, clickedPieceColumn = clickedPiece.pos[1], clickedPiece.pos[0]
        elif mClick == True:
            if clickedPiece != None and pieces[clickedmRow][clickedmColumn] == clickedPiece:
                clickedPiece.x = mx - offsetmx
                clickedPiece.y = my - offsetmy

    elif not pygame.mouse.get_pressed()[0] and mouseOnBoard:
        if mClick == True:
            mClick = False
            if clickedPiece != None:
                notSameColor = True
                if pieces[mRow][mColumn] != None:
                    if pieces[mRow][mColumn].teamColor == clickedPiece.teamColor:
                        notSameColor = False
                if clickedPiece.teamColor == turn and clickedPiece.testMoveSet(mColumn, mRow) and notSameColor:
                    prevPiece = pieces[mRow][mColumn]
                    pieces[clickedPieceRow][clickedPieceColumn] = None
                    pieces[mRow][mColumn] = clickedPiece
                    pieces[mRow][mColumn].getPos()
                    if testCheck():
                        pieces[mRow][mColumn] = prevPiece
                        pieces[clickedPieceRow][clickedPieceColumn] = clickedPiece
                        clickedPiece.getPos()
                    else: 
                        turnSwitch()
                        moveList.append(generateFEN())
                        if testCheck():
                            if testNoMoves():
                                print('checkmate')
                            else:
                                print('check')
                        elif testNoMoves():
                            print('stalemate')
                        for row in pieces:
                            for piece in row:
                                if type(piece) is Pawn:
                                    if piece.teamColor == turn:
                                        piece.isPassantable = False
                else:
                    clickedPiece.getPos()
    
    elif pygame.mouse.get_pressed()[0]:
        if mClick == False:
            mClick = True
            if resetButton.collidepoint(mx, my):
                restartBoard()
            elif undoButton.collidepoint(mx, my):
                undo()
    elif not pygame.mouse.get_pressed()[0]:
        mClick = False
            
    updateDisplay()
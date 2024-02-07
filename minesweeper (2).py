#We took help from ChatGPT and internet for this game.
import random
import time
import copy
from os import system, name
#Printing welcome message
print('''  \033[33m 
███╗   ███╗██╗███╗   ██╗███████╗███████╗██╗    ██╗███████╗███████╗██████╗ ███████╗██████╗ 
████╗ ████║██║████╗  ██║██╔════╝██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗
██╔████╔██║██║██╔██╗ ██║█████╗  ███████╗██║ █╗ ██║█████╗  █████╗  ██████╔╝█████╗  ██████╔╝
██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ╚════██║██║███╗██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗
██║ ╚═╝ ██║██║██║ ╚████║███████╗███████║╚███╔███╔╝███████╗███████╗██║     ███████╗██║  ██║
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝''')
def clear():
    time.sleep(0.2)
    if name == 'nt':
        system('cls')
    else:
        _ = system('clear')
    

def openbox(rown, col, gridblank, board, size):
    #for the row above
    if rown -1 > -1:
        row = gridblank[rown-1]
        if col - 1> -1:
            row[col-1] = loc(rown-1, col-1, board)
            row[col] = loc(rown -1, col, board)
        if size > col+1:
            row[col+1] = loc(rown-1, col +1, board)
    
    #for the same row
    row = gridblank[rown]
    if col -1 > -1:
        row[col - 1] = loc(rown, col-1, board)
    if size > col +1:
        row[col +1] = loc(rown, col+1, board)

    #for the row below
    if size > rown +1:
        row = gridblank[rown+1]
        if col -1 > -1:
            row[col-1] = loc(rown+1, col-1, board)
            row[col] = loc(rown+1, col, board)
        if size > col +1:
            row[col+1] = loc(rown+1, col+1, board)



#openingin up all the boxes  around a 0 because they cant have a bomb 
def checkzeros(gridblank, board, row, col, size):
    oldgrid = copy.deepcopy(gridblank)
    openbox(row, col, gridblank, board,size) #opens up the boxes
    if oldgrid == gridblank:
        return
    while True:
        oldgrid = copy.deepcopy(gridblank)
        for x in range(size):
            for y in range(size):
                if loc(x, y, gridblank) == 0:
                    openbox(x, y, gridblank, board, size)
        if oldgrid == gridblank:
            return


#placing the marker
def marker(row, col, gridblank, size):
    gridblank[row][col] = '⚐ '
    printBoard(gridblank, size)

def choose(board, gridblank, starttime, size):
    letters = []
    for i in range(size):
        letters.append(chr(97 + i))
    
    numbers = []
    for j in range(size):
        numbers.append(str(j))
    
    
    #asking for location and checking if input is valid
    while True:
        chosen = input("Choose a sqaure (eg. E4) or place a marker (eg. mE4): ").lower()
        #checking if sqaure is valid
        if len(chosen) == 3 and chosen[0] == 'm' and chosen [1] in letters and chosen[2] in numbers:
            col, row = (ord(chosen[1]) - 97, int(chosen[2]))
            marker(row, col, gridblank, size)
            play(board, gridblank, starttime, size)
            break
        elif len(chosen) == 2 and chosen[0] in letters and chosen[1] in numbers:
            col, row = (ord(chosen[0])-97, int(chosen[1]))
            break
    return col, row

def countBombs(board):
    count = 0
    for row in board:
        count += row.count("*")
    return count

#playing the game
def play(board, gridblank, starttime, size):
    #asking player to choose the sqaure
    col , row = choose(board, gridblank, starttime, size)
    #geting the value at the choosen location
    v = loc(row, col, board)
    #checking if a bomb is there
    if v =="*":
        printBoard(board, size)
        print(''' \033[36m 
██╗   ██╗ ██████╗ ██╗   ██╗      
╚██╗ ██╔╝██╔═══██╗██║   ██║      
 ╚████╔╝ ██║   ██║██║   ██║      
  ╚██╔╝  ██║   ██║██║   ██║      
   ██║   ╚██████╔╝╚██████╔╝      
   ╚═╝    ╚═════╝  ╚═════╝       
                                 
██╗      ██████╗ ███████╗███████╗
██║     ██╔═══██╗██╔════╝██╔════╝
██║     ██║   ██║███████╗█████╗  
██║     ██║   ██║╚════██║██╔══╝  
███████╗╚██████╔╝███████║███████╗
╚══════╝ ╚═════╝ ╚══════╝╚══════╝
                                 

  ''')
      
        #print the time 
        print('You played For', str(round(time.time()- starttime)), 'seconds')
        #offer the player to play again
        playagain = input('Play again? (Y/N): ').lower()
        if playagain == 'y':
            setupgame()
        else:
            print("Goodbye!")
            exit()
    #adding the value in the gridblank
    gridblank[row][col] = v
    #check if the value (v) is 0
    if v == 0:
        checkzeros(gridblank, board, row, col, size)
    printBoard(gridblank, size)
    #check to see if you player wins by seeing if the the number of sqaures left are SIZE+1 i.e successfully managed to select locations wherer there were no mines counting uncovered boxes
    uncovered = 0
    for x in range(size):
        for y in range(size):
            if gridblank[x][y] != " " and board[x][y] !="*":
                uncovered += 1
    non_bombsqaures = size * size - countBombs(board)
    
    if uncovered == non_bombsqaures:
        printBoard(board, size)
        print('''\033[37m  
██╗   ██╗ ██████╗ ██╗   ██╗    
╚██╗ ██╔╝██╔═══██╗██║   ██║    
 ╚████╔╝ ██║   ██║██║   ██║    
  ╚██╔╝  ██║   ██║██║   ██║    
   ██║   ╚██████╔╝╚██████╔╝    
   ╚═╝    ╚═════╝  ╚═════╝     
                               
██╗    ██╗██╗███╗   ██╗        
██║    ██║██║████╗  ██║        
██║ █╗ ██║██║██╔██╗ ██║        
██║███╗██║██║██║╚██╗██║        
╚███╔███╔╝██║██║ ╚████║        
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝        
                                 ''')
        
        #print the time 
        print('You played for', str(round(time.time()- starttime)), 'seconds')
        #offer to play again
        playagain = input('Play again? (Y/N): ').lower()
        if playagain == 'y':
            clear()
            setupgame()
        else:
            print("Goodbye!")
            exit()
    #repeats
    play(board, gridblank, starttime, size)


#printing the print for variable grid sizes
def printBoard(c, size):
    clear()
    board = c
    letters = [chr(65+i) for i in range(size)]
    maxwidth = len(str(size-1)) #max widht of largest label

    #printing the letters for the top
    print("       ","     ".join([letter for letter in letters]))
    #print the top border
    print("   ", "╔═════" + "╦═════" *(size -1) + "╗")

    #printing the rows and chaning bomb tos 💣 fruom *
    for r in range(size):
        rowvalues = [str(loc(r, col, board)) if loc(r, col, board) != "*" else '💣' for col in range(size)]
                
        for i in range(len(rowvalues)):
            if str(rowvalues[i]).isdigit() or str(rowvalues[i])==' ':
                rowvalues[i] = ''+str(rowvalues[i]) + ' ' 
        if '💣' in rowvalues:
            print(str(r), "  ║ ", " ║  ".join(rowvalues) + " ║")
        else:
            print(str(r), "  ║ ", " ║  ".join(rowvalues) + " ║")

        if r != size - 1:
            #print the seperator b/w rows
            print("   ", "╠═════" + "╬═════" * (size-1) + "╣")
    #print the bottom border
    print("   ", "╚═════" + "╩═════" * (size-1) + "╝")




#updating/ adding 1s to all the sqaures surrounded by a bomb
def upadteValues(rown, col, board, size):
    #for the row above
    if rown - 1 > - 1:
        row = board[rown - 1]

        if col - 1 > -1:
            if row[col-1] != "*":
                row[col-1] += 1
        if row[col] != "*":
            row[col] += 1
        if size > col + 1:
            if row [col+1] != "*":
                row[col +1] += 1

    # in the same row
    row = board[rown]
    if col - 1 > -1:
        if row[col-1] != "*":
            row[col-1] += 1
    if size > col + 1:
        if row[col +1] != "*":
            row[col +1] += 1
    
    #for the row below
    if size > rown +1:
        row = board[rown+1]

        if col - 1 > -1:
            if row[col-1] != "*":
                row[col-1] += 1
        
        if row[col] != "*":
            row[col] += 1
        
        if size > col+1:
            if row[col+1] != "*":
                row[col+1] += 1


#getting the value from board at the location/coordinates
def loc(r, c, board):
    return board[r][c]

#function to place the placeBomb
def placeBomb(board, size):
    row = random.randint(0,size-1)
    col = random.randint(0,size-1)
    #check if bomb is already in the location generated and if its already there get another location
    if board[row][col] != "*":
        board[row][col] = "*"
    else:
        placeBomb(board, size)
    
    
#setting up the game i.e the main menu and instructions 
def setupgame():
    print('''
Main Menu
=========

--> For instructions on how to play, type 'I'
--> To play the game, type 'P'
--> To exit type 'E'
''')
    
    while True: 
        choice = input("Type here: ").upper()
        if choice == "I":
            #printing the instructions
            print(open('instruction.txt', 'r').read())
            input("Press [enter] when ready to play. ")
            break
    #if doewsnt enter p or i we want to show the user this again
        elif choice == "E":
            print("Goodbye!")
            exit()
        elif choice == "P":
            break
        print("Invalid input try again")
    while True:
        size = int(input("Choose grid size (4-10): "))
        if size >=4 and size <= 10:
            break
        else:
            print("Invalid input")
    

    #getting the grid
    board = []
    l  = []
    for i in range(size):
        for j in range(size+1):
            l.append(0)
            if j  == size:
                board.append(l)
                l = []
                break
    #placing the bomb in the board
    for n in range(0, size+1):
        placeBomb(board, size)


    #chaning the vlaues of 0 in the board to the number of bombds they are surrounded by
    for r in range(size):
        for c in range(size):
            value = loc(r, c, board)
            if value == '*':
                upadteValues(r, c, board, size)
    # seting up a grid of blank spaces as nothing is know abt the grid due to random placement of bombds
    gridblank = []
    k = []
    for a in range(size):
        for b in range(size+1):
            k.append(" ")
            if b == size:
                gridblank.append(k)
                k = []
                break
    printBoard(gridblank, size)

    #starting the Time
    starttime = time.time()

    #playing the game
    play(board, gridblank, starttime, size)

setupgame()






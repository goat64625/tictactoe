import random
import mysql.connector as pysql
X = [[" ▄▄   ▄▄  "],
     ["█  █▄█  █ "],
     ["█       █ "],
     ["█       █ "],
     [" █     █  "],
     ["█   ▄   █ "],
     ["█▄▄█ █▄▄█ "]]
O = [[" ▄▄▄▄▄▄▄  "],
     ["█       █ "],
     ["█   ▄   █ "],
     ["█  █ █  █ "],
     ["█  █▄█  █ "],
     ["█       █ "],
     ["█▄▄▄▄▄▄▄█ "]]
S = [["          "],
     ["          "],
     ["          "],
     ["          "],
     ["          "],
     ["          "],
     ["          "]]
#connecting to database use user='root',passwd='Isalain',database="tictactoe"
conn = pysql.connect(host="localhost",user="gay",database='test')
c = conn.cursor()
#checking i the table score exists
c.execute("show tables ")
data=c.fetchall()
if "score" not in data[0]:
    c.execute("CREATE TABLE score(name varchar(15), win int(3),loss int(3),draw int(3))")
#verified
#login/creat a user
def login(user):
    c.execute("SELECT * FROM score")
    data = c.fetchall()
    if user in data[0]:
        print("hello"+name)
    else:
        cmd="INSERT INTO score VALUES('"+name+"',0,0,0)"
        c.execute(cmd)
        print(cmd)
        input()

while True:
    try:
        name = input("Enter your name :")
        login(name)
        break
    except:
        continue
#add to win loss and draw
def updateScore(name,s):
    cmd = "SELECT * FROM score WHERE name='"+name+"'"
    c.execute(cmd)
    data=c.fetchall()
    if s == "win":
        new_score=data[0][1]+1
        cmd = "UPDATE score SET win="+str(new_score)+" WHERE name='"+name+"'"
        c.execute(cmd)
    elif s == "loss":
        new_score=data[0][2]+1
        cmd = "UPDATE score SET loss="+str(new_score)+" WHERE name='"+name+"'"
        c.execute(cmd)
    else:
        new_score=data[0][3]+1
        cmd = "UPDATE score SET draw="+str(new_score)+" WHERE name='"+name+"'"
        c.execute(cmd)
def printTable():
    print("NAME"," "* int(len(name)-3), "WIN  LOSS  DRAW")
    for row in data:
        for i in range(0,4):
            print(row[i],end="    ")
        print()
def printboard(board,trail=''):
    for i in range(3):
        for k in range(7):
            print(trail+' ',str(board[i][0][k])[2:-2],end='|',sep='')
            print(str(board[i][1][k])[2:-2],end='|')
            print(str(board[i][2][k])[2:-2],end=trail+'\n')
            if k == 6:
                if i < 2:
                    print(trail,"-"*11+'+'+"-"*10+'+'+"-"*10,end=trail+'\n',sep='')
def isMovesLeft(board) :
    for i in range(3) :
        for j in range(3) :
            if (board[i][j] == S) :
                return True
    return False
def checkwon(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != S:
            return (board[i][0])
        if board[0][i] == board[1][i] == board[2][i] != S:
            return (board[0][i])
    if board[1][1] == board[2][2] == board[0][0] != S:
        return (board[0][0])
    if board[0][2]==board[1][1]==board[2][0] !=S:
        return (board[i][0]) 
    return None
def evaluate(b,player,opponent):
    for row in range(3) :   
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]) :    
            if (b[row][0] == player) :
                return 10
            elif (b[row][0] == opponent) :
                return -10
        if (b[0][row] == b[1][row] and b[1][row] == b[2][row]) :
            if (b[0][row] == player) :
                return 10
            elif (b[0][row] == opponent) :
                return -10
    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]) :
        if (b[0][0] == player) :
            return 10
        elif (b[0][0] == opponent) :
            return -10
    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]) :
        if (b[0][2] == player) :
            return 10
        elif (b[0][2] == opponent) :
            return -10
    return 0
def minimax(board,depth, isMax,player=O,opponent=X) :
    score = evaluate(board,player,opponent)
    if (score == 10):
        return score
    if (score == -10):
        return score
    if (isMovesLeft(board) == False):
        return 0
    if (isMax) :    
        best = -10000000
        for i in range(3) :     
            for j in range(3) :
                if (board[i][j]==S) :
                    board[i][j] = player
                    best = max( best, minimax(board,depth + 1,not isMax,player,opponent) )
                    board[i][j] = S
        return best
    else :
        best = 10000000
        for i in range(3) :     
            for j in range(3) :
                if (board[i][j] == S) :
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, not isMax,player,opponent))
                    board[i][j] = S
        return best
def findBestMove(board,player=O,opponent=X) :
    bestVal = -10000000
    bestMove = (-1, -1)
    for i in range(3) : 
        for j in range(3) :
            if (board[i][j] == S) :
                board[i][j] = player
                moveVal = minimax(board, 1, False,player,opponent)
                board[i][j] = S
                if (moveVal > bestVal) : 
                    bestMove = (i, j)
                    bestVal = moveVal
    return bestMove
def winscreen(winner,player=None):
    if player == 'y':
        print('''
           ▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄
           █▒▒░░░░░░░░░▒▒█
            █░░█░░░░░█░░█
         ▄▄  █░░░▀█▀░░░█  ▄▄
        █░░█ ▀▄░░░░░░░▄▀ █░░█''')
    print("▄"*35) 
    printboard(board,"█")
    print("█","▄"*33,"█",sep='')
    if winner == X:
        print('''
 ▄▄   ▄▄ 
█  █▄█  █
█       █
█       █
 █     █ 
█   ▄   █
█▄▄█ █▄▄█ is the winner''')
    else:
        print('''
 ▄▄▄▄▄▄▄ 
█       █
█   ▄   █
█  █ █  █
█  █▄█  █
█       █
█▄▄▄▄▄▄▄█ is the winner''')
    input('enter to start')
def printPlayer(player):
    for i in range(7):
        print(str(player[i])[2:-3])
def playerMove(player):
    print()
    printPlayer(player)
    move = input("Make you'r move  : ")
    if not validMove(move) :
            print("invalid move try again ")
            playerMove(player)
    else:
        board[int(move[0])-1][int(move[1])-1] = player
def validMove(pos):
    if int(pos)> 10 and int(pos[1])<4 and int(pos) < 34 and board[int(pos[0])-1][int(pos[1])-1] == S and pos.strip() != '' and int(pos[1]) < 4 and int(pos) in [11,12,13,21,22,23,31,32,33] :
        return True
    else:
        return False
def Mgame():
    global board
    while True:
        printboard(board)
        playerMove(X)
        if checkwon(board):
                winscreen(checkwon(board),'y')
                board = [[S,S,S],[S,S,S],[S,S,S]]
                break
        printboard(board)
        playerMove(O)
        if checkwon(board):
                winscreen(checkwon(board),'y')
                break
                board = [[S,S,S],[S,S,S],[S,S,S]]
def EAI(board):
    global winner
    while True:
        playerMove(X)
        if checkwon(board):
            winscreen(checkwon(board),'y')
            updateScore(name,"win")
            break
        if not isMovesLeft(board):
            updateScore(name,"draw")
            print("its a draw")
            input('enter to start')
            menu()
            break
        while True:
            Opos = ['11','12','13','21','22','23','31','32','33'][random.randint(0,8)]
            if not validMove(Opos):
                continue
            else:
                break
        board[int(Opos[0])-1][int(Opos[1])-1] = O 
        if checkwon(board):
            winscreen(checkwon(board))
            updateScore(name,"loss")
            board = [[S,S,S],[S,S,S],[S,S,S]]
            break
        printboard(board)
    board = [[S,S,S],[S,S,S],[S,S,S]]
def HAI(board):
    if  random.randint(0,1)==0:
        player = X
        AI = O
        while True:
            printboard(board)
            playerMove(player)
            if checkwon(board) != None:
                winscreen(checkwon(board),'y')
                updateScore(name,"win")
                break
            if not isMovesLeft(board):
                printboard(board)
                updateScore(name,"draw")
                print("its a draw")
                input('enter to start')
                break
            bestMove = findBestMove(board,AI,player)
            board[bestMove[0]][bestMove[1]] = AI
            if checkwon(board) != None:
                winscreen(checkwon(board))
                updateScore(name,"loss")
                break
            if not isMovesLeft(board):
                printboard(board)
                updateScore(name,"draw")
                print("its a draw")
                input('enter to start')
                break
    else:
        player =O
        AI = X
        while True:
            bestMove = findBestMove(board,AI,player)
            board[bestMove[0]][bestMove[1]] = AI
            if checkwon(board) != None:
                winscreen(checkwon(board))
                updateScore(name,"loss")
                break
            if not isMovesLeft(board):
                printboard(board)
                updateScore(name,"draw")
                print("its a draw")
                input('enter to start')
                break
            printboard(board)
            playerMove(player)
def selectmode():
    print('''
 ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄     ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
█       █       █   █   █       █       █       █
█  ▄▄▄▄▄█    ▄▄▄█   █   █    ▄▄▄█       █▄     ▄█
█ █▄▄▄▄▄█   █▄▄▄█   █   █   █▄▄▄█     ▄▄█ █   █  
█▄▄▄▄▄  █    ▄▄▄█   █▄▄▄█    ▄▄▄█    █    █   █  
 ▄▄▄▄▄█ █   █▄▄▄█       █   █▄▄▄█    █▄▄  █   █  
█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█ █▄▄▄█  
1 for multipalyer
2 for single player
3 for single player(hard)
4 Back
          ''')
    choice = int(input())
    if choice == 1:
        return(1)
    elif choice == 2:
        return(2)
    elif choice == 3:
        return(3)
    elif choice == 4:
        return(4)
def menu():
    print('''
 ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄   ▄▄▄▄▄▄▄ 
█       █       █      █   ▄  █ █       █
█  ▄▄▄▄▄█▄     ▄█  ▄   █  █ █ █ █▄     ▄█
█ █▄▄▄▄▄  █   █ █ █▄█  █   █▄▄█▄  █   █  
█▄▄▄▄▄  █ █   █ █      █    ▄▄  █ █   █  
 ▄▄▄▄▄█ █ █   █ █  ▄   █   █  █ █ █   █  
█▄▄▄▄▄▄▄█ █▄▄▄█ █▄█ █▄▄█▄▄▄█  █▄█ █▄▄▄█  
1 to paly:
2 to see leaderboard: 
3 to Quit:
''')
    return int(input("Enter (1/2/3): "))

mode = 0
while True:
    board = [[S,S,S],[S,S,S],[S,S,S]]
    mode=0
    mode = menu()
    if mode == 1:
        mode = 0
        mode = selectmode()
        if mode == 1:
                Mgame()
        elif mode == 2:
                EAI(board)
        elif mode == 3:
                HAI(board)
    elif mode == 2:
        pass
    elif mode == 3:
        break

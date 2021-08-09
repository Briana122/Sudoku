import pygame #python pygame modules
import time #python time module
import Sudoku_Solver_Class #sudoku solver class
import Timer_Class #timer class

#activate pygame library and allow pygame functionalities
pygame.init()

#rgb colour codes
WHITE = (255,255,255)
DARK_BLUE = (0,0,102)
MAROON = (102,0,51)
GRAY = (192,192,192)
BLACK = (0,0,0)
RED = (255,0,0)
PINK = (204, 0, 102)
GREEN = (0, 153, 0)

#create font object, use default font
TITLEFONT = pygame.font.Font(pygame.font.get_default_font(), 48)
NUMFONT = pygame.font.Font(pygame.font.get_default_font(), 36)
MEDIUMFONT = pygame.font.Font(pygame.font.get_default_font(), 24)
SMALLFONT = pygame.font.Font(pygame.font.get_default_font(), 18)

#set and declare screen display parameters
WIDTH, HEIGHT = 800, 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku!")
FPS = 60    # variable to store the display-update frequency - 20 frames per second

#create global variables
CLICKED = False                             #clicked on a Sudoku box
CLICKED_X, CLICKED_Y = 0,0                  #x/y pixel coordinates of clicked Sudoku box
CLICKED_POS_X, CLICKED_POS_Y = 0,0          #x/y grid coordinates of clicked Sudoku box
GET_GRID = False                            #has called Sudoku-Solver class to obtain solved grid
SPACE_PRESSED = False                       #quit
TIMER = Timer_Class.Timer()                       #call timer class
PLAYER_TIMER ='00:00'                       #store time elapsed
WIN = False

#create 2D arrays for 9x9 Sudoku grids
UNSOLVED_GRID =  [[0 for x in range (9)] for y in range (9)]
PLAYER_INPUT_GRID = [[0 for x in range (9)] for y in range (9)]
PLAYER_CORRECT_GRID = [[0 for x in range (9)] for y in range (9)]
SOLVED_GRID = [[0 for x in range (9)] for y in range (9)]

# FUNCTION - draws Sudoku game board, the given numbers, user's temporary numbers, and correct user inputs
def draw_board(input_value):
    
    global UNSOLVED_GRID, PLAYER_INPUT_GRID, PLAYER_CORRECT_GRID, SPACE_PRESSED, WIN

    #call draw_Timer function
    draw_timer()

    for j in range(9):
        for i in range(9):
            #set coordinates of box squares
            square_x = 100 + (j*70)
            square_y = 130 + (i*70)

            #set coorinates of numbers
            num_x = 120 + (j*70)
            num_y = 145 + (i*70)

            #store number from given Sudoku grid
            num = UNSOLVED_GRID[i][j] + PLAYER_CORRECT_GRID[i][j]

            #colour each 3x3 Sudoku grid appropriately - white and gray
            if ((j in range (3) and i in range (3)) or (j in range (6,9) and i in range (3)) or
                (j in range (3,6) and i in range (3,6)) or (j in range (3) and i in range (6,9)) or
                (j in range (6,9) and i in range (6,9))):
                pygame.draw.rect(WINDOW, GRAY, pygame.Rect(square_x, square_y, 60, 60))

            else:
                pygame.draw.rect(WINDOW, WHITE, pygame.Rect(square_x, square_y, 60, 60))

            #check if user quit (pressed SPACE) or won (WIN)
            if (SPACE_PRESSED):
                draw_quit_message(i, j, num_x, num_y)

            elif (WIN):
                draw_winner_message(i, j, num_x, num_y)

            #fill empty Sudoku slots w/ button, allowing user input
            if (num == 0 and not SPACE_PRESSED): 
                user_input(square_x, square_y, num_x, num_y, i, j , input_value)

                #fill user inputs - temporary answers
                fill_temp_input(i, j, num_x, num_y)

            #fill given Sudoku numbers into grid
            elif (UNSOLVED_GRID[i][j] != 0 and not SPACE_PRESSED):
                fill_given_nums(i, j, num_x, num_y, num)
                
            #fill correct player input into grid
            elif (PLAYER_CORRECT_GRID[i][j] != 0 and not SPACE_PRESSED):
                fill_correct_input(i, j, num_x, num_y)

# FUNCTION - get mouse position when playing game and draws user number input
def user_input(square_x, square_y, num_x, num_y, x, y, input_value):

    #call global variables to keep track of position for user input and grids
    global CLICKED, CLICKED_X, CLICKED_Y, CLICKED_POS_X, CLICKED_POS_Y, PLAYER_INPUT_GRID, UNSOLVED_GRID, SPACE_PRESSED

    #get mouse position
    mouse_pos = pygame.mouse.get_pos()
    #get mouse click
    mouse_click = pygame.mouse.get_pressed()

    #outline box in red if user clicked it
    if (CLICKED == True):
        pygame.draw.rect(WINDOW, PINK, pygame.Rect(CLICKED_X, CLICKED_Y, 60, 60), 2)
        #COLOUR selected ROW, COLUMN, AND 3x3 GRID
        #print("(" + str(CLICKED_POS_X) + ", " + str(CLICKED_POS_Y) + ")")

        #store user input into PLAYER_INPUT_GRID
        if (input_value == '1'or input_value == '2' or input_value == '3' or input_value == '4' or 
            input_value == '5' or input_value == '6' or input_value == '7' or input_value == '8' or input_value == '9'):
            PLAYER_INPUT_GRID[CLICKED_POS_X][CLICKED_POS_Y] = int(input_value)
        #delete user input
        elif (input_value == 'del' and PLAYER_INPUT_GRID != 0):
            PLAYER_INPUT_GRID[CLICKED_POS_X][CLICKED_POS_Y] = 0
        #enter -> verify user input for selected square
        elif (input_value == 'ret'):
            enter_pressed()
        #space -> terminate game and reveal all answers
    if (input_value == 'space'):
        SPACE_PRESSED = True
            
    #keep track of mouse position and box clicked
    if (square_x < mouse_pos[0] < square_x + 60) and (square_y < mouse_pos[1] < square_y + 60):
        pygame.draw.rect(WINDOW, DARK_BLUE, pygame.Rect(square_x, square_y, 60, 60), 2)
        if mouse_click[0] == 1:
            input_rect = pygame.draw.rect(WINDOW, PINK, pygame.Rect(square_x, square_y, 60, 60), 2)
            #grid location of clicked box
            CLICKED_POS_X = x
            CLICKED_POS_Y = y
            #pixel location of clicked box
            CLICKED_X = square_x
            CLICKED_Y = square_y 
            input_value = ''
            #set global clicked to True
            CLICKED = True

# FUNCTION - draws timer
def draw_timer():

    global SPACE_PRESSED, WIN, TIMER, PLAYER_TIMER

    TIMER.start_timer()

    if (not SPACE_PRESSED and not WIN):
        PLAYER_TIMER = TIMER.get_time()   #update only if still playing

    timer_text = MEDIUMFONT.render('Timer: ' + PLAYER_TIMER, True, GRAY)
    timer_rect = timer_text.get_rect()
    WINDOW.blit(timer_text, (580,780)) 

# FUNCTION - draws correct user input
def fill_correct_input(i, j, num_x, num_y):
    global PLAYER_CORRECT_GRID
    #create text surface object for text
    num_text = NUMFONT.render(str(PLAYER_CORRECT_GRID[i][j]), True, GREEN)
    #create rectangular object for text surface object
    textRect = num_text.get_rect()
    WINDOW.blit(num_text, (num_x, num_y))

# FUNCTION - draws user temporary answers
def fill_temp_input(i, j, num_x, num_y):
    global PLAYER_INPUT_GRID
    if PLAYER_INPUT_GRID[i][j] != 0:
        #create text surface object for text
        num_text = NUMFONT.render(str(PLAYER_INPUT_GRID[i][j]), True, PINK)
        #create rectangular object for text surface object
        textRect = num_text.get_rect()
        WINDOW.blit(num_text, (num_x, num_y))

# FUNCTION - draws given Sudoku numbers
def fill_given_nums(i, j, num_x, num_y, num):
    #create text surface object for text
    num_text = NUMFONT.render(str(num), True, DARK_BLUE)
    #create rectangular object for text surface object
    textRect = num_text.get_rect()
    WINDOW.blit(num_text, (num_x, num_y))

# FUNCTION - checks user input and updates PLAYER_CORRECT_GRID
def enter_pressed():
    global SOLVED_GRID, PLAYER_INPUT_GRID, PLAYER_CORRECT_GRID, UNSOLVED_GRID

    for x in range(9):
        for y in range(9):
            if PLAYER_INPUT_GRID[x][y] == SOLVED_GRID[x][y]:
                PLAYER_CORRECT_GRID[x][y] = PLAYER_INPUT_GRID[x][y]                

# FUNCTION - prints quit message
def draw_quit_message(i, j, num_x, num_y):

    global SOLVED_GRID
    #create text surface object for text
    num_text = NUMFONT.render(str(SOLVED_GRID[i][j]), True, RED)
    #create rectangular object for text surface object
    textRect = num_text.get_rect()
    WINDOW.blit(num_text, (num_x, num_y))

    exit1 = SMALLFONT.render("You quit :( Thank you for playing", True, WHITE)
    exit1_rect = exit1.get_rect()
    WINDOW.blit(exit1, (265, 95))

# FUNCTION - prints out winner message
def draw_winner_message(i, j, num_x, num_y):

    global SOLVED_GRID
    #create text surface object for text
    num_text = NUMFONT.render(str(SOLVED_GRID[i][j]), True, GREEN)
    #create rectangular object for text surface object
    textRect = num_text.get_rect()
    WINDOW.blit(num_text, (num_x, num_y))

    win = SMALLFONT.render("CONGRATS! YOU WON! :)", True, WHITE)
    win_rect = win.get_rect()
    WINDOW.blit(win, (300, 95))

# FUNCTION - draws special key functions during game
def draw_key_option():
    message1 = SMALLFONT.render("Press 'ENTER' to check answers", True, WHITE)
    message2 = SMALLFONT.render("Press 'DEL' or 'BACKSPACE' to erase", True, WHITE)
    message3 = SMALLFONT.render("Press 'SPACE' to quit", True, WHITE)

    message1_rect = message1.get_rect()
    message2_rect = message2.get_rect()
    message3_rect = message3.get_rect()

    WINDOW.blit(message1, (30,790))
    WINDOW.blit(message2, (30,820))
    WINDOW.blit(message3, (30,850))    

# FUNCTION - returns del, ret or space depending on which key the user pressed
def key_pressed(key):
    if key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
        # get special key input - DEL, RETURN/ENTER and SPACE
        return 'del'
    elif key == pygame.K_RETURN:
        return 'ret'
    elif key == pygame.K_SPACE:
        return 'space'
    else:
        return event.unicode

# FUNCTION - call Solver class to get solved grid
def get_solved_grid(level_type):
    global SOLVED_GRID

    #create instance of sudoku solver to solve grid
    SOLVED_GRID = set_grid(level_type)
    solver1 = Sudoku_Solver_Class.Sudoku_Solver(SOLVED_GRID)

    #if the solver class successfully solves the grid, store it in SOLVED_GRID
    if (solver1.solve_Sudoku()):
        SOLVED_GRID = solver1.get_grid()

# FUNCTION - loops to check if user has solved the puzzle
def check_solved_grid():
    global UNSOLVED_GRID, PLAYER_CORRECT_GRID

    for i in range (9):
        for j in range(9):
            if UNSOLVED_GRID[j][i] == 0 and PLAYER_CORRECT_GRID[j][i] == 0:
                return False
    return True

# FUNCTION - calls functions to play the game 
def play_game(input_value, level_type):

    global UNSOLVED_GRID, SOLVED_GRID, GET_GRID, WIN

    #fill background with white colour  
    WINDOW.fill(MAROON)

    # Populate 2D array for Sudoku game
    UNSOLVED_GRID = set_grid(level_type)

    #solve the grid only once
    if (not GET_GRID):
        get_solved_grid(level_type)
        GET_GRID = True
    if (GET_GRID):
        draw_title()
        draw_key_option()
        draw_board(input_value)
        
        if (check_solved_grid()):
            WIN = True

    pygame.display.update()

# FUNCTION - calls functions for welcome screen, returns level user wants to play
def draw_welcome():
    WINDOW.fill(MAROON)
    draw_title()
    draw_instructions()
    level_type = draw_levels()

    pygame.display.update()
    return level_type

# FUNCTION - draws Sudoku title
def draw_title():
    #create text surface object for text
    text = TITLEFONT.render('SUDOKU', True, WHITE)
    #create rectangular object for text surface object
    text_rect = text.get_rect()
    WINDOW.blit(text, (305,40))

# FUNCTION - draws Sudoku instructions
def draw_instructions():
    #create text surface object for text
    instruction1 = SMALLFONT.render('Welcome to Sudoku!', True, WHITE)
    instruction2 = SMALLFONT.render('The goal of the game is to fill the 9x9 grid with numbers from 1 to 9,', True, WHITE)
    instruction3 = SMALLFONT.render('unique in every row, column and 3x3 grid. Good luck! :)', True, WHITE)
    instruction4 = SMALLFONT.render('Please choose a difficulty level:', True, WHITE)

    #create rectangular object for text surface object
    instruction1_rect = instruction1.get_rect()
    instruction2_rect = instruction2.get_rect()
    instruction3_rect = instruction3.get_rect()
    instruction4_rect = instruction4.get_rect()

    WINDOW.blit(instruction1, (20,130))
    WINDOW.blit(instruction2, (20,190))
    WINDOW.blit(instruction3, (20,220))
    WINDOW.blit(instruction4, (20,290))

# FUNCTION - draws levels and tracks whether the mouse position to return correct user selection
def draw_levels():
    #set text for level of difficulty
    easy = TITLEFONT.render('EASY', True, WHITE)
    easy_rect = easy.get_rect()
    pygame.draw.rect(WINDOW, WHITE, pygame.Rect(335, 340, 153, 63), 5)

    med = TITLEFONT.render('MEDIUM', True, WHITE)
    med_rect = med.get_rect()
    pygame.draw.rect(WINDOW, WHITE, pygame.Rect(305, 440, 215, 63), 5)

    hard = TITLEFONT.render('HARD', True, WHITE)
    hard_rect = med.get_rect()
    pygame.draw.rect(WINDOW, WHITE, pygame.Rect(335, 540, 160, 63), 5)

    #get mouse position
    mouse_pos = pygame.mouse.get_pos()

    #get mouse click
    mouse_click = pygame.mouse.get_pressed()

    if (335 < mouse_pos[0] < 335 + 153) and (340 < mouse_pos[1] < 340 + 63):
        #change rectangle colour
        pygame.draw.rect(WINDOW, PINK, pygame.Rect(335, 340, 153, 63))
        #return level if mouse is clicked
        if mouse_click[0] == 1:
            return 'easy'
    elif (305 < mouse_pos[0] < 305 + 215) and (440 < mouse_pos[1] < 440 + 63):
        pygame.draw.rect(WINDOW, PINK, pygame.Rect(305, 440, 215, 63))
        if mouse_click[0] == 1:
            return 'med'
    elif (335 < mouse_pos[0] < 335 + 160) and (540 < mouse_pos[1] < 540 + 63):
        pygame.draw.rect(WINDOW, PINK, pygame.Rect(335, 540, 160, 63))
        if mouse_click[0] == 1:
            return 'hard'

    WINDOW.blit(easy, (345,350))
    WINDOW.blit(med, (315,450))
    WINDOW.blit(hard, (345,550))

# FUNCTION - returns unsolved grid depending on user choice
def set_grid(level):
    #possible levels
    easy = [[0, 4, 7, 1, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 4, 8, 0, 0, 1],
            [8, 0, 0, 0, 0, 0, 0, 2, 0],
            [7, 2, 6, 0, 5, 4, 1, 0, 3],
            [0, 0, 0, 7, 0, 0, 5, 0, 2],
            [1, 0, 4, 2, 9, 3, 8, 0, 6],
            [0, 8, 2, 0, 3, 0, 0, 1, 0],
            [0, 0, 0, 9, 0, 0, 0, 0, 4],
            [4, 0, 5, 0, 0, 0, 0, 3, 7]]

    med = [[8, 0, 1, 0, 0, 0, 0, 0, 7],
            [0, 9, 7, 5, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 9, 7, 6, 0, 8],
            [0, 0, 0, 0, 5, 0, 0, 0, 3],
            [7, 8, 0, 3, 0, 4, 0, 0, 2],
            [0, 0, 3, 6, 7, 0, 1, 0, 0],
            [9, 7, 6, 2, 3, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 3, 2, 0],
            [0, 3, 0, 0, 0, 0, 0, 0, 0]]

    hard = [[0, 0, 0, 9, 1, 0, 7, 0, 0],
            [0, 6, 2, 0, 0, 0, 0, 9, 0],
            [4, 0, 9, 0, 0, 0, 1, 3, 0],
            [9, 1, 0, 8, 0, 0, 0, 2, 7],   
            [0, 0, 7, 0, 0, 3, 0, 0, 0],
            [0, 0, 4, 7, 0, 0, 6, 0, 3],
            [0, 0, 0, 6, 0, 0, 8, 0, 1],
            [0, 9, 0, 0, 7, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 8, 0, 0, 0]]

    #return the correct grid depending on which level the user picks
    if level == 'easy':
        return easy
    elif level == 'med':
        return med
    elif level == 'hard':
        return hard

#print Sudoku grid array
#def print_grid(arr):
#    for i in range(9):
#        for j in range(9):
#            print(arr[i][j], end = "  ")
#        print()

#MAIN CODE--------------------------------------------------------

# variable to control speed of while loop
clock = pygame.time.Clock()

# variable to ensure that window will be opened throughout runtime of game
running = True
welcome_loop = True
input_value = ''
while running:
    # control the speed of while loop
    clock.tick(FPS)
    for event in pygame.event.get():
        # if the player quits game, window will close
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
                # Check for backspace
                input_value = key_pressed(event.key)

    if welcome_loop == True:
        level_type = draw_welcome()
        if level_type != None:
            welcome_loop = False
    else:
        play_game(input_value, level_type)
    
    #reset input number 
    input_value = ''
pygame.quit()
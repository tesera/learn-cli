'''
A demonstration of interactive and object oriented programming
'''
import random

print ' Hello World'
name = raw_input(" Enter Your First Name and Press Enter ... ")

print ' \n\n\n Hi ', name,
print ' \n\n\n This is just a quick introduction to interactive programming in Python'
print ' Most of this came from the following website:  http://learn-to-program.net/userinput.htm'
#Now get a number ... Numbers are input using the input() command
#If you try to put a character in the program will crash
#To avoid a crash you would use raw_input() and then try to convert it to a number - if unsuccessful you would repeat the question 
#The raw_input() command converts everything to a string
endStatement = 'Yes'
i = 0
while endStatement == 'Yes':
    if i == 0:
        print " \n\n Lets try adding two numbers \n\n"
    else:
        print " \n Back in the saddle again \n\n"
        
    a = 0
    b = 0
    a = input(" Enter a number, Press Enter ... ")
    b = input(" Enter another number, Press Enter ... ")
    c = a + b
    print  '\n ', a, " plus ", b, " equals ", c
    print " \n Are you finished or would you like to do another addition?"
    endStatement = raw_input(" \n Please enter Yes and Press Enter if you want to continue, otherwise Press Enter ... ")
    if not endStatement == 'No':
        endStatement = 'No'
    i = i + 1
    
raw_input(" Press Enter to Continue To The Next Session ... ")


#This class statement is an example of object oriented programming
class Level: #make a class for level objects
    def __init__(self, cap, levelno): #when initializing, get cap and level no.
        self.cap = cap
        self.number = random.randint(0, cap) #Get random number between 0 and cap
        self.level = levelno

    def check_number(self, x): #Make function to tell if guess is high or low
        if x > self.number:
            print "That number is too high!"
            return False #If the number is higher, return false
        elif x < self.number:
            print "That number is too low!"
            return False #if the number is lower, return false
        else:
            print "That's it! YOU PASSED THE LEVEL"
            return True #if the number is equal to the right one, return true

print "\n\n\n\n Here is an interactive game"
print "\n This part of the program also involves Object Oriented Programming"
print "\n http://learn-to-program.net/classes.htm"

#The object Level is now initialized with different attributes -
#  where the name Level is associated with self under the class statement above
#The first value in the pranetheses refers to cap
#The second value refers levelno
#Different Levels are initialized each time the Level() statement is made
# according to the _init_ function under the class statement above
#Note also that a random number referred to as self,number is generated and assigned to each level

level1 = Level(100, 1)
level2 = Level(500, 2)
level3 = Level(1000, 3)
levels = [level1, level2, level3]
x = 0
currentlevel = levels[x] #set current level as level1

print "\n Welcome to Higher or Lower! Good Luck!"
print " Level", currentlevel.level, "\n\n"

running = 1

while running: #While true
    guess = input("\n Please guess a number between 0 and %d: " % currentlevel.cap)      
    if currentlevel.check_number(guess) == True:
        x += 1 #bumps the index up for levels
        if x >= len(levels):
            print "\n\n\n\n CONGRATS! YOU WIN THE GAME!" #If you win the last       level,  you win the game
            running = 0 #game stops
        else:
            currentlevel = levels[x] #If not, go to the next level
            print "\n\n Level", currentlevel.level, "\n\n" #Show current level

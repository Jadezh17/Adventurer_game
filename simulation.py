import sys
from room import Room
from adventurer import Adventurer
from item import Item
from quest import Quest

#Calling the Adventurer Class
adv = Adventurer()

pSource ="p"
iSource ="i"

paths = []
rooms = []
items = []
quests =[]

#Calling the reading congfig files
def main(pathSource, itemSource, questSource):

    global pSource 
    pSource = pathSource
    global iSource 
    iSource = itemSource
    global qSource
    qSource = questSource
    currentRoom = None
    
#Checking that there is 3 configuration files else print error and quit
if (len(sys.argv) < 4):
    print("Usage: python3 simulation.py <paths> <items> <quests>")
    exit()
#puts the three config file into the main function 
else:    
    x = main(sys.argv[1],sys.argv[2],sys.argv[3])    

# function opens the paths config file , reading each path and adding to list paths
def read_paths(source):
    try:
        read =  open(source,"r")

        while True:
            line = read.readline()
            if len(line) >0:
                path = line.strip("\n").split(">")
                paths.append(path)
            else:
                break
        read.close()
            
    except:
        return
    return paths


#read each path creating each room paths
def create_rooms(paths):
    i = 0 
    while i < len(paths):
        x = paths[i][0].strip(" ")
        d = paths[i][1].strip(" ")
        y = paths[i][2].strip(" ")
        i+=1
        
        roomExist = False
        #Check start room name in path config file aginst available rooms list
        m = 0 
        while m < len(rooms):
            room = rooms[m]
            if (room.name == x):
                room.set_path(d,y)
                roomExist = True 
            m+=1
         #if no start room found, create new room and add into rooms list        
        if (not roomExist):
            #create new room object
            newRoom = Room(x)
            #add new path to the room
            newRoom.set_path(d,y)
            #add new room into current room list
            rooms.append(newRoom)    
        endRoomExist = False
        b = 0 
        while b < len(rooms):
            room = rooms[b]
            if (room.name == y):
                endRoomExist = True
            b+=1
        
        #if no start room found, create new room and add into rooms list        
        if (not endRoomExist):
            #create new room object
            newRoom = Room(y)
            #Skip path for End room with no destination
            rooms.append(newRoom)
    return rooms

#reads fromt the item config file, getting each attribute of Items class
def generate_items(source): 
    try:
        read = open(source,"r")
        while True:
            line = read.readline()
            if (len(line))>0:
                line = line.strip("\n").split("|")
                name = line[0].strip()
                short = line[1].strip()
                skill_bonus = line[2].strip()
                will_bonus = line[3].strip()
                item = Item(name, short, skill_bonus, will_bonus)
                items.append(item)
            else:
                break
        read.close()
    except:
        return
    return items

#Open the quests config file getting each attribute of quests class
def generate_quests(source, items, rooms):
    try:
        
        read = open(source,"r")
        while True:
            lines = read.readline()
            if not lines.strip() and len(lines)>0:
                continue
            elif len(lines)>0:
                questList = lines.strip("\n").split("|")
            else:
                break

            reward = questList[0].strip()
            action = questList[1].strip()
            desc = questList[2].strip()
            before = questList[3].strip()
            after = questList[4].strip()
            req = questList[5].strip()
            fail_msg = questList[6].strip()
            pass_msg = questList[7].strip()
            room = questList[8].strip()

            if len(questList) >0:
                quest = Quest(reward, action, desc, before, after, req, fail_msg, pass_msg, room)
                quests.append(quest)  
        read.close()
        return quests
    
    except:
        return

#Calling the function
read_paths(pSource)
create_rooms(paths)
generate_items(iSource)
generate_quests(qSource,items,rooms)

# Initially set quest from configure file to relevant room
m = 0 
while m < len(quests):
    quest = quests[m]
    j = 0 
    while j < len(rooms):
        room = rooms[j]
        if (room.name == quest.get_room_desc()):  
            room.set_quest(quest)
            break 
        j +=1
    m+=1            

#Error Catching, testing each config file is valid and openable
try: 
    x = open(sys.argv[1],"r")
    y = open(sys.argv[2],"r")
    z = open(sys.argv[3],"r")
except:
    print("Please specify a valid configuration file.")
    exit()
if len(paths) <1:
    print("No rooms exist! Exiting program...")
    exit()
#closing files
x.close()
y.close()
z.close()


#Set first room and draw it at the beginning of program
if (len(rooms)>0):
    currentRoom = rooms[0]
    currentRoom.draw()
    roomQuest = currentRoom.get_quest()
    if (roomQuest) != None and (roomQuest.completed == False) and currentRoom == rooms[0]:
        print(roomQuest.before + "\n") 
try:
    while True:
    #waiting for user instruction to move
        i = input(">>> ")
        i = i.upper()
        # allows adventurer to type both N and North 
        if (i == "N" or i == "NORTH"):
            i = "NORTH"
        elif (i == "S" or i=="SOUTH"):
            i = "SOUTH"
        elif (i == "W" or i =="WEST"):
            i = "WEST"
        elif (i == "E" or i =="EAST"):
            i = "EAST"
        #When a quests is completed it can't be completed again
        elif (currentRoom.quest != None and i == currentRoom.quest.action):
            if currentRoom.quest.completed == True:
                 print("You have already completed this quest.\n")
            #if quest not completed but adventurer cannot complete it due to skill/will levels print fail
            elif (not currentRoom.quest.attempt(adv)): 
                 print(currentRoom.quest.fail_msg + "\n")
            #if adventurer can attempt and Adventurer input matches quest action quest completed
            else:
                print(currentRoom.quest.pass_msg + "\n")
                currentRoom.quest.completed = True
                currentRoom.quest.desc = currentRoom.quest.desc + " [COMPLETED]"
                #matching the reward from the quest with item object
                m = 0 
                while m < len(items):
                    if (currentRoom.quest.reward == items[m].name):
                        adv.take(items[m])
                        break      
                    m+=1
                       
            
        elif i == "CHECK":
            x = input("Check what? ")
            m = x.upper()
            print("")
            if m =="ME":
                adv.check_self()      
            if m != "ME":
                #allows the adventurer input to be case insensitive and checks if item in adventurers inventory
                m = 0                
                while m < len(items):
                    if ((x.upper() == items[m].name.upper()) or (x.upper() == items[m].short.upper())):  
                        print(items[m].name)
                        print("Grants a bonus of " + items[m].skill_bonus + " to SKILL.")
                        print("Grants a bonus of " + items[m].will_bonus + " to WILL.")
                        print()
                        print()
                        break
                    m+=1
                #if object not in inventory 
                else:
                    print("You don't have that!\n")
        #checking quest completed
        elif i =="QUESTS":
            i = 0
            countCompleted = 0
            while i < len(quests):
                quest = quests[i].completed
                inital = "#" + str(0)+str(i) + ": "
                string = quests[i].reward
                desc = "{:<20}".format(string)
                print(inital + desc + " - "+ quests[i].desc)
                if quest == True:
                    countCompleted += 1
                i+=1
            #if all quest completed seen through the countCompleted 
            if (countCompleted == len(quests)):
                print()
                message = "=== All quests complete! Congratulations! ===".rstrip()
                print(message)
                break
            else:
                print()
         #if adventurer input quit
        elif i == "QUIT":
            print("Bye!")
            exit()
        #if adventurer inputs help , opens help file.txt
        elif i == "HELP":
            x= open ("list.txt","r")
            while True:
                lines = x.readline()
                if len(lines) > 0:
                    line = lines.rstrip("\n\r")
                    print(line)
                else:
                    break
            x.close()
        #look draws current room and check if quest completed or not
        elif i == "LOOK" or i == "L":
            # Response to LOOK command
            currentRoom.draw()
            #print(currentRoom.quest.is_complete())
            if (not currentRoom.quest == None):      
                if (currentRoom.quest.is_complete()):
                    print(currentRoom.quest.after + "\n")
            
                else:
                    print(currentRoom.quest.before + "\n")
        #prints a list of what is in the adventurer's inventory
        elif i == "INV":
            #response to Inventory command
            print("You are carrying:")

            if len(adv.inventory)==0:
                print("Nothing.\n")
            else:
                m = 0 
                while m < len(adv.inventory):
                    print("- A " + adv.inventory[m].name )
                    m+=1
                print()         

        else:
            print("You can't do that.\n")
            
        
        #if user input is dirction value, then process move action
        if (i == "NORTH" or i == "WEST" or i == "SOUTH" or i == "EAST"):   
            valid = False 
            m = 0 
            while m < len(currentRoom.paths):
                path = currentRoom.paths[m]
                if path["dir"] == i:
                    valid = True
                    break
                else:
                    m+=1
            if(valid): 
                #return new room name after move from current room
                newRoom = currentRoom.move(i)          

                #check new room in current rooms list by name to get new room object
                if (newRoom != None):
                    n = 0 
                    while n < len(rooms):
                        room = rooms[n]
                        if (newRoom == room.name):
                            currentRoom = room
                            #once new room is found, draw it
                            print("You move to the {}, arriving at the {}.".format(i.lower(),newRoom))
                            currentRoom.draw()
                            roomQuest = currentRoom.get_quest()
                            
                            if (roomQuest) != None:
                                if (roomQuest.completed == False):
                                    print(roomQuest.before)
                                    print()
    
                                else:
                                    print(roomQuest.after)
                                    print()
                            #stop search room once found
                            break 
                        else:
                            n+=1 
            else:
                print("You can't go that way.\n")           
except:   
    exit()



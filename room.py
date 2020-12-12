class Room:
    
    def __init__(self, name):
        self.name = name
        self.quest = None
        
        self.north = "-"
        self.west = "|"
        self.south = "-"
        self.east = "|"
        self.paths = []

    def get_name(self):
        return self.name
    def get_short_desc(self):
        return self.south
    def get_quest_action(self):
        pass
    def set_quest(self, quest):
        if (quest != None):
            self.quest = quest
    def get_quest(self):
        return self.quest
    def set_path(self, dir, dest):
        if self.paths == 0:
            return "No rooms exist! Exiting program..."
        else:
            path = {"dir":dir, "dest":dest}
            self.paths.append(path)
                
            if (dir == "NORTH"):
                self.north = "N"
            elif (dir == "WEST"):
                self.west = "W"
            elif (dir == "SOUTH"):
                self.south = "S"
            elif (dir == "EAST"):
                self.east = "E"
            
    def move(self, dir):
        if (dir == "N" or dir =="NORTH"):
            dir = "NORTH"
        elif (dir == "S" or dir == "SOUTH"):
            dir = "SOUTH"
            #print("You move to the south, arriving at the {}.".format(self.name))
        elif (dir == "W" or dir == "WEST"):
            dir = "WEST"
        elif (dir == "E" or dir == "EAST"):
            dir = "EAST"
        #search current paths list to find valid destination by direction
        i = 0 
        while i < len(self.paths):
            p = self.paths[i]
            if (p["dir"] == dir):
                return p["dest"]
            else:
                i+=1
                continue
        

    def draw(self):
        print('')
        print("+---------"+self.north+self.north+"---------+")
        print("|                    |")
        print("|                    |")
        print("|                    |")
        print("|                    |")
        print(self.west+"                    "+self.east)
        print("|                    |")
        print("|                    |")
        print("|                    |")
        print("|                    |")
        print("+---------"+self.south+self.south+"---------+")
        print("You are standing at the {}.".format(self.name))
        if self.name == "Test Room":
            print("There is nothing in this room.")
        elif self.get_quest() == None:
            print("There is nothing in this room.\n")

     

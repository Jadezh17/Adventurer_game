class Quest:
    def __init__(self, reward, action, desc, before, after, req, fail_msg, pass_msg, room):
        self.reward = reward
        self.action = action
        self.desc = desc
        self.before = before
        self.after = after
        self.completed = False
        self.requirement = {"SKILL":0,"WILL":0}
        
        requirements = []
        if (req.find(",")>-1):
            requirements = req.split(",")
        else:
            requirements.append(req)       
        skill = 0
        will = 0

        i = 0 
        while i < len(requirements):
            r = requirements[i]
            if (r.find("SKILL")>-1):
                skill = r.strip("SKILL").strip()
            elif (r.find("WILL")> -1):
                will = r.strip("WILL").strip()
            i+=1
        self.requirement = {"SKILL":skill,"WILL":will}
        self.fail_msg = fail_msg
        self.pass_msg = pass_msg
        self.room = room

    def get_info(self):
        return self.desc
    def is_complete(self):
        return self.completed
    #self.completed
		#"""TODO: Returns whether or not the quest is complete."""

    def get_room_desc(self):
        return self.room
        #"""TODO: Returns a description for the room that the quest is currently in. Note that this is different depending on whether or not the quest has been completed.""" 
    def get_action(self):
        return self.action
	#"""TODO: Returns a command that the user can input to attempt the quest."""
		
		
    def attempt(self, player):        
        if (player.get_skill() >= int(self.requirement["SKILL"]) and
           player.get_will() >= int(self.requirement["WILL"])):
            return True
        else:
            return False
#         #"""TODO: Allows the player to attempt this quest.

#         #Check the cumulative skill or will power of the player and all their items. If this value is larger than the required skill or will threshold for this quest's completion, they succeed and are rewarded with an item (the room's description will also change because of this).
    
#         #Otherwise, nothing happens."""


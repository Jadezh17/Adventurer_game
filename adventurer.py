class Adventurer:
    
    def __init__(self):
        self.inventory = []
        self.will_power = 5
        self.skill_power = 5
        self.total_skill = 5
        self.total_will = 5
    def get_inv(self):
        return self.inventory
        
    def get_skill(self):
        # self.skill_level = 5
        if self.total_skill < 0:
            self.total_skill = 0
        return self.total_skill

    def get_will(self):
        # self.will_power = 5
        if self.total_will <0:
            self.total_will = 0

        return self.total_will
    
        """TODO: Returns the adventurer's will power. Whether this value is generated before or after item bonuses are applied is your decision to make."""
        #1. linked with item in inventory(will_bonus)
    def take(self, item):
        self.inventory.append(item)
        self.total_skill += int(item.get_skill())
        self.total_will += int(item.get_will())

        return self.inventory
    def check_self(self):
        print("You are an adventurer, with a SKILL of {} and a WILL of {}.".format(self.skill_power,self.will_power))
        print("You are carrying:\n")
        if len(self.inventory) == 0:
            print("Nothing.\n")
            print("With your items, you have a SKILL level of {} and a WILL power of {}.".format(self.will_power,self.skill_power))
            print()
        else:
            
            m = 0
            while m < len(self.inventory):
                print(self.inventory[m].name)
                print("Grants a bonus of {} to SKILL.".format(self.inventory[m].get_skill()))
                print("Grants a bonus of {} to WILL.\n".format(self.inventory[m].get_will()))
                m+=1
            
            if self.total_skill <0:
                self.total_skill = 0
            if self.total_will <0:
                self.total_will = 0

            print("With your items, you have a SKILL level of {} and a WILL power of {}.\n".format(self.total_skill,self.total_will))
                

              

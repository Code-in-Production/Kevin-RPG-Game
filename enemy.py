from random import uniform

class Enemy:
    def __init__(self, hp, dps, rnge=0):
        self.hp = hp
        self.dps = dps
        self.rnge = rnge

    def attack(self):
        return uniform(self.dps-self.rnge, self.dps+self.rnge)

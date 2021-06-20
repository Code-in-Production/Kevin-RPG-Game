from random import sample

from enemy import Enemy

class Game:
    def __init__(self):
        self.level = 0  # 0 levels 1 to 9, then 10 as the boss fight
        self.can_move_on = True

        # Will be shuffled
        self.leveltypes = sample([0, 0, 0, 0, 1, 1, 2, 2, 2], 9)  # 0 enemy, 1 merchant, 2 random events
        # self.leveltypes = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.leveltypes.append(0)  # For the boss
        self.curr_lvltype = -1

        # Enemies
        self.enemies = [Enemy(25, 5), Enemy(75, 10), Enemy(50, 25, 25), Enemy(250, 5, 5), Enemy(500, 50)]
        self.enemyidx = -1
        self.curr_enemy = None

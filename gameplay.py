from random import randint, random

from discord.ext import commands

from game import Game
from ship import Ship
# from event import Event

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = Game()
        self.ship = Ship()

    """ LEVEL PROGRESSION """
    @commands.command()
    async def hyperdrive(self, ctx):
        # Cannot move on, stay on the level lol
        if not self.game.can_move_on:
            await ctx.send("Fight the enemy you noob")
            return

        # must defeat the enemy if you want to use
        if self.game.level == 10:
            await ctx.send("GGEZ. `;hyperdrive` to start a new journey")
            self.reset()
            return

        # self.game.can_move_on = True
        self.game.level += 1
        self.game.curr_lvltype = self.game.leveltypes[self.game.level-1]

        if self.game.curr_lvltype == 0:
            self.game.enemyidx += 1
            self.game.curr_enemy = self.game.enemies[self.game.enemyidx]
            await ctx.send(f"Enemy approaching! This one has {self.game.curr_enemy.hp} hp and averages {self.game.curr_enemy.dps} damage per shot")
            self.game.can_move_on = False
            # create enemy
        elif self.game.curr_lvltype  == 1:
            await ctx.send("You bumped into a space merchant, feel free to sell any scrap for tools `;sell [amount]`")
        elif self.game.curr_lvltype  == 2:
            idx = randint(0, 3)

            if idx == 0:  # Bad
                await ctx.send("You ran into some pirates and was barely able to make it away at the cost of your cannon. It now deals half damage.")
                self.ship.cannon /= 2
            elif idx == 1:  # Good
                await ctx.send("Some wandering nomads were kind enough to fix your ship. Enjoy a 50 HP gain.")
                self.ship.hp += 50
            elif idx == 2:  # Bad
                await ctx.send("The engineer forgot to close a hatch, causing you to lose some scrap")
                self.ship.scrap = max(0, self.ship.scrap-50)
            elif idx == 3:  # Good
                await ctx.send("You discovered some ancient remnants of a civilization on a small moon and scavenged the ruines, gaining some scrap")
                self.ship.scrap += 500

            await ctx.send("`;hyperdrive` to move along")

    """ ENCOUNTERING ENEMY """
    @commands.command()
    async def use(self, ctx, weapon: str):
        if self.game.curr_lvltype != 0:
            await ctx.send("You can only use this command when fighting enemies")
            return

        if self.game.curr_enemy.hp == 0:
            await ctx.send("The enemy is already dead. No point in beating a dead horse. `;hyperdrive` to move on")
            return

        # print(ctx.command, type(ctx.command), str(ctx.command))
        if weapon == "laser":  # laser with 5% crit chance
            dmg_to_enemy = self.ship.laser*self.ship.dmg_boost/100 + 100*(random() <= 0.05)
        elif weapon == "cannon":  # cannon is average
            dmg_to_enemy = self.ship.cannon*self.ship.dmg_boost/100
        elif weapon == "rocket":  # decreases player hp by 10%
            await ctx.send("The rocket's power decreased your HP by 10%")
            self.ship.hp *= 0.9
            dmg_to_enemy = self.ship.rocket*self.ship.dmg_boost/100
        else:
            await ctx.send("Thats not a valid weapon")
            return

        self.game.curr_enemy.hp = max(0, self.game.curr_enemy.hp-dmg_to_enemy)
        await ctx.send(f"You dealt {dmg_to_enemy} damage to the enemy, leaving them at {self.game.curr_enemy.hp} HP")
        
        # Enemy dies
        if self.game.curr_enemy.hp == 0:
            loot = self.game.enemyidx
            self.ship.tools += loot
            self.game.can_move_on = True
            await ctx.send(f"You have defeated the enemy and won {loot} tools. `;hyperdrive` to move on.")
            return

        # Enemy attacks back
        print(self.game.curr_enemy)
        dmg_to_player = self.game.curr_enemy.attack()
        self.ship.hp = max(0, self.ship.hp-dmg_to_player)
        await ctx.send(f"Enemy dealt {dmg_to_player} damage, leaving you with {self.ship.hp} HP.")

        if self.ship.hp == 0:
            self.reset()
            await ctx.send(f"You died, game over. `;hyperdrive` to restart at level 1.")
   
    """ ENCOUNTERING MERCHANT """
    @commands.command()
    async def sell(self, ctx, value: int):
        # Not at a merchant
        if self.game.curr_lvltype != 1:
            await ctx.send("You can only use this command when trading when a merchant")
            return

        # Too poor
        if value > self.ship.scrap or value < 0:
            await ctx.send("You cannot sell your proposed amount of scrap")
            return

        self.ship.scrap -= value
        self.ship.tools += value // 10
        await ctx.send(f"{value} scrap sold for {value//10} tools. You now have {self.ship.scrap} scrap and {self.ship.tools} tools.")
        ...

    """ REPAIRING SHIP """
    @commands.command()
    async def boosthp(self, ctx):
        # 1 tool increases hp by 25
        if self.ship.tools <= 0:
            await ctx.send("No more tools. You cannot increase the ship's HP")
            return
        
        self.ship.hp += 25
        self.ship.tools -= 1
        await ctx.send(f"Used a tool to boost the ship's HP to {self.ship.hp}")

    @commands.command()
    async def boostdamage(self, ctx):
        # 1 tool increase hp by 25%
        if self.ship.tools <= 0:
            await ctx.send("No more tools. You cannot boost the ship's damage")
            return

        self.ship.dmg_boost += 10
        self.ship.tools -= 1
        await ctx.send(f"Used a tool to boost the ship damage to {self.ship.dmg_boost}%")

    @commands.command()
    async def me(self, ctx):
        await ctx.send(f"\
            HP: {self.ship.hp}\
            \nScrap: {self.ship.scrap}\
            \nTools: {self.ship.tools}\
            \nLaser damage: {self.ship.laser*self.ship.dmg_boost/100:.1f}\
            \nCannon damage: {self.ship.cannon*self.ship.dmg_boost/100:.1f}\
            \nRocket damage: {self.ship.rocket*self.ship.dmg_boost/100:.1f}\
        ")

    def reset(self):
        self.game = Game()
        self.ship = Ship()

    # @commands.command()
    # async def a(self, ctx):
    #     await ctx.send(f"{ctx.command}")
    #     await ctx.send(f"{self.ship.__dict__}")
    #     ...
    
    # @commands.command()
    # async def s(self, ctx):
    #     await ctx.send(f"{self.game.__dict__}")

def setup(bot):
    bot.add_cog(Test(bot))

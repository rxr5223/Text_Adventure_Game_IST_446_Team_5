import random
import items, enemies, actions, world, sys, time, random
 
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def intro_text(self):
        raise NotImplementedError()
 
    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves
 
    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.Heal())
        moves.append(actions.Quit())
 
        return moves


class StartingRoom(MapTile):
    # Method to print slow texts
    def print_slow(str):
        for letter in str:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(0.010)

    print_slow("""
        -------------------------------------------------------------------
        |                                                                  |
        |                                                                  |
        -------------------------------------------------------------------
        """)
    # override the intro_text method in the superclass
    def intro_text(self):
        return """
        -------------------------------------------------------------------
        | You find yourself in a cave with a flickering torch on the wall. |
        | You can make out four paths, each equally as dark and foreboding.|
        -------------------------------------------------------------------
        """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

class ColdRoom(MapTile):
    def intro_text(self):
        return """
        A freezing breathe of air flows through you. You feel your bones chill.
        """

    def modify_player(self, player):
        player.bodyTemp -= 10

class LootRoom(MapTile):
    def __init__(self, x, y, item, beenThere):
        self.item = item
        self.beenThere = False
        super().__init__(x, y)

    def add_loot(self, player):
        if(self.beenThere == False):
            player.inventory.append(self.item)
            self.beenThere = True

 
    def modify_player(self, player):
        self.add_loot(player)

class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)
 
    def modify_player(self, the_player):
        if self.enemy.is_alive():
            hit = random.randint(1,3)
            if hit >= 2:
                the_player.hp = the_player.hp - self.enemy.damage
                print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))
            else:
                print("Enemy misses their attack.")

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Attack(enemy=self.enemy), actions.Flee(tile=self)]
        else:
            return self.adjacent_moves()

class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """
 
    def modify_player(self, player):
        #Room has no action on player
        pass
 
class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())
 
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """
 
class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger(), beenThere = False )
 
    def intro_text(self):
        if(self.beenThere == False):
            return """
            Your notice something shiny in the corner.
            It's a dagger! You pick it up.
            """
        else:
            return"""
            There is nothing there
            """

class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """
 
    def modify_player(self, player):
        player.victory = True

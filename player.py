import random
import items, world
 
class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Pillow(), items.MedicalPack()]
        self.hp = 100
        self.maxHP = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False
 
    def is_alive(self):
        return self.hp > 0
 
    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')

    def heal(self):
        for i in self.inventory:
         if isinstance(i, items.Health):
            if self.hp < self.maxHP:
                if i.uses > 0:
                    i.uses = i.uses - 1
                    self.hp = self.hp + 5
                    if self.hp > self.maxHP:
                        self.hp = self.maxHP
                    print("Your HP was restored to", self.hp)
                else:
                    print("You have no medical supplies left.")
            else:
                print("Your HP is at max.")
    
    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())
 
    def move_north(self):
        self.move(dx=0, dy=-1)
 
    def move_south(self):
        self.move(dx=0, dy=1)
 
    def move_east(self):
        self.move(dx=1, dy=0)
 
    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
         if isinstance(i, items.Weapon):
            if i.damage > max_dmg:
                max_dmg = i.damage
                best_weapon = i
 
        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        hit = random.randint(1,20)
        if hit > 5 and hit <= 15:
            print("You hit for {} damage!".format(best_weapon.damage))
            enemy.hp -= best_weapon.damage
        elif hit > 15:
            print("You hit critically for {} damage!!!".format(best_weapon.damage * 2))
            enemy.hp -= (best_weapon.damage * 2)
        else:
            print("Your attack missed")

        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def flee(self, tile):
        """Moves the player randomly"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves))
        self.do_action(available_moves[r])

    def quit (self):
        print("You quit the game!")
        self.hp = 0

    def do_action(self, action, **kwargs):
     action_method = getattr(self, action.method.__name__)
     if action_method:
                action_method(**kwargs)


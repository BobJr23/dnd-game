import random, json

hit_list = []

theif_state = "Sneak"


def show_spells(issneak):
    if issneak:
        issneak = "Backstab"
    else:
        issneak = "Sneak"
    return {
        "Warrior": "1:Basic 2:Pound",
        "Thief": f"1:Basic 2:{issneak}",
        "Wizard": "1:Basic 2:Magic_Missle",
        "Cleric": "1:Basic 2:Heal",
    }


weapons = {
    "club": ["1d4", 5],
    "greatclub": ["1d8", 15],
    "mace": ["1d6", 10],
    "wand": ["1d4", 5],
    "dagger": ["1d4", 5],
    "greatsword": ["1d10", 25],
    "axe": ["2d6", 30],
    "Nunchucks": ["2d4", 25],
}
classes = ["Warrior", "Wizard", "Cleric", "Thief"]
# DICE ROLLING
def roll_dice(sides, times=1):
    if type(sides) == list:
        sides, times = sides
    summ = 0
    for _ in range(int(times)):
        summ += random.randint(1, int(sides))
    return summ


def creation_dice():
    su = []
    for _ in range(4):
        su.append(random.randint(1, 6))

    return sum(su) - min(su)


# BASE PLAYER
class Player:
    def __init__(self, name, clas, gold):
        self.name = name
        self.clas = clas
        self.melee = True
        self.dmg = "1d4"
        self.inv = []
        self.hp = 10
        self.gold = gold
        self.maxhp = 10
        self.sneak = False
        self.str = creation_dice()
        self.dex = creation_dice()
        self.con = creation_dice()
        self.int = creation_dice()
        self.wis = creation_dice()
        self.cha = creation_dice()

    def get_stats(self):
        dic = vars(self)
        print("")
        for key, val in dic.items():
            print(key, "is", val)


# PARTY
class Party:
    def __init__(self):
        self.p1 = player1
        self.p2 = player2
        self.p3 = player3
        self.p4 = player4


class Monster:
    def __init__(self, hp, num_dice, damage, damage_mod, armor, name):
        self.hp = hp
        self.num = num_dice
        self.damage = damage
        self.damage_mod = damage_mod
        self.armor = armor
        self.name = name


# CREATE PLAYER OBJECTS
def create_player(num):
    player_class = 5
    player_name = input(f"What is player {num}'s name? ")
    while not player_class in range(1, 5):

        try:
            player_class = int(input(f"Which class do you want(number)? {classes}"))
        except:
            pass
    player = Player(player_name, classes[player_class - 1], roll_dice(6, 4) * 10)
    return player


player1, player2, player3, player4 = (
    create_player(1),
    create_player(2),
    create_player(3),
    create_player(4),
)
party = Party()
print(vars(party), "\n")


def show_stats(lst=[player1, player2, player3, player4]):
    for x in lst:
        x.get_stats()


def basic_hit(player):
    damage = roll_dice(player.dmg[2], player.dmg[0])
    return damage + (player.str - 10) // 2


def wizard_attacks(player):
    # MAGIC MISSLE
    return 3, 50


def warrior_attacks(player):
    # POUND

    taken = roll_dice(6)
    player.hp -= taken
    print(
        player.name,
        "delt",
        taken,
        "damage to himself. They are now at",
        player.hp,
        "health",
    )
    if player.hp <= 0:
        return "dead"
    else:
        return (
            roll_dice(*[int(x) + 1 for x in player.dmg.split("d")])
            + (player.str - 10) // 2,
            roll_dice(20, 1) + (player.str - 10) // 2,
        )


def thief_attacks(player):
    if player.sneak:
        num, dam = [int(x) for x in player.dmg.split("d")]
        damage = roll_dice(num, dam)
        player.sneak = False
        return damage * 2 + (player.str - 10) // 2, 50
    else:
        player.sneak = True
        return 0, -1


def cleric_attacks(player):
    part_list = list(vars(party).values())
    healed = int(
        input(
            f"Which character do you want to heal (1-4){[player1.name, player2.name, player3.name, player4.name]}"
        )
    )
    x, y = [int(x) + 1 for x in player.dmg.split("d")]
    headled_player = part_list[healed - 1]
    gained = roll_dice(x, y)
    if headled_player.hp + gained > headled_player.hp:
        gained = headled_player.maxhp - headled_player.hp
        headled_player.hp = headled_player.maxhp
    else:
        headled_player.hp += gained
    print(
        headled_player.name,
        "gained",
        gained,
        "health.",
        "They are now at",
        headled_player.hp,
        "health.",
    )
    return -1, -1


def player_attack(player, monster):
    p_class = player.clas
    attack_spells = show_spells(player.sneak)
    attack_num = int(
        input(
            f"Do you want to do {' or '.join(attack_spells[p_class].split())} (number)"
        )
    )

    # BASIC WEAPON ATTACK
    match attack_num:
        case 1:

            attack_roll = roll_dice(20, 1) + (player.str - 10) // 2
            if attack_roll >= monster.armor:

                tot_dam = basic_hit(player)
                monster.hp -= tot_dam
                print(f"You dealt {tot_dam} damage to the monster")
            else:
                print("You missed your attack!")
        case 2:
            print("You did", attack_spells[p_class])
            match p_class:
                case "Warrior":
                    damage, ac = warrior_attacks(player)
                case "Wizard":
                    damage, ac = wizard_attacks(player)
                case "Cleric":
                    damage, ac = cleric_attacks(player)
                case "Thief":
                    damage, ac = thief_attacks(player)
            try:
                if ac < 0:
                    ...
                elif ac < monster.armor:
                    print("You missed!")
                else:
                    monster.hp -= damage
                    print(f"You dealt {damage} damage to the monster")
            except TypeError:
                print("d")
    return theif_state


def fight_monster(monsters):

    players = list(party.__dict__.values())

    objects = monsters + players
    while len(monsters) > 0:
        for object in objects:
            if object.__class__.__name__ == "Player":
                player_attack(object)
            else:
                monster_attack(object)

        def player_attack(player):
            z = [monster.name for monster in monsters]
            if len(z) == 0:
                return
            print(f"It is {player.name}'s turn. Which monster do you want to attack?\n")

            monster = monsters[int(input(z)) - 1]
            # ATTACK!
            player_attack(player, monster)
            # CHECK IF DEAD
            if monster.hp > 0:
                print(f"the monster has {monster.hp} health left")
            else:
                print("The monster is dead!")
                monsters.remove(monster)

        def monster_attack(monster):
            attacked = random.choice(list(players))
            print(f"It is {monster.name}'s turn. They attack {attacked.name}.\n")

            mons_dam = roll_dice(monster.damage, monster.num)
            attacked.hp -= mons_dam
            if attacked.hp > 1:
                print(
                    f"{attacked.name} took {mons_dam} damage. They are now at {attacked.hp} hp!"
                )
            else:
                print(
                    f"{attacked.name} took {mons_dam} damage. They are now unconcious"
                )
                players.remove(attacked)


show_stats()
# JSON FILE OPENING
f = open(r"C:\Users\maand\OneDrive\CodingProjects\DND GAME\dndstory.json")
story = json.loads(f.read())
m = open(r"C:\Users\maand\OneDrive\CodingProjects\DND GAME\dndmonsters.json")
monster_json = json.loads(m.read())


def shop():
    for key, val in weapons.items():
        print(f"{key}: {val[0]} damage. Price is {val[1]} gold")


def tavern(completed=0):
    x = int(
        input(
            "\n"
            + "You walk into a tavern, and you see 4 people. Who do you walk up to? (1. Dwarf)"
        )
    )
    match x:
        case 1:
            c1 = int(
                input(
                    "You walk up to the dwarf, and he tells you about the goblins attacking their miners. He promises good money to get rid of them, extra if you bring one back alive.(1:Accept or 2:Decline)"
                )
            )
            if c1 == 2:
                tavern()
            else:
                choicee = -1
                decision = "decision1"
        case 2:
            ...
        case 3:
            ...

    def get_choice(choicee, decision):
        if len(story[decision][1]) > 0:
            lst = []
            monster_name = 1
            for x in story[decision][1]:
                lst.append(Monster(*monster_json[x], f"{x}{monster_name}"))
                monster_name += 1
            fight_monster(lst)
            print(
                story[decision][2][3],
                "\n",
                story[decision][2][0][0],
                "\nor\n",
                story[decision][2][1][0],
                "\n",
            )
        else:
            print(
                story[decision][0],
                "\n",
                story[decision][2][0][0],
                "\nor\n",
                story[decision][2][1][0],
                "\n",
            )
            choicee = int(input()) - 1
            decision = story[decision][2][choicee][1]

        return decision

    while True:
        decision = get_choice(choicee, decision)


tavern()

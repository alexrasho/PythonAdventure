import random
import copy
import time

class hero():
    gold = 5
    strength = 2
    hp = 20
    armor = 0
    maxHp = 20
    mp = 1
    maxMp = 1
    inventory = [1]    #Amount of certain items

class monster():
    def __init__(self, name , hp, strength, armor, gold):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.armor = armor
        self.gold = gold
 #   mp = ''
#   HasAbility = []

monsters = [monster("Goblin", 10, 1, 0, 5), monster("Jerry Smith", 1, 1, 0, 9999)]
#enemy1 = monster[1]

class item():
    def __init__(self, name, type, potency):
        self.name = name
        self.type = type
        self.potency = potency

items = [item("Potion", "Heal", 10)]

#Abilities = {}

class ability():
    def __init__(self, name, type, magnitude, duration, mpCost, message):
        self.name = name
        self.type = type
        self.magnitude = magnitude
        self.duration = duration
        self.mpCost = mpCost
        self.message = message
        
abilities = [ability("Weaken", "Damage", 1, 4, 1, "The monster is weakened!")]
abilityUsed = None
abilityDuration = 0

def wait():
    input("\nPress Enter to continue...\n")

def run():
    if(random.randint(1,4) == 1):
        return 1
    else:
        print("\nYou try to escape... but fail!")
        return 0

def attack(enemyHp, hero):
    damage = random.randint(hero.strength + 1, hero.strength + 3)
    enemyHp -= damage
    print("\nYou strike for", damage, "damage!")
    return enemyHp

def useitem(hero, monster):
    print("\nITEM LIST\n1 . Back")
    for x in range(0, len(items)):
        if(hero.inventory[x] != 0):
            print((x + 2), ". " + items[x].name)
    print()
    command = int(input("Press the corresponding number to choose your option.\nCHOICE: "))
    if(hero.inventory[command - 2] != 0 and command != 1):
        hero.inventory[command - 2] -= 1
        if(items[command - 2].type == "Heal"):
            hero.hp += items[command - 2].potency
            if(hero.hp > hero.maxHp):
                hero.hp = hero.maxHp
            print("\nThe " + items[command - 2].name + " heals you for", items[command - 2].potency, "hp!")
        elif(items[command - 2].type == "Damage"):
            monster.hp -= items[command - 2].potency
            print("\nThe " + items[command - 2].name + " damages the " + monster.name + " for", items[command - 2].potency, "damage!")
    elif(command == 1):
        return 1
    else:
        print("Invalid option")
        
def useAbility(hero, monster, continueflag):
    global abilityDuration
    global abilityUsed
    if (continueflag == 1):
        if(abilityUsed.type == "Damage"):
            monster.hp -= abilityUsed.magnitude
            print("\nYour ability", abilityUsed.name, "damages the " + monster.name + " for", abilityUsed.magnitude , "damage!\n")
            if (abilityDuration == 1):
                print("The duration of your ability has exhausted!\n")
            else:
                print("Your ability continues for ", abilityDuration-1, "more turns!\n")
            return 0
    if (abilityDuration > 0):
        print("You are already using an ability! It will last for another ", abilityDuration, "turns\n")
        return 1
    if (abilities):
        print("Ability List:\n1 . Back")
        for x in range (0, len(abilities)):
            print(x+2, ".", abilities[x].name)
        abilityChoice = int(input("Press the corresponding number to choose your option\n"))
        if(abilityChoice == 1):
            return 1
        else:
            if(hero.mp >= abilities[abilityChoice-2].mpCost):
                hero.mp -= abilities[abilityChoice-2].mpCost
            else:
                print("You do not have enough MP!\n")
                return 1
            if(abilities[abilityChoice-2].type == "Damage"):
                monster.hp -= abilities[abilityChoice-2].magnitude
                print("\nYour ability", abilities[abilityChoice-2].name, "damages the " + monster.name + " for", abilities[abilityChoice-2].magnitude , "damage!\n")
            if(abilities[abilityChoice-2].duration > 0):
                print("Your ability will continue for ", abilities[abilityChoice-2].duration, "more turns!\n")
        if(abilities[abilityChoice-2].duration > 0):
            abilityDuration = abilities[abilityChoice-2].duration
            abilityUsed = abilities[abilityChoice-2]

def monsterTurn(heroHp, monster):
    damage = random.randint(monster.strength + 1, monster.strength + 3)
    heroHp -= damage
    print(monster.name + " strikes you for", damage, "damage!")
    return heroHp

def combatLoop(hero, monster):
    while(1):
        global abilityDuration
        Back = 0
        print("\nUSER:", hero.hp, "HP ", hero.mp, "MP     THE ENEMY!:", monster.hp, "HP")
        command = input("\nPress the corresponding number to choose your option.\n1. Attack    2. Items    3. Abilities    4. Run\nCHOICE: ")
        if(command == '1' or command == '2' or command == '3' or command == '4'):
            if(command == '1'):
                monster.hp = attack(monster.hp, hero)
                if (abilityDuration > 0):    #continues ability use
                    useAbility(hero, monster, 1)
                    abilityDuration -= 1
                if (monster.hp <= 0):
                    return "win"
            elif(command == '2'):
                Back = useitem(hero, monster)
                if (abilityDuration > 0):    #continues ability use
                    useAbility(hero, monster, 1)
                    abilityDuration -= 1
                if (monster.hp <= 0):
                    return "win"
            elif(command == '3'):
                Back = useAbility(hero, monster, 0)
                if (monster.hp <= 0):
                    return "win"
            elif(command == '4'):
                if(run() == 1):
                    return "run"
                if (abilityDuration > 0):   #continues ability use
                    useAbility(hero, monster, 1)
                    abilityDuration -= 1
                if (monster.hp <= 0):
                    return "win"
            if(Back != 1):
                hero.hp = monsterTurn(hero.hp, monster)
            if hero.hp <= 0:
                return "lose"
        else:
            print("Invalid option")

def combat(hero, monster):
    print("\nINITIATE COMBAT\n\n" + monster.name + " approaches!\nWhat will you do?")
    result = combatLoop(hero, monster)
    if(result == "win"):
        hero.gold += monster.gold
        print("\n" + monster.name + " has been slain!\nYou gain", monster.gold, "gold! GOLD:", hero.gold)
    elif(result == "run"):
        print("\nYou try to escape... and are successful!")
    elif(result == "lose"):
        print("\nOMEGALUL")
    print("\nRESOLVE COMBAT")
    wait()

def intro(hero):
    print("Welcome to the World of Proke Raast!")
    wait()
    print("You are a mildly skilled adventurer who is headed to the main city 'Tar Dhi'. Along the road you run into a stranger who has seemingly appeared from nowhere.")
    wait()
    print("You can see the glint of their beady eyes from the shadows of their hood. Their head suddenly turns toward you and they gesture to you. The stranger's voice croaks as words begin to flow from their lips.")
    wait()
    print("Stranger: You...What do you wish for?")
    wait()
    y = '0'
    while (y != '1') and (y != '2') and (y != '3') and (y != '4'):
        y = input("Press the corresponding number to choose your option.\n1.'I wish for gold'\n2.'I wish for power'\n3.'I wish for health'\n4.'I am content'\nCHOICE: ")
        if y == '1':
            hero.gold += 100
            print("Your pockets feel heavier (+100 gold) \nYour gold:", hero.gold, "\n")
        elif y == '2':
            hero.strength += 2
            print("You feel stronger\nStrength:", hero.strength, "\n")
        elif y == '3':
            hero.maxHp += 5
            hero.hp += 5
            print("You feel vitalized\nMax HP:", hero.maxHp, "\n")
        elif y == '4':
            print("Wow.\n")
        else:
            print("Input a valid number.\n")
    time.sleep(2)
    print("The stranger disappears in a sudden puff of smoke. In the middle of your bewilderment, a monster jumps through the smoke and attacks!")
    combat(hero, copy.copy(monsters[random.randint(0,1)]))
    print("After slaying the monster, you find a note attached to it\n*Join us at the rogue guild and become rich beyond your wildest dreams.*")
    choice = '0'
    while(choice != '1' and choice != '2'):
        choice = input("1. Go to the Rogue Guild\n2. Proceed to the Kingdom\n")
        if(choice == '1'):
            print("You head for the Rogue Guild.")
        if(choice == '2'):
            print("You head for the Kingdom.")
    print("END OF DEMO")

def main():
    bro = hero() 
    intro(bro)

main()
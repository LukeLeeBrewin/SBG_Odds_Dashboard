import numpy as np

# Order of operations is important!
# This is the order in which functions will be applied
def duel_roll_modifiers_dict():
    return {
        "Banner":banner,        
        "2h Weapon":twohandweapon
    }

    

def twohandweapon(dice_rolls):
    print("2h Weapon Function Called")
    dice_rolls = dice_rolls - 1
    return dice_rolls

def banner(dice_rolls):
    print("Banner Function Called")
    num_rolls = len(dice_rolls)
    new_rolls = np.random.randint(1,7, num_rolls)
    for i in range(0,len(dice_rolls)):
        
        if new_rolls[i] > np.min(dice_rolls[i,:]):
            dice_rolls[i,np.argmax(np.min(dice_rolls[i,:]))] = new_rolls[i]

    return dice_rolls



def apply_duel_roll_modifiers(dice_rolls, active_modifiers):
    
    duel_roll_modifiers = duel_roll_modifiers_dict()

    print(f"Active Modifiers {active_modifiers}")
    print(f"Full Modifiers List {list(duel_roll_modifiers.keys())}")
    if active_modifiers is not None:
        for modifier in list(duel_roll_modifiers.keys()):
            if modifier in active_modifiers:
                dice_rolls = duel_roll_modifiers[modifier](dice_rolls)
    return dice_rolls

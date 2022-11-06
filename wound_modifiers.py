import numpy as np



# Order of operations is important!
# This is the order in which functions will be applied
def wound_modifiers_dict():
    return {        
        "Trapped":trapped,
        "+1 To Wound":plusonewound        
    }


def plusonewound(dice_rolls):
    dice_rolls = dice_rolls + 1
    return dice_rolls

def trapped(dice_rolls):
    print("Trapped Function Called")
    print(f"Dice Roll Shape Before: {dice_rolls.shape}")
    num_rolls, num_atks = np.shape(dice_rolls)
    new_rolls = np.random.randint(1,7,(num_rolls, 2*num_atks))
    print(f"Dice Roll Shape After: {new_rolls.shape}")
    return new_rolls



def apply_wound_modifiers(dice_rolls, active_wound_modifiers):
    
    wound_roll_modifiers = wound_modifiers_dict()

    print(f"Active Modifiers {active_wound_modifiers}")
    print(f"Full Modifiers List {list(wound_modifiers_dict().keys())}")
    if active_wound_modifiers is not None:
        for modifier in list(wound_roll_modifiers.keys()):
            if modifier in active_wound_modifiers:
                dice_rolls = wound_roll_modifiers[modifier](dice_rolls)
    return dice_rolls

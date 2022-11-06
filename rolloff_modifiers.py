import numpy as np


# Attacker Modifiers
# Order of operations is important!
# This is the order in which functions will be applied
def atk_rolloff_modifiers_dict():
    return {        
        "Elven Blade":atk_elvenblade      
    }


def atk_elvenblade(rolloff):
    print("Atk Elven Blade Function Called")
    return rolloff-1



# Defender Modifiers
# Order of operations is important!
# This is the order in which functions will be applied
def def_rolloff_modifiers_dict():
    return {        
        "Elven Blade":def_elvenblade      
    }

def def_elvenblade(rolloff):
    print("Def Elven Blade Function Called")
    return rolloff+1






def apply_rolloff_modifiers(rolloff, active_rolloff_modifiers, atk=True):
    
    if atk:
        print("Attacker Roll Off Dictionary Loaded")
        rolloff_roll_modifiers = atk_rolloff_modifiers_dict()
    else:
        print("Defender Roll Off Dictionary Loaded")
        rolloff_roll_modifiers = def_rolloff_modifiers_dict()

        
    print(f"Apply Roll Off Modifier Function Called")
    print(f"Active Modifiers {active_rolloff_modifiers}")
    print(f"Full Modifiers List {list(rolloff_roll_modifiers.keys())}")
    if active_rolloff_modifiers is not None:
        for modifier in list(rolloff_roll_modifiers.keys()):
            if modifier in rolloff_roll_modifiers:
                rolloff = rolloff_roll_modifiers[modifier](rolloff)
    return rolloff
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from fight_modifiers import *
from wound_modifiers import *
from rolloff_modifiers import *

class FightRoller:

    def __init__(self, atk_stats, def_stats, modifiers):
        print("\n\n\n---------------------------------------------------------------------------------------------------")
        print("---------------------------------------------------------------------------------------------------")
        print(f"Init Called")
        print(f"Modifiers:\n{modifiers}\n")

        # Resets modifiers after use (turns into empty list otherwise and breaks things)
        for i in range(0,len(modifiers)):
            if modifiers[i] is not None:
                if len(modifiers[i]) == 0:
                    modifiers[i] = None


        # Rename Modifiers
        self.atk_duel_roll_modifiers = modifiers[0]
        self.atk_rolloff_modifiers = modifiers[1]
        self.atk_wound_modifiers = modifiers[2]


        self.def_duel_roll_modifiers = modifiers[3]
        self.def_rolloff_modifiers = modifiers[4]





        # Attacker Profile
        self.atk_attacks = atk_stats[2]
        self.atk_strength = atk_stats[1]
        self.atk_fv = atk_stats[0]
        
        # Defender Profile
        self.def_attacks = def_stats[2]
        self.def_defence = def_stats[1]
        self.def_fv = def_stats[0]

        # Roll Off Modifiers
        self.roll_off_target = 4 # value required to win the fight if fight values are equal
        self.roll_off_target = apply_rolloff_modifiers(self.roll_off_target, self.atk_rolloff_modifiers, atk=True)
        self.roll_off_target = apply_rolloff_modifiers(self.roll_off_target, self.def_rolloff_modifiers, atk=False)
        print(f"Modfied Roll Off Target: {self.roll_off_target}\n")

        self.dice_rolls()
        self.determine_winner()


    def dice_rolls(self):

        self.atk_rolls = np.random.randint(1,7,(100000, self.atk_attacks))
        self.def_rolls = np.random.randint(1,7,(100000, self.def_attacks))

        self.atk_rolls = apply_duel_roll_modifiers(self.atk_rolls, self.atk_duel_roll_modifiers)


        print("Dice Rolls Generated")
        print(f"Attacker Dice Rolls Shape: {self.atk_rolls.shape}")
        print(f"Defenders Dice Rolls Shape: {self.def_rolls.shape}\n")




    def determine_winner(self):
        # 1 = attacker win, 0 = defender win, winrate = sum/length
        results = []
        for i in range(0, len(self.atk_rolls)):
            atk_highest = np.max(self.atk_rolls[i,:])
            def_highest = np.max(self.def_rolls[i,:])


            # Attacker wins
            if atk_highest - def_highest > 0:
                results.append(1)
            
            # Defender wins
            elif atk_highest - def_highest < 0:
                results.append(0)

            # Drawn fight
            else:
                # Attacker higher fight value
                if self.atk_fv > self.def_fv:
                    results.append(1)
                # Defender higher fight value
                elif self.atk_fv < self.def_fv: 
                    results.append(0)
                else:
                    roll_off = np.random.randint(1,7)

                    if roll_off >= self.roll_off_target:
                        results.append(1)
                    else:
                        results.append(0)

        self.win_rate = np.sum(results)/len(results)
        print(f"Win Rate: {self.win_rate}")


    def GetWinRate(self):
        return f"Win Rate: {np.round(self.win_rate,2)*100}%"


    def wounds(self):
        wound_chart = np.genfromtxt("assets/wound_chart.csv", delimiter=',')

        wound_rolls = self.atk_rolls

        # Apply Modifiers
        wound_rolls = apply_wound_modifiers(wound_rolls, self.atk_wound_modifiers)

        num_rolls, num_attacks = np.shape(wound_rolls)
                
        wound_roll_required = wound_chart[self.atk_strength-1, self.def_defence-1]
        print(num_rolls, num_attacks)


        results = np.zeros(num_rolls)
        for i in range(0,num_rolls):
            for j in range(0,num_attacks):
                # Normal Wounds
                if self.def_defence - self.atk_strength <= 4:
                    if wound_rolls[i,j] > wound_roll_required:
                        results[i] += 1
                    

                # Double Roll Wounds
                elif(self.def_defence - self.atk_strength >= 5) and (wound_rolls[i,j] >= wound_roll_required):
                    if np.random.randint(1,7) == 6: # need to change with modifiers
                        results[i] += 1 

        fig = px.histogram(x = results, histnorm='percent', labels={'x':'Wounds Dealt'})
        return fig
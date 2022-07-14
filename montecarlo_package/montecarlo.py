import numpy as np
import pandas as pd
import random

class Die():
    '''
    A Die object contains an array of faces and a weight associated to each face.
    The weights are stored in an array of their own and are paired with the faces by index.
    A Die can adjust its weights after initialization.
    A Die can be "rolled" to select a face.
    '''

    def __init__(self, name, arr):
        '''
        Initializes a Die object. name and arr are passed in and set to their respective attributes,
        and weights are all set to 1.0. Additionally, a private DataFrame is initialized, storing the
        faces alongside their weights.

        The array must contain either all strings or all numbers, otherwise initialization will fail.
        In this case, all attributes are set to None.
        '''
        sametype = True
        arrtype = type(arr[0])
        for elm in arr:
            if type(elm) != arrtype:
                sametype = False
        if sametype and arrtype is (str or int or float):
            self._name = name
            self.faces = arr
            self.weights = []
            for i in range(len(arr)):
                self.weights.append(1.0)
            self._df = pd.DataFrame([self.faces, self.weights]).T
            self._df.columns = ["Face", "Weight"]
        else:
            print(arrtype)
            print("Error: All faces must be of same type and either strings or numbers.")
    
    def change_weight(self, face, weight):
        '''
        Changes one weight of the weights attribute. Takes in two params, a face to change the weight of
        and the new weight. Only changes the weight if both params are valid. Returns a boolean indicating
        whether the change was successful (True = weight changed).
        '''
        if face not in self.faces:
            print("Error: " + str(face) + " not in faces DataFrame.")
            return False
        elif not ( isinstance(weight, float) or isinstance(weight, int)):
            print("Error: Weight param is not a int or float.")
            return False
        else:
            i = self.faces.index(face)
            self.weights[i] = float(weight)
            self._df.iloc[i,1] = weight
            return True

    def roll(self, n=1):
        '''
        "Rolls" the Die object n times. n defaults to 1 if not otherwise indicated.
        A Die roll consists of selecting a face from the faces attribute, where faces with larger weights 
        are more likely to be selected.
        
        i.e a face with weight 5.0 is five times as likely to be selected as a face with weight 1.0.

        The list of all faces rolled during the method's execution is returned.
        '''
        lst = random.choices(self.faces, self.weights, k=n)
        return lst

    def get_df(self):
        '''
        A getter method to access the Die's private DataFrame attribute.
        '''
        return self._df

    def get_name(self):
        '''
        A getter method to access the Die's private name attribute.
        '''
        return self._name

class Game():
    '''
    A game entails rolling one or more Die objects, one or more times. Results of most recent game are stored in a private DataFrame.
    '''

    _df = pd.DataFrame()

    def __init__(self, dice):
        '''
        Initializes a Game object with a dice attribute containing one
        or more Die objects. Each Die must contain the same faces, otherwise init fails.
        '''
        eq = True
        valid_faces = sorted(dice[0].faces)
        for die in dice:
            if sorted(die.faces) != valid_faces:
                eq = False
        if eq:
            self.dice = dice
        else:
            print("Error: Die face values not equivalent throughout list. Game construction failed.")

    def play(self, n):
        '''
        Rolls each Die object n times. Stores results of the rolls in the Game private DataFrame with each roll as a row and 
        each Die as a column.
        '''
        self._df = pd.DataFrame()
        for i in range(n):
            lst = []
            for die in self.dice:
                lst.append(die.roll()[0])
            temp_df = pd.DataFrame(data=lst)
            self._df = pd.concat([self._df, temp_df.T])
        indices = np.arange(1, n+1)
        self._df = self._df.set_index(indices)
        cols = [d.get_name() for d in self.dice]
        self._df.columns = cols

    def show_df(self, width="wide"):
        '''
        A getter method to access the Game's private DataFrame attribute. Takes an optional param to display the DataFrame
        as "narrow", with a double-index for rolls and dice.
        '''
        if width == "wide":
            return self._df
        elif width == "narrow":
            narrow = self._df.stack()
            narrow.index.names = ["Roll", "Die"]
            return narrow
        else:
            print("Error: Width parameter must be wide or narrow.")
            return    

class Analyzer():
    '''
    This class takes in a completed Game object and calculates various descriptive statistics on the game results.
    '''

    jackpot_df = pd.DataFrame()
    combos_df = pd.DataFrame()
    face_counts_df = pd.DataFrame()

    def __init__(self, game):
        '''
        Initializes the Analyzer object with the game passed in. This method also determines the type of the face values
        on the dice used in the game.
        '''
        self.game = game
        self.face_type = type(self.game.dice[0].faces[0])

    def jackpot(self):
        '''
        This method returns the number of times the game had a "jackpot", meaning all face values were the same on a given roll.

        The jackpot data is stored in the Analyzer's jackpot_df attribute, which contains a row for each roll and a corresponding
        boolean value for whether or not the roll had a jackpot.
        '''
        n = 0
        df = self.game.show_df()
        for index, row in df.iterrows():
            if len(set(row)) == 1:
                n += 1
                temp_df = pd.DataFrame([index, True])
                self.jackpot_df = pd.concat([self.jackpot_df, temp_df.T])
            else:
                temp_df = pd.DataFrame([index, False])
                self.jackpot_df = pd.concat([self.jackpot_df, temp_df.T])
        self.jackpot_df = self.jackpot_df.set_index(0)
        return n

    def combo_counts(self):
        '''
        This method fills in the combos_df DataFrame such that each row contains a combination that was rolled in the game
        and its number of times rolled. Does not return a value but prints a statement indicating that the combos_df was
        successfully updated.
        '''
        game_df = self.game.show_df()
        combos = {}
        for index, row in game_df.iterrows():
            lst = row.values.flatten().tolist()
            lst.sort()
            s = "(" + ", ".join(str(e) for e in lst) + ")"
            if s in combos.keys():
                combos[s] += 1
            else:
                combos[s] = 1
        self.combos_df = pd.DataFrame(list(combos.items())).sort_values(1, ascending=False)
        print("Combination DataFrame Updated Successfully.")

    def face_counts_per_roll(self):
        '''
        This method fills in the face_counts DataFrame where each row corresponds to a roll, each column is a different
        face value of the set of dice, and the data represents the number of times each face was rolled on a given roll.
        Does not return a value but prints a statement indicating that the face_counts_df was successfully updated.
        '''
        df = self.game.show_df()
        faces = self.game.dice[0].faces
        for index, row in df.iterrows():
            face_counts = {}
            for elm in faces:
                face_counts[elm] = 0
            for r in row:
                face_counts[r] += 1
            temp_df = pd.DataFrame(list(face_counts.items())).set_index(0)
            self.face_counts_df = pd.concat([self.face_counts_df, temp_df.T])
        indices = np.arange(1, len(self.face_counts_df)+1)
        self.face_counts_df = self.face_counts_df.set_index(indices)
        self.face_counts_df.index.names = ["Roll #"]
        print("Face Counts DataFrame Updated Successfully.")
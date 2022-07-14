import unittest
import pandas as pd
from montecarlo import Die, Game, Analyzer

class MontecarloTestSuite(unittest.TestCase):

    def test_00_die_init(self):
        '''
        Confirms that the init method correctly sets the weights array to 1.0 values of a correct length.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        self.assertTrue(die1.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    def test_001_die_change_weight(self): 
        '''
        Tests to confirm that we can validly add a weight and see the change refleccted in the "weights" array.
        Additionally, confirms that the weights are set to floats even if the method takes in an int.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        die1.change_weight("four", 2)
        self.assertTrue(die1.weights == [1.0, 1.0, 1.0, 2.0, 1.0, 1.0])

    def test_002_die_change_weight(self):
        '''
        Tries to change the weight of a face that doesn't exist.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        self.assertFalse(die1.change_weight("seven", 2))
    
    def test_003_die_change_weight(self):
        '''
        Tries to change the weight of a face to an invalid value.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        self.assertFalse(die1.change_weight("four", "notanintorfloat"))

    def test_004_die_roll(self):
        '''
        Ensures that only valid faces end up in the roll's output.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        lst = die1.roll()
        self.assertTrue([elm in die1.faces for elm in lst])

    def test_005_die_roll(self):
        '''
        Ensures that the output list has a length equal to the "n" parameter.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        self.assertTrue(len(die1.roll(5)) == 5)

    def test_006_die_get_df(self):
        '''
        Ensures that the method returns a DataFrame with correct values.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        expected_df = pd.DataFrame([["one", "two", "three", "four", "five", "six"], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]).T
        expected_df.columns = ["Face", "Weight"]
        self.assertTrue(die1.get_df().equals(expected_df))

    def test_007_die_get_name(self):
        '''
        Ensures that the correct name is returned.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        self.assertTrue(die1.get_name() == "die1")

    def test_100_game_init(self):
        '''
        Checks that length of created dice attribute matches length of input array. Input array has identical dice.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        die2 = Die("die2", ["one", "two", "three", "four", "five", "six"])
        die3 = Die("die3", ["one", "two", "three", "four", "five", "six"])
        die4 = Die("die4", ["one", "two", "three", "four", "five", "six"])
        die5 = Die("die5", ["one", "two", "three", "four", "five", "six"])
        game1 = Game([die1, die2, die3, die4, die5])
        self.assertTrue(len(game1.dice) == 5)

    def test_101_game_init(self):
        '''
        Attempts to pass in dice containing different faces. Ensures that no dice attribute is assigned due to the incorrect input.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        die2 = Die("die2", ["one", "two", "three", "four", "five", "six"])
        die3 = Die("die3", ["one", "two", "three", "four", "five", "six"])
        die4 = Die("die4", ["one", "two", "three", "four", "five", "six"])
        die5 = Die("die5", ["one", "two", "three", "four", "five", "seven"]) # six changed to seven
        game1 = Game([die1, die2, die3, die4, die5])
        self.assertFalse(hasattr(game1, 'dice'))

    def test_102_game_play(self):
        '''
        Plays a game with 20 rolls. Ensures that the DataFrame attribute has 20 rows and 5 columns (for the 5 Die objects).
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        die2 = Die("die2", ["one", "two", "three", "four", "five", "six"])
        die3 = Die("die3", ["one", "two", "three", "four", "five", "six"])
        die4 = Die("die4", ["one", "two", "three", "four", "five", "six"])
        die5 = Die("die5", ["one", "two", "three", "four", "five", "six"])
        game1 = Game([die1, die2, die3, die4, die5])
        game1.play(20)
        self.assertTrue(game1._df.shape == (20, 5))

    def test_103_game_play(self):
        '''
        Plays two consecutive games, first with 20 rolls and second with 25 rolls. Ensures that only the second game's results
        are stored in the DataFrame attribute, i.e the df's shape is 25 rows and 5 columns.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        die2 = Die("die2", ["one", "two", "three", "four", "five", "six"])
        die3 = Die("die3", ["one", "two", "three", "four", "five", "six"])
        die4 = Die("die4", ["one", "two", "three", "four", "five", "six"])
        die5 = Die("die5", ["one", "two", "three", "four", "five", "six"])
        game1 = Game([die1, die2, die3, die4, die5])
        game1.play(20)
        game1.play(25)
        self.assertTrue(game1._df.shape == (25, 5))

    def test_104_game_show_df(self):
        '''
        Plays one game, then checks that the show_df method (in wide form) returns the DataFrame attribute identically.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        die2 = Die("die2", ["one", "two", "three", "four", "five", "six"])
        die3 = Die("die3", ["one", "two", "three", "four", "five", "six"])
        die4 = Die("die4", ["one", "two", "three", "four", "five", "six"])
        die5 = Die("die5", ["one", "two", "three", "four", "five", "six"])
        game1 = Game([die1, die2, die3, die4, die5])
        game1.play(20)
        self.assertTrue(game1._df.equals(game1.show_df()))

    def test_105_game_show_df(self):
        '''
        Plays one game. Calls the show_df method with the "narrow" parameter. Ensures that the shape of the narrow DataFrame
        is now a single value, equal to (the number of dice) * (the number of rolls).
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        die2 = Die("die2", ["one", "two", "three", "four", "five", "six"])
        die3 = Die("die3", ["one", "two", "three", "four", "five", "six"])
        die4 = Die("die4", ["one", "two", "three", "four", "five", "six"])
        die5 = Die("die5", ["one", "two", "three", "four", "five", "six"])
        game1 = Game([die1, die2, die3, die4, die5])
        num_dice = len(game1.dice)
        num_rolls = 20
        expected_shape = num_dice * num_rolls
        game1.play(num_rolls)
        narrow_df = game1.show_df("narrow")
        self.assertTrue(narrow_df.shape == (expected_shape,))

    def test_200_analyzer_init(self):
        '''
        Initializes an Analyzer object and confirms its type attribute is correct.
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        die2 = Die("die2", ["one", "two", "three", "four", "five", "six"])
        die3 = Die("die3", ["one", "two", "three", "four", "five", "six"])
        die4 = Die("die4", ["one", "two", "three", "four", "five", "six"])
        die5 = Die("die5", ["one", "two", "three", "four", "five", "six"])
        expected_face_type = str
        game1 = Game([die1, die2, die3, die4, die5])
        game1.play(20)
        analyzer1 = Analyzer(game1)
        self.assertTrue(analyzer1.face_type == expected_face_type)

    def test_201_analyzer_jackpot(self):
        '''
        Creates a game object that guarantees that every roll will be a jackpot (two faces, one with weight 0.0). Ensures
        that jackpot method's output matches the number of rolls.
        '''
        die1 = Die("die1", ["one", "two"])
        die2 = Die("die2", ["one", "two"])
        die1.change_weight("one", 0)
        die2.change_weight("one", 0)
        game1 = Game([die1, die2])
        num_rolls = 20
        game1.play(num_rolls)
        analyzer1 = Analyzer(game1)
        self.assertTrue(analyzer1.jackpot() == num_rolls)

    def test_202_analyzer_combo_counts(self):
        '''
        Creates a game object that is virtually guaranteed to have three different combinations. Check that after calling 
        this method, the combos_df attribute has three rows.
        '''
        die1 = Die("die1", ["one", "two"])
        die2 = Die("die2", ["one", "two"])
        game1 = Game([die1, die2])
        game1.play(100) # 100 rolls virtually guarantees that each of the three possible combos will occur one or more times.
        analyzer1 = Analyzer(game1)
        analyzer1.combo_counts()
        self.assertTrue(len(analyzer1.combos_df) == 3)

    def test_203_analyzer_face_counts_per_roll(self):
        '''
        Creates a game object that plays a 100-roll game. The dice have six faces each. Ensures that the face_counts_df attribute
        has shape (100, 6).
        '''
        die1 = Die("die1", ["one", "two", "three", "four", "five", "six"])
        die2 = Die("die2", ["one", "two", "three", "four", "five", "six"])
        die3 = Die("die3", ["one", "two", "three", "four", "five", "six"])
        die4 = Die("die4", ["one", "two", "three", "four", "five", "six"])
        die5 = Die("die5", ["one", "two", "three", "four", "five", "six"])
        game1 = Game([die1, die2, die3, die4, die5])
        game1.play(100)
        analyzer1 = Analyzer(game1)
        analyzer1.face_counts_per_roll()
        self.assertTrue(analyzer1.face_counts_df.shape == (100, 6))


if __name__ == '__main__':

    unittest.main(verbosity=3)
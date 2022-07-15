# FinalProject5100

## Metadata
David Siamon, Monte Carlo Simlulator

Most recent patch July 14, 2022 (0.0.0)

## Synopsis
This package contains three classes, used in conjunction to create a basic [Monte Carlo Simulator](https://en.wikipedia.org/wiki/Monte_Carlo_method). 
To install, clone this repo with `git clone https://github.com/davsiam57349/FinalProject5100`. Then, when in root of repo, run `pip install -e`

### Die
The Die object can be constructed to model a standard six-sided numeric die, but contains adjustable parameters to be outlined further below.

Firstly, we can initialize a Die with our \_\_init_\_\ method:

`dice_values = [1, 2, 3, 4, 5, 6]`  
`regular_die = Die('regular_die', dice_values)` 

Here we have created a basic instance of a Die. We can now call its roll method and specify the number of times to “roll” our die (defaults to 1). The method returns a list where we can see the roll results:

`lst = regular_die.roll(20)`

The lst variable would contain, formally, a random sample from the faces of our die, repeated 20 times.

We can create other Die objects however we desire. Here I create an object analogous to a fair coin and another containing all letters of the English:

`coin = Die('coin', ['Heads', 'Tails']`  

`letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']`
`alphabet = Die('alphabet', letters]`

Note that all faces have to be of the same datatype, and said datatype must be either a string or a number.

Lastly, we can change the "weight" of a Die face to affect the probability said face comes up when the Die is rolled. All weights are initially set to 1.0 in initialization time. As such, if we want to change our coin object to have it 3/4 likely to show heads, we would use the change_weight method as follows:

`coin.change_weight("Heads", 3.0)`

### Game
A Game object takes in a list of one or more Die objects, and rolls them simultaneously.

First, we initialize our Game with its \_\_init_\_ method:

`die1 = Die("die1", [1, 2, 3, 4, 5, 6])`  
`die2 = Die("die2", [1, 2, 3, 4, 5, 6])`  
`die3 = Die("die3", [1, 2, 3, 4, 5, 6])`  
`die4 = Die("die4", [1, 2, 3, 4, 5, 6])`  
`die5 = Die("die5", [1, 2, 3, 4, 5, 6])`  
`game = Game([die1, die2, die3, die4, die5])`

Note that all Die objects passed into the initializer must have the same list of possible faces. This game now contains the five Die objects we created. Next, we can use the play method to roll this set of dice n times:

`game.play(20)`

The play method doesn't return a value, but the roll outputs can be returned in a pandas DataFrame using the show_df method:

`game.show_df()`

This method also takes an optional parameter, `show_df('narrow')`, which returns the results in a multi-indexed DataFrame on rolls and Die faces.

### Analyzer

We use the Analyzer class to calculate various statistics on a played Game object's results. It gets set up with an \_\_init_\_ method that takes in a completed game as a parameter:

`analyzer = Analyzer(game)`

This code initializes an Analyzer object for the Game object created above. We can now use the class's other three methods to provide us with statistics on the game's results:

`analyzer.jackpot()` returns the number of rolls in the game where all faces rolled the same value. Also populates a jackpot_df attribute indexed by roll number, containing a boolean for whether or not the roll was a jackpot.  
`analyzer.combo_counts()` computes the distinct combinations of faces rolled, along with their counts, and stores the results to a combos_df attribute.  
`analyzer.face_counts_per_roll()` computes, roll by roll, how many times each face was rolled among the set of dice. These results are stored in the face_counts_df attribute, where each row is a distinct roll and each column is a different die face.

## API Description

### Die Methods:

`\_\_init_\_  ` 
Initializes a Die object. name and arr are passed in and set to their respective attributes,
and weights are all set to 1.0. Additionally, a private DataFrame is initialized, storing the
faces alongside their weights.

The array must contain either all strings or all numbers, otherwise initialization will fail.
In this case, all attributes are set to None.

params  
name (str) -- the Die's name  
faces (list) -- the list of faces that the Die could potentially roll (the sample space)  

returns  
None

`change_weight`  
Changes one weight of the weights attribute. Takes in two params, a face to change the weight of
and the new weight. Only changes the weight if both params are valid. Returns a boolean indicating
whether the change was successful (True = weight changed).

params  
face -- an element in the faces attribute for which the weight should be changed  
weight (float) -- the weight to change the indicated face to

returns 
True if weight is changed successfully, False if not

`roll`  
"Rolls" the Die object n times. n defaults to 1 if not otherwise indicated.
A Die roll consists of selecting a face from the faces attribute, where faces with larger weights 
are more likely to be selected.

i.e a face with weight 5.0 is five times as likely to be selected as a face with weight 1.0.

The list of all faces rolled during the method's execution is returned.

params  
(optional) n (int) -- number of times to roll the Die. Defaults to 1.

returns 
A list of all faces rolled during the method's execution

## Manifest
- LICENSE
- README.md
- FinalProjectSubmissionTemplate.ipynb
- letter-freqs.csv
- montecarlo_test.py
- montecarlo_test_output.txt
- setup.py
- \_\_pycache_\_\
  - montecarlo.cpython-39.pyc
  - montecarlo_test.cpython-39.pyc
- montecarlo_package\
  - \_\_init_\_\.py
  - montecarlo.py

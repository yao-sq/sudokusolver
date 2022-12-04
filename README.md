# Sudoku solver

## Approach

The implementation included in the `.ipynb` file uses depth-first constraint satisfaction with backtracking.
In this approach, a board state is viewed as a collection of variables, each of which has a chosen value or a list of possible values called the domain. There are a number of constraints defined for the variables, which correspond to the rules of sudoku: in each column, row, and box, the cells must have different values. The algorithm picks a value to assign to an unnassigned variable, applies it and checks whether the constraints are satisfied. If the constraints are satisfied, the process is repeated until a goal state is reached. Else, if the constraints are not satisfied, the algorithm backtracks and makes a different choice. A goal state is one where all variables have an assigned value, and the constraints are satisfied.
In addition to the general part of the algorithm, the implementation looks for patterns when the possible values are being updated. These recognised patterns reduce the possible values in a logical manner, which results in a drastically smaller search space.

### Code Overview

The main function in the implementation is `sudoku_solver`, following the structure of the provided code.

The `sudoku_solver` function first declares all the variables, which correspond to sudoku cells, along with their domain, which in the beginning is everything - all the digits except zero; Then it transforms the initial input grid into a state composed of variables and their assigned values; Then it creates an initial state in which all the variables have their possible values updated; In that initial state, once all possible values are updated, the implementation looks for logical patterns; Then it declares the constraints on columns, rows, and boxes; With variables, constraints, and the initial state defined, the function calls the more general `solve` function to find a solution; Finally, the result, which is either a goal state or `None` when there is no solution, is transformed into a numpy array, as expected by the rest of the code.

The `solve` function implements the depth-first constraint satisfaction with backtracking algorithm. It accepts as parameters the initial state, the constraints, and two functions that can specialise the behaviour: `successor_generator` and `goal_check`. The latter of the two function parameters, `goal_check`, is a simple function that checks whether all variables have an assigned value. It will only be called to check a state that satisfied the constraints, and if it returns `True`, that checked state will be the final solution. The former of the two function parameters, `successor_generator`, is the heart of the solver and will be described in more detail below. With these parameters, the `solve` function uses recursion to achieve backtracking, and repeatedly uses `successor_generator` to make a choice and continue the search in a depth-first manner.

The provided `successor_generator` function has to produce successor states, given a state. Broken down into simpler steps, it makes a choice for a variable and a value, and applies that choice to produce a successor state. When there are multiple choices, there are multiple successors, and that is where the search space grows. The actual implementation uses a general helper function called `successor_generator` that takes in three function parameters and combines them to achieve the desired functionality. Namely, the three parameters are `choice_generator`, `update_possible`, `check_valid`, and they correspond to the simpler steps of "making a choice", then updating other variables accordingly, and then checking if the produced successor state is actually valid.

Of the three parameters, the last one, `check_valid`, is the simplest and in the case of this sudoku implementation it simply checks if there are any unassigned variables that have no remaining possible value. This check saves the effort of making choices for all the variables that still do have possible values, only to find some time later that the constraints cannot be satisfied.

The second of the three parameters, `update_possible`, is semantically simple, but represents the more complicated aspect of the implementation. It is used to update the possible values of other variables, once a value is chosen for a variable. But while updating the domains of variables, it also looks for logical patterns. There are a fair number of known sudoku strategies, which correspond to such patterns, but only the basic ones have been included in this implementation. The included ones, as can be found in the `handle_patterns` function, are: "Pointing Pairs/Triples", "Box/Line Reduction", "Naked Pairs", "Naked Triples", and "Hidden Pairs". These are applied recursively, as the application of one such pattern can expose another.

And lastly, the first of the three parameters, `choice_generator`, is used to get an array of choices, which are a simply a pair of a variable and a value. The implementation of that first looks for variables with only one possible value, called "Naked Singles", and if any exist chooses the first one. By choosing only one, there is effectively no branching and the search space does not grow. The next interation of the algorithm will choose the next such "safe choice", until they are all applied. In much the same way, the implementation looks for "Hidden Singles", which are variables that are the only ones capable of having a specific value. For example, if in a column there is only one cell that can have the value `1`, then even if seemingly possible for the cell to also have other values like `2` and `3`, it must be `1`.
If there are no "safe choices", the function will return an array of choice tuples, but will try to be clever about it. It will gather all the unassigned variables in the box closest to completion, and list the choices for those. In other words, it will find which box has the fewest unassigned variables and only return those as choices. The reasoning behind that is that if even one box cannot be completed, there is no point exploring the other choices for the other unassigned variables - the constraints on this box will never be satisfied.


### Recognised patterns

As mentioned in the overview, several patterns are included in this implementation.
This section will only briefly describe them. For more details, please visit a website like https://www.sudokuwiki.org

The implementation checks for these patterns whenever a variable's possible values get updated.

#### Pointing Pairs/Triples

A pointing star is a pattern of two or three candidate cells for a given number, in the same box, that are also in the same column or in the same row. It implies all other candidate cells in that column or row cannot possibly have the given number.

Whenever a variable in a box gets updated, the box is checked for this pattern. If the number of remaining candidates for the updated number is two or three, and their `x` or `y` coordinate is the same, then the pattern can be applied to the touched column or row respectively.

#### Box/Line Reduction

Box/Line Reduction is a pattern of two or three candidate cells for a given number, in the same column or row, that are also in the same box. It implies the given number cannot be anywhere else in that box.

Whenever a variable gets updated, the column and the row get checked. If the number of remaining candidates for the updated number is two or three, and they all belong to the same box, then all other cells in the box get updated.

#### Naked Pairs

A Naked Pair is a pattern where only two candidates remain in a unit (box/row/column), and those two candidates only have two possible values that are the same. It implies that those two numbers cannot be anywhere else in the neighbours besides that pair of cells.

Whenever a variable gets updated, all of its units (box/row/column) get checked. If there are two unassigned variables with two possible values each, and those two possible values are the same, then the rest of the unit gets updated.

#### Naked Triples

A Naked Triple is much like a Naked Pair, but the number of candidates is three, and the total of possible values is three - but the possible values for an individual cell can be fewer. It implies, like in the Naked Pair case, that those possible values cannot be anywhere else in the neighbours besides that triple.

Whenever a variable gets updated, all of its units get checked. If there are three remaining candidates and their distinct possible values are three, then the rest of the unit gets updates.

#### Hidden Pairs

A Hidden Pair is a pattern where in a given unit (box/row/column) there are only two candidates for any two numbers. It implies that those cells cannot have any other value besides the two numbers.

Whenever a variable is updated, all of its units get checked. If there are two candidates remaining for the updated value, and for any of the other possible values for those cells these two are again the only remaining candidates in the unit, then all other possible values get removed from the two cells.


## Implementation notes

### Note 1
The implementation looks for patterns only after the initial state is created.
In an earlier version of the code, the initial state was built by setting the input values one at a time and looking for the patterns at each application.
However, that was found to noticeably slow down the execution, and it was not actually critical to the correctness. A naive loop over all cells and all values, after the initial state was created, proved faster while still producing correct results.

### Note 2
Logically, the checks for "Naked Singles" and "Hidden Singles" that happen in the `choice_generator` as "safe choices", actually belong in the pattern detection code, and not in the choice generator.
However, the pattern detection code gets invoked many more times, and because of that the overall execution time is higher.
On top of that, it is possible that with the application of all the patterns, the whole puzzle gets solved without any choices for backtracking. And for that to work, all the loops and the search over "choices" needs a bit of extra logic just to handle it. It is certainly doable, but the code is easier to read this way, when there is guaranteed to be a choice, even if it is a "safe choice"
It can be viewed as: code that chooses a value is in the `choice_generator`, whilst code that updates possible values is in the `handle_patterns`.

### Note 3
Technically, the implementation could use an array to represent the state and the variables, instead of a dictionary.
However, the goal of the coursework is not to optimise code with technical tricks. So this was not done.

### Note 4
Memoization was used in some places in the form of `@functools.cache`.
Although it can be considered a "technical trick", it does not greatly affect the performance.
It can easily be removed by removing the annotations/decorators, but was left in simply because it was trivial to apply through the annotations.

### Note 5
The general function `solve` performs the depth-first search with backtracking. Given the abstraction of the `successor_generator`, other search algorithms can also be implemented and only the `solve` function should have to change. It can be replaced with a breadth-first search, or a heuristic search, because the successor states can be retrieved.
However, for the current implementation, depth-first search is the simplest.

### Note 6
In an earlier version of the code, the strategy for returning multiple choices for successor states was different, as can be seen in the code comments. It was finding the number/value that was closest to completion, and listing all the candidates for it as choices.
However, empirically it was found that it was not very performant. The other strategy of "closest box to completion" performed significantly better, in some cases reducing the time from 1.5sec down to 0.3sec.
A possible explanation for that is that most patterns apply to boxes and because of that the choices for variables in the same box lead to far less branching.

### Note 7
An attempt was made to implement another pattern/strategy - X Wing. However, it is not tested and most likely wrong. The examples did not trigger it, probably because of the particular order the patterns are checked in. The other patterns are more likely to have already updated the values.

## Future work

- Fix the "X Wing" pattern code
- Implement other patterns/strategies.
  From trying out the solver at sudokuwiki.org , the most "useful" one seemed to be "Alternating Inference Chains".

# Reflection

## Adjust Request Trace

For the request `adjust 3 offset=2 scale=4`, the CLI first separates the command name, value, and options. The value starts as `3`, and the options are `offset=2` and `scale=4`. The CalculationFactory converts these inputs into numeric values and creates a Calculation using `Operations.adjust`. At this point, the calculation has only been constructed and the math has not happened yet. When the CalculateCommand executes, the session calls `calculation.get_result()`. The adjust operation calculates `(3 + 2) * 4`, which gives `20.0`. After the calculation succeeds, the session saves the calculation and actual result in history. The command returns the display text `Result: 20.0000`.

## Failed Span and Last Request Trace

For the request `span 5`, the factory creates the Calculation because span accepts a variable number of operands. The error does not happen during construction. When the calculation executes, `Operations.span` checks the number of values. Since only one value was provided, it raises a ValueError. The exception happens before the session adds anything to history, so the failed calculation is not saved. If `last` is entered afterward and there were no earlier successful calculations, LastCommand reads the history and returns `History is empty.` It does not execute the failed calculation again.

## Design Concepts

The static operations perform math without needing an Operations object. For example, `Operations.adjust` receives values, performs the calculation, and returns a number. Commands are different because they represent application actions. A command is an object with an `execute()` method and can work with other objects such as the CalculatorSession.

`*args` allows a function to receive a flexible number of positional values. This is useful for span because it can receive multiple readings. `**kwargs` allows named options to be passed, such as `offset` and `scale` for adjust.

The factory is responsible for selecting the correct operation and constructing a Calculation. Commands are responsible for application actions such as calculating, displaying history, clearing history, and showing the last result.

One LBYL choice is checking the number of values in `Operations.span` before calling `max()` and `min()`. The program checks that at least two values exist and raises a clear ValueError when the request is invalid. An EAFP example is the factory trying to retrieve an operation from the operations dictionary and catching KeyError when the operation does not exist. These choices make expected failures easier to understand and handle.

## Student Tests

I added tests for adjust with an offset and scale, span with negative values, and span with too few values. These tests check both successful calculations and an expected error. I also tested LastCommand with successful and empty history. Finally, I tested that a failed division is not added to history. This case is useful because it confirms that the session records calculations only after they succeed.
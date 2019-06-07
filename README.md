# test_suite

This is a basic curses-based test gui that was built for fun by Scragly during the Python Discord Code Jam 5 Qualifier for the purpose of testing entries while also being sort of pretty, as far as CLI interfaces go.

To create a collection of tests for an event, you need to first define a TestGroup with methods containing Tests.

A test group must have a class attribute of `name` that defines the display name for the group.

Test methods must be named with `test_` at the beginning so they are detected.

Test methods must have a docstring, with the first two characters being used for the number used when sorting, and the remainder being the display description of the test.

Test methods can access the test function via `self.function`.

Test methods can return one of two ways:
 - a single Truthy/Falsy value representing if the test passed or not
 - a tuple of `passed, value` where `passed` is evaluating if passed, and `value` is shown on the result line.

To start the tests, you create an instance of `Suite` with the title shown on the test window, and the function to be tested.

```py
from test_suite import Suite, TestGroup
from tested_module import test_function


class FakeTests(TestGroup):
    name = "Fake"

    def test_string(self):
        """1 Returns a string"""
        # returns only a single True/False value
        return isinstance(self.function(), str)

    def test_length(self):
        """2 Length over 10"""
        length = len(self.function())
        if length > 10:
            # returns True for passed, shows length as result value
            return True, length
        else:
            # returns False for passed, shows length as result value
            return False, length

suite = Suite(f"Example Test Suite - {entry_name}.py", test_function)
```
# Testing

Python is an interpreted language.  This gives it a great deal of flexibility, such as duck typing.  However, this can also lead to different types of common bugs.  For example, if you pass a `float` to a function that really should only receive  an `int`, Python won’t stop you, but it might lead to unexpected behavior.  In general, we have to run the code to get an error, but not all bugs will generate errors.  Towards the goal of writing correct code, we use tests to determine two things:


1. **Does it work?**  That is, does the code do what it’s supposed to do?
2. **Does it still work?** Can you be confident that the changes you made haven’t caused other part of the code to break?

## Writing Tests

Testing your code means writing more code that checks that the behavior matches your expectations. This is important:

> Test  behavior, not implementation.

You have some idea of what code is supposed to do.  You run the code.  Did it do what you expected?  How about some other inputs?  In the simplest case, you could simply add some code to the bottom of the module.  

```python {cmd}
class Doubler:
    def __init__(self, n):
        self._n = 2 * n

    def n(self):
        return self._n

if __name__ == ‘__main__’:
    x = Doubler(5)
    assert(x.n() == 10)
    y = Doubler(-4)
    assert(y.n() == -8)
```

The `assert` statement will raise an error if the predicate that follows it is `False`.  Otherwise, the program just continues as usual.  Assertions are much better than just printing because you don’t have to manually check to see that it printed what you expected it to print.  Also, people have a tendency to delete old print statements to reduce clutter in their test output.  Deleting tests after they pass is a *very bad idea*.  Your code is going to change, and you will want to know if a change breaks something that *used* to work.

The line `if __name__ == ‘__main__’:` makes sure that the tests will not run when the module is imported from somewhere else.

For some, learning to test their code runs into a substantial psychological block.  They feel that testing the code will reveal its flaws and thus reveal the programmer’s flaws.  If you feel the slightest hesitation to testing your own code, you should practice the OGAE protocol.  It stands for, "Oh Good, An Error!".  Every time you get an error, you say this with honest enthusiasm.  The computer has just done you a huge favor by identifying something wrong, and it has done so in the safety of your room or office.  You can fix it before it becomes any bigger.

## Unit Testing with `unittest`

The simple kind of testing in the module described above is fine for tiny programs that will not be needed again, but for anything remotely serious, you will need proper **unit tests**.  The word unit in *unit* testing is meant to imply a single indivisible case.  Thus, unit tests are supposed to test a specific behavior of a specific function.  This means you will have many tests and you will run them all, every time you change the code.  

To make the process go smoothly, there is a standard package  called `unittest` for writing unit tests in Python.  The package provides a standard way to write the tests, the ability to run the tests all together, and the ability to see the results of the tests in a clear format.  In modern software engineering, tests are also run automatically as part of build and deployment systems.

To use the `unittest` package, you will want to import the package in your test file.
Then, import the code you want to test.
The actual tests will be methods in a class that extends the `unittest.TestCase` class.
Every test method must start with the word "test".  If it doesn’t start with "test", then it will not run.
Tests are run by calling the `unittest.main` function.

Here is an example that tests a particular behavior of a hypothetical `DayOfTheWeek` class.

```python {cmd}
import unittest
from dayoftheweek import DayOfTheWeek

class TestDayOfTheWeek(unittest.TestCase):
    def testinitwithabbreviation(self):
        d = DayOfTheWeek(‘F’)
        self.assertEquals(d.name(), ‘Friday’)

        d = DayOfTheWeek(‘Th’)
        self.assertEquals(d.name(), ‘Thursday’)		

unittest.main()
```

Notice that even if we have never seen the code for the `DayOfTheWeek` class, we can get a good sense of its expected behavior from reading the tests.  In this case, we see that it can be instantiated with the abbreviation `F` and the `name()` function will return the value "Friday".  It often happens that unit tests like this give the clearest specification of a data structure’s expected behavior.  Moreover, because the tests can be executed, one can be certain that the class really has the expected behavior.  With documentation, one sometimes finds that changes in the code are not reflected in the documentation, but passing tests don’t have this problem.

## Test-Driven Development

**Test-Driven Development (TDD)** is based on the simple idea that you can write the tests before you write the code.  But won’t the test fail if the code hasn’t been written yet?  Yes, if it’s a good test.  What if it passes?  Then, either you’re done (unlikely) or there is something wrong with your test.

Writing tests first forces you to do two things:

1. Decide how you want to be able to use some function.  What should the parameters be?  What should it return?
2. Write only the code that you need.  If there is code that doesn’t support some desired behavior with tests, then you don’t need to write it.

The TDD mantra is **Red-Green-Refactor**.  It refers to three phases of the testing process.

- **Red:** The tests fail.  They better!  You haven’t written the code yet!
- **Green:** You get the tests to pass by changing the code.
- **Refactor:** You clean up the code, removing duplication.

The terms "Red" and "Green" refer to many testing fameworks that show failed tests in red and passing tests in green.

**Refactoring** is the process of cleaning up code, most often referring to the process of removing duplication.  Duplication in code, whether it comes from copy-and-paste or just repeating logic can be a source of many errors.  If you duplicate code with a bug, now you have two bugs.  If you find the bug, you will have to find it twice.

Here is a simple example of refactored code:

**Original Code with Minor Duplication:**

```python
avg1 = sum(L1)/len(L1)
avg2 = sum(L2)/len(L2)
```

Then, it is observed that there should be some default behavior for empty lists so (a test is added and) the code is updated as follows.

**Updated Code Before Refactoring:**

```python
if len(L1) == 0:
    avg1 = 0
else:
    avg1 = sum(L1) / len(L1)

if len(L2) == 0:
    avg2 = 0
else:
    avg2 = sum(L2) / len(L2)
```

**Refactored Code:**

```python
def avg(L):
    if len(L) == 0:
        return 0
    else:
        return sum(L) / len(L)

avg1 = avg(L1)
avg2 = avg(L2)
```

In the refactored code, the details of the `avg` function are not duplicated.  If we want to later modify how the code handles empty lists, we will only have to change it in one place.  

The refactored code is also easier to read.  

## What to Test

Step away from the computer.  Think about the problem you are trying to solve.  Think about the methods you are writing.  Ask yourself, *"What should happen when I run this code?"*. Also ask yourself, *"How do I want to use this code?"*

- Write tests that use the code the way it ought to be used.
- Then write tests that use the code incorrectly to test that your code *fails gracefully*.  Does it give clear error messages?
- Test the *edge cases*, those tricky cases that may rarely come up.  Try to break your own code.
- Turn bugs into tests.  A bug or an incorrect behavior can reappear after you fix it.  You want to catch it when it does.  Sometimes you notice a bug when a different test fails.  Write a specific test to reveal the bug, then fix it.
- Test the public interface.  Usuually you don’t need to or want to test the private methods of a class.  You should treat the test code as a user of the class and it should make no assumptions about private attributes.  This way, if a private gets renamed or refactored, you don’t have to change the tests.

## Testing and Object-Oriented Design

In object-oriented design, we divide the code into classes.  These classes have certain relationships sometimes induced by inheritance or composition.  The classes have public methods.  We call these public methods the **interface** to the class.

To start a design, we look at the problem and identify nouns (classes) and verbs (methods).  In our description, we express what *should* happen.  Often these expectations are expressed in "if...then" language, i.e., "if I call this method with these parameters, then this will happen.". A unit test will encode this expectation.  It will check that the actual behavior of the code matches the expected behavior.

When writing a class, it helps focus our attention and reduce the number fo things to think about if we assume each class works the way it is supposed to.  We try to make this true by testing each class individually.  Then, when we compose classes into more complex classes, we can have more confidence that any errors we find are in the new class and not somewhere lurking in the previously written classes.  

At first it may seem like a waste of time to thoroughly test your code.  However, any small savings in time you might reap early on by skipping tests will very quickly be spent in the headaches of countless hours debugging untested code.  When you have lots of untested code, every time there is an unexpected behavior, the error could be anywhere.  The debugging process can virtually grind to a halt.  If and when this happens to you: Stop. Pick one piece. Test it. Repeat.  Being careful and systematic will take you substantially less time overall. **It is faster to go slow**.

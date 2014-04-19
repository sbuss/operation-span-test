"""Generate random equations with a correct and incorrect answer."""
from operator import add
from operator import div
from operator import mul
from operator import sub
import random


class Equation(object):
    """A general-purpose equation container"""
    def __init__(self, **kwargs):
        for (key, val) in kwargs.items():
            setattr(self, key, val)

    @property
    def correct_answer(self):
        raise NotImplementedError("You must define the equation")

    @property
    def incorrect_answer(self):
        raise NotImplementedError(
            "You must define a way to find an incorrect answer")

    @classmethod
    def random(cls):
        """Return a random Equation."""
        raise NotImplementedError("You must define a random initializer")

    @property
    def str_correct(self):
        return "%s = %s" % (self, self.correct_answer)

    @property
    def str_incorrect(self):
        return "%s = %s" % (self, self.incorrect_answer)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self)


class SimpleEquation(Equation):
    """(x <op_1> y) <op_2> z.

    This guarantees that all oerations work correctly with integers.
    """
    def apply(self, x, op_1, y, op_2, z):
        return op_2(op_1(x, y), z)

    @property
    def correct_answer(self):
        return self.apply(self.x, self.op_1, self.y, self.op_2, self.z)

    @property
    def incorrect_answer(self):
        # Now figure out an incorrect answer:
        ans = self.correct_answer
        incorrect = random.randint(1, 10)
        if ans != incorrect:
            return incorrect
        return self.incorrect_answer

    @classmethod
    def random(cls):
        """Generate a random equation in the form (x <op_1> y) <op_2> z.

        The goal is to have a single digit positive answer
        """
        op_1 = random.choice([mul, div])

        if op_1 == div:
            y = random.randint(1, 9)
            # Ensure integer division
            max_factor = 20 / y
            x = y * random.randint(1, max_factor)
        else:
            y = random.randint(1, 4)
            max_factor = min(20 / y, 10)
            x = random.randint(1, max_factor)

        #op_2 = random.choice([add, sub])
        ans = op_1(x, y)
        minz = -ans
        maxz = 10 - ans
        z = random.randint(minz, maxz)
        if z < 0:
            z = -z
            op_2 = sub
        else:
            op_2 = add
        return cls(x=x, op_1=op_1, y=y, op_2=op_2, z=z)

    def __str__(self):
        functions = {mul: "*", div: "/", add: "+", sub: "-"}
        return "({x} {op_1} {y}) {op_2} {z}".format(
            x=self.x, op_1=functions[self.op_1], y=self.y,
            op_2=functions[self.op_2], z=self.z)


def dump_random_equations(outfile_name, equation_cls, number_of_eqs):
    with open(outfile_name, 'w') as out:
        out.write("equation,correct_answer,incorrect_answer\n")
        for i in range(number_of_eqs):
            eq = equation_cls.random()
            out.write("%s,%s,%s\n" % (
                eq, eq.correct_answer, eq.incorrect_answer))

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
    """(x <op_1> y) <op_2> z"""
    @property
    def correct_answer(self):
        return self.op_2(self.op_1(self.x, self.y), self.z)

    @property
    def incorrect_answer(self):
        return self.op_2(self.op_1(self.x - 1, self.y + 1), self.z)

    @classmethod
    def random(cls, minx=0, maxx=20, miny=0, maxy=20, minz=0, maxz=20,
               op_1=None, op_2=None):
        """Generate a random equation in the form (x <op_1> y) <op_2> z.

        op_1 and op_2 are the operators to choose from.
        If op_1 is not defined, defaults to [mul, div]
        if op_2 is not defined, defaults to [add, sub]
        """
        op_1 = random.choice(op_1 or [mul, div])
        op_2 = random.choice(op_2 or [add, sub])
        x = random.randint(minx, maxx)
        y = random.randint(miny, maxy)
        z = random.randint(minz, maxz)
        return cls(x=x, op_1=op_1, y=y, op_2=op_2, z=z)

    def __str__(self):
        functions = {mul: "*", div: "/", add: "+", sub: "-"}
        return "({x} {op_1} {y}) {op_2} {z}".format(
            x=self.x, op_1=functions[self.op_1], y=self.y,
            op_2=functions[self.op_2], z=self.z)

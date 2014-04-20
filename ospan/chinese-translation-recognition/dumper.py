import csv
from itertools import chain
from itertools import groupby
import os
from random import shuffle

from csv_to_sesame import Loop
from csv_to_sesame import group_to_variables


def load(filename):
    reader = csv.DictReader(open(filename, 'r'))
    return reader


def separate_by_color(reader):
    colors = dict()
    for (color, group) in groupby(
            reader, lambda x: x['Color_Group']):
        colors[color] = list(group)
    return colors


def chunks(l, n):
    """Yield successive n-sized chunks from l.
    From http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python  # nopep8
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def run():
    """Produce several loops:
    320 variables, in groups of 80, for yes-no_yellow, and yes-no_green
    """
    os.chdir('chinese-translation-recognition')
    sminus = separate_by_color(load('sminus.csv'))
    splus = separate_by_color(load('splus.csv'))
    tminus = separate_by_color(load('tminus.csv'))
    tplus = separate_by_color(load('tplus.csv'))
    yes = load('yes trials.csv')
    practice = load('practice.csv')

    with open('out.txt', 'w') as out:
        # First dump practice
        practice_loop = Loop(
            'Practice', description="Practice run",
            variable_rows=group_to_variables(practice))
        out.write(str(practice_loop))
        out.write("\n")

        # Now separate the yellows and the greens
        def cfilter(color):
            return sminus[color] + splus[color] + tminus[color] + tplus[color]

        yellows = cfilter("Yellow")
        greens = cfilter("Green")

        # Can't seek on a csv reader, so make it a list
        yes_list = list(yes)

        # And finally combine the groups and sort randomly
        yes_yellow = yes_list + yellows
        yes_green = yes_list + greens
        shuffle(yes_yellow)
        shuffle(yes_green)
        # and dump in groups of 80
        count = 1
        for chunk in chain(chunks(yes_yellow, 80), chunks(yes_green, 80)):
            loop = Loop(
                "Formal%s" % count, description="Formal run #%s" % count,
                variable_rows=group_to_variables(chunk))
            out.write(str(loop))
            out.write("\n")
            count += 1


if __name__ == "__main__":
    run()

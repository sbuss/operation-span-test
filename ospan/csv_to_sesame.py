import argparse
from collections import namedtuple
import csv
from itertools import groupby


class Loop(object):
    def __init__(self, name, repeat=1, cycles=None, description="A Loop",
                 item="sequence", order="random", variable_rows=None):
        self.name = name
        self.repeat = 1
        self.variable_rows = variable_rows or []
        self.cycles = cycles or len(variable_rows)
        self.description = description
        self.item = item
        self.order = order

    def __str__(self):
        all_columns = set()
        for row in self.variable_rows:
            all_columns.update({variable.name for variable in row})
        column_order = ";".join(sorted(list(all_columns)))
        s = """define loop {name}
\tset repeat "{repeat}"
\tset description "{description}"
\tset item "{item}"
\tset column_order "{column_order}"
\tset cycles "{cycles}"
\tset order "{order}"
""".format(
            name=self.name,
            repeat=self.repeat,
            description=self.description,
            item=self.item,
            column_order=column_order,
            cycles=self.cycles,
            order=self.order)
        # Now print each variable
        for c, variable_row in enumerate(self.variable_rows):
            for variable in variable_row:
                s += '\tsetcycle {cycle} {name} "{value}"\n'.format(
                    cycle=c, name=variable.name, value=variable.value)
        s += "\trun {item}\n".format(item=self.item)
        return s


Variable = namedtuple("Variable", ["name", "value"])


def group_to_variables(group):
    variable_rows = []
    for row in group:
        variable_rows.append([Variable(name=key, value=val)
                              for (key, val) in row.items()
                              if key != "Loop_Name"])
    return variable_rows


def run(infile, outfile):
    csv_file = csv.DictReader(open(infile, 'r'))
    with open(outfile, 'w') as out:
        for (loop_name, group) in groupby(
                csv_file, lambda x: x['Loop_Name']):
            variable_rows = group_to_variables(group)
            loop = Loop(loop_name, variable_rows=variable_rows)
            out.write(str(loop))
            out.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert a CSV file to loops.')
    parser.add_argument('infile',
                        help=("The csv file to parse. The csv file should "
                              "have a column named 'Loop_Name' which will "
                              "be used to name the loop."))
    parser.add_argument('outfile',
                        help="The file to write to")
    args = parser.parse_args()
    run(args.infile, args.outfile)

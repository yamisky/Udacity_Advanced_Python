

""" 探索‘近地天体（near-Earth objects (NEOs)）数据集’ 和 ‘近地状态数据集’



命令行调用此脚本方法：

    $ python main.py {inspect,query,interactive} [args]

（1）
“inspect”：按name或primary designation查找NEO，并可选地列出该NEO的所有close approaches信息，例如：

    $ python main.py inspect --pdes 1P
    $ python main.py inspect --name Halley
    $ python main.py inspect --verbose --name Halley

（2）
“query”：搜索与给定条件匹配的close approaches信息，例如：

    $ python main.py query --date 1969-07-29
    $ python main.py query --start-date 2020-01-01 --end-date 2020-01-31 --max-distance 0.025
    $ python main.py query --start-date 2050-01-01 --min-distance 0.2 --min-velocity 50
    $ python main.py query --date 2020-03-14 --max-velocity 25 --min-diameter 0.5 --hazardous
    $ python main.py query --start-date 2000-01-01 --max-diameter 0.1 --not-hazardous
    $ python main.py query --hazardous --max-distance 0.05 --min-velocity 30

可以手动控制限制大小，或将其保存为CSV或JSON格式的输出文件：

    $ python3 main.py query --limit 5 --outfile results.csv
    $ python3 main.py query --limit 15 --outfile results.json

（3）
“interactive”：加载NEO数据库并生成一个交互式命令shell，
它可以重复执行“inspect”和“query”命令，而无需每次都等待重新加载数据库。

如果需要，可以从本地加载其他CSV或json数据，而不是使用“--neofile”或“--cadfile”的默认值。
"""


import argparse
import cmd
import datetime
import pathlib
import shlex
import sys
import time

from extract import load_neos, load_approaches
from database import NEODatabase
from filters import create_filters, limit
from write import write_to_csv, write_to_json


PROJECT_ROOT = pathlib.Path(__file__).parent.resolve()
DATA_ROOT = PROJECT_ROOT / 'data'

# 当前时间，用于交互式shell的kill on change功能。
_START = time.time()


def date_fromisoformat(date_string):
    """
    :param date_string: A date in the format YYYY-MM-DD.
    :return: A `datetime.date` correspondingo the given date string.
    """
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{date_string}' is not valid date. Use YYYY-MM-DD.")



def make_parser():
    """给这个脚本创建ArgumentParser

    :return: A tuple of the top-level, inspect, and query parsers.
    """
    parser = argparse.ArgumentParser(description="Explore past and future close approaches of near-Earth objects.")

    # Add arguments for custom data files.
    parser.add_argument('--neofile', default=(DATA_ROOT / 'neos.csv'),
                        type=pathlib.Path,
                        help="Path to CSV file of near-Earth objects.")
    parser.add_argument('--cadfile', default=(DATA_ROOT / 'cad.json'),
                        type=pathlib.Path,
                        help="Path to JSON file of close approach data.")
    subparsers = parser.add_subparsers(dest='cmd')

    # Add the `inspect` subcommand parser.
    inspect = subparsers.add_parser('inspect',
                                    description="Inspect an NEO by primary designation or by name.")
    inspect.add_argument('-v', '--verbose', action='store_true',
                         help="Additionally, print all known close approaches of this NEO.")
    inspect_id = inspect.add_mutually_exclusive_group(required=True)
    inspect_id.add_argument('-p', '--pdes',
                            help="The primary designation of the NEO to inspect (e.g. '433').")
    inspect_id.add_argument('-n', '--name',
                            help="The IAU name of the NEO to inspect (e.g. 'Halley').")

    # Add the `query` subcommand parser.
    query = subparsers.add_parser('query',
                                  description="Query for close approaches that "
                                              "match a collection of filters.")
    filters = query.add_argument_group('Filters',
                                       description="Filter close approaches by their attributes "
                                                   "or the attributes of their NEOs.")
    filters.add_argument('-d', '--date', type=date_fromisoformat,
                         help="Only return close approaches on the given date, "
                              "in YYYY-MM-DD format (e.g. 2020-12-31).")
    filters.add_argument('-s', '--start-date', type=date_fromisoformat,
                         help="Only return close approaches on or after the given date, "
                              "in YYYY-MM-DD format (e.g. 2020-12-31).")
    filters.add_argument('-e', '--end-date', type=date_fromisoformat,
                         help="Only return close approaches on or before the given date, "
                              "in YYYY-MM-DD format (e.g. 2020-12-31).")
    filters.add_argument('--min-distance', dest='distance_min', type=float,
                         help="In astronomical units. Only return close approaches that "
                              "pass as far or farther away from Earth as the given distance.")
    filters.add_argument('--max-distance', dest='distance_max', type=float,
                         help="In astronomical units. Only return close approaches that "
                              "pass as near or nearer to Earth as the given distance.")
    filters.add_argument('--min-velocity', dest='velocity_min', type=float,
                         help="In kilometers per second. Only return close approaches "
                              "whose relative velocity to Earth at approach is as fast or faster "
                              "than the given velocity.")
    filters.add_argument('--max-velocity', dest='velocity_max', type=float,
                         help="In kilometers per second. Only return close approaches "
                              "whose relative velocity to Earth at approach is as slow or slower "
                              "than the given velocity.")
    filters.add_argument('--min-diameter', dest='diameter_min', type=float,
                         help="In kilometers. Only return close approaches of NEOs with "
                              "diameters as large or larger than the given size.")
    filters.add_argument('--max-diameter', dest='diameter_max', type=float,
                         help="In kilometers. Only return close approaches of NEOs with "
                              "diameters as small or smaller than the given size.")
    filters.add_argument('--hazardous', dest='hazardous', default=None, action='store_true',
                         help="If specified, only return close approaches of NEOs that "
                              "are potentially hazardous.")
    filters.add_argument('--not-hazardous', dest='hazardous', default=None, action='store_false',
                         help="If specified, only return close approaches of NEOs that "
                              "are not potentially hazardous.")
    query.add_argument('-l', '--limit', type=int,
                       help="The maximum number of matches to return. "
                            "Defaults to 10 if no --outfile is given.")
    query.add_argument('-o', '--outfile', type=pathlib.Path,
                       help="File in which to save structured results. "
                            "If omitted, results are printed to standard output.")

    repl = subparsers.add_parser('interactive',
                                 description="Start an interactive command session "
                                             "to repeatedly run `interact` and `query` commands.")
    repl.add_argument('-a', '--aggressive', action='store_true',
                      help="If specified, kill the session whenever a project file is modified.")
    return parser, inspect, query



def inspect(database, pdes=None, name=None, verbose=False):
    """Perform the `inspect` subcommand.

    :param database: The `NEODatabase` containing data on NEOs and their close approaches.
    :param pdes: The primary designation of an NEO for which to search.
    :param name: The name of an NEO for which to search.
    :param verbose: Whether to additionally print all of a matching NEO's close approaches.
    :return: The matching `NearEarthObject`, or None if not found.
    """
    # Fetch the NEO of interest.
    if pdes:
        neo = database.get_neo_by_designation(pdes)
    else:
        neo = database.get_neo_by_name(name)

    # Ensure that we have received an NEO.
    if not neo:
        print("No matching NEOs exist in the database.", file=sys.stderr)
        return None

    # Display information about this NEO, and optionally its close approaches if verbose.
    print(neo)
    if verbose:
        for approach in neo.approaches:
            print(f"- {approach}")
    return neo


def query(database, args):
    """Perform the `query` subcommand.

    :param database: The `NEODatabase` containing data on NEOs and their close approaches.
    :param args: All arguments from the command line, as parsed by the top-level parser.
    """
    # Construct a collection of filters from arguments supplied at the command line.
    filters = create_filters(
        date=args.date, start_date=args.start_date, end_date=args.end_date,
        distance_min=args.distance_min, distance_max=args.distance_max,
        velocity_min=args.velocity_min, velocity_max=args.velocity_max,
        diameter_min=args.diameter_min, diameter_max=args.diameter_max,
        hazardous=args.hazardous
    )
    # Query the database with the collection of filters.
    results = database.query(filters)

    if not args.outfile:
        # Write the results to stdout, limiting to 10 entries if not specified.
        for result in limit(results, args.limit or 10):
            print(result)
    else:
        # Write the results to a file.
        if args.outfile.suffix == '.csv':
            write_to_csv(limit(results, args.limit), args.outfile)
        elif args.outfile.suffix == '.json':
            write_to_json(limit(results, args.limit), args.outfile)
        else:
            print("Please use an output file that ends with `.csv` or `.json`.", file=sys.stderr)




class NEOShell(cmd.Cmd):
    """交互式方法

    This is a `cmd.Cmd` shell - a specialized tool for command-based REPL sessions.

    It wraps the `inspect` and `query` parsers to parse flags for those commands
    as if they were supplied at the command line.

    The primary purpose of this shell is to allow users to repeatedly perform
    inspect and query commands, while only loading the data (which can be quite
    slow) once.
    """
    intro = ("Explore close approaches of near-Earth objects. "
             "Type `help` or `?` to list commands and `exit` to exit.\n")
    prompt = '(neo) '

    def __init__(self, database, inspect_parser, query_parser, aggressive=False, **kwargs):
        """Create a new `NEOShell`.

        Creating this object doesn't start the session - for that, use `.cmdloop()`.

        :param database: The `NEODatabase` containing data on NEOs and their close approaches.
        :param inspect_parser: The subparser for the `inspect` subcommand.
        :param query_parser: The subparser for the `query` subcommand.
        :param aggressive: Whether to kill the session whenever a project file is changed.
        :param kwargs: A dictionary of excess keyword arguments passed to the superclass.
        """
        super().__init__(**kwargs)
        self.db = database
        self.inspect = inspect_parser
        self.query = query_parser
        self.aggressive = aggressive

    @classmethod
    def parse_arg_with(cls, arg, parser):
        """Parse the additional text passed to a command, using a given parser.

        If any error is encountered (in lexical parsing or argument parsing),
        print the error to stderr and return None.

        :param arg: The additional text supplied after the command.
        :param parser: An `argparse.ArgumentParser` to parse the arguments.
        :return: A `Namespace` of the arguments (produced by `parse_args`) or None.
        """
        # Lexically parse the additional text with POSIX shell-like syntax.
        try:
            args = shlex.split(arg)
        except ValueError as err:
            print(err, file=sys.stderr)
            return None

        # Use the ArgumentParser to parse the shell arguments.
        try:
            return parser.parse_args(args)
        except SystemExit as err:
            # The `parse_args` method doesn't actually surface `ArgumentError`s
            # nor `ArgumentTypeError`s - instead, it calls its own `error`
            # method which prints the error message and then calls `sys.exit`.
            return None

    def do_i(self, arg):
        """Shorthand for `inspect`."""
        self.do_inspect(arg)

    def do_inspect(self, arg):
        """Perform the `inspect` subcommand within the REPL session.

        Inspect an NEO by designation or by name:

            (neo) inspect --pdes 1P
            (neo) inspect --name Halley

        Additionally, list all known close approaches:

            (neo) inspect --verbose --name Eros
        """
        args = self.parse_arg_with(arg, self.inspect)
        if not args:
            return

        # Run the `inspect` subcommand.
        inspect(self.db,
                pdes=args.pdes, name=args.name,
                verbose=args.verbose)

    def do_q(self, arg):
        """Shorthand for `query`."""
        self.do_query(arg)

    def do_query(self, arg):
        """Perform the `query` subcommand within the REPL session.

        This command behaves the same as the `query` subcommand from the command
        line. For example, to query close approaches on January 1st, 2020:

            (neo) query --date 2020-01-01

        You can use any of the other filters: `--start-date`, `--end-date`,
        `--min-distance`, `--max-distance`, `--min-velocity`, `--max-velocity`,
        `--min-diameter`, `--max-diameter`, `--hazardous`, `--not-hazardous`.

        The number of results shown can be limited to a maximum number with `--limit`:

            (neo) query --limit 2

        The results can be saved to a file (instead of displayed to stdout) with
        `--outfile`:

            (neo) query --limit 5 --outfile results.csv
            (neo) query --limit 5 --outfile results.json
        """
        args = self.parse_arg_with(arg, self.query)
        if not args:
            return

        # Run the `inspect` subcommand.
        query(self.db, args)

    def do_EOF(self, _arg):
        """Exit the interactive session."""
        return True

    # Alternative ways to quit.
    do_exit = do_EOF
    do_quit = do_EOF

    def precmd(self, line):
        """Watch for changes to the files in this project."""
        changed = [f for f in PROJECT_ROOT.glob('*.py') if f.stat().st_mtime > _START]
        if changed:
            print("The following file(s) have been modified since this interactive session began: "
                  f"{', '.join(str(f.relative_to(PROJECT_ROOT)) for f in changed)}.",
                  file=sys.stderr)
            if not self.aggressive:
                print("To include these changes, please exit and restart this interactive session.",
                      file=sys.stderr)
            else:
                print("Preemptively terminating the session aggressively.", file=sys.stderr)
                return 'exit'
        return line













def main():
    parser, inspect_parser, query_parser = make_parser()
    args = parser.parse_ars()

    database = NEODatabase(load_neos(args.neofile), load_approaches(args.cadfile))

    if args.cmd == 'inspect':
        inspect(database, pdes=args.pdes, name=args.name, verbose=args.verbose)

    elif args.cmd == 'query':
        query(database, args)
    
    elif args.cmd == 'interactive':
        NEOShell(database, inspect_parser, query_parser, aggressive=args.aggressive).cmdloop()



#一个python文件通常有两种使用方法，第一是直接执行该脚本，
# 第二是被其他脚本import调用（模块重用）执行。
# 在 if __name__ == 'main': 里面的代码只有在第一种情况下（即文件作为脚本直接执行）才会被执行，
if __name__ == '__main__':
    main()
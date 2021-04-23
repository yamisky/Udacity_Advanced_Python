

""" 探索‘近地天体数据集’和‘接近地球（状态）数据集’



可以从命令行调用此脚本：

    $ python main.py {inspect,query,interactive} [args]

The `inspect` subcommand looks up an NEO by name or by primary designation, and
optionally lists all of that NEO's known close approaches:

    $ python3 main.py inspect --pdes 1P
    $ python3 main.py inspect --name Halley
    $ python3 main.py inspect --verbose --name Halley

The `query` subcommand searches for close approaches that match given criteria:

    $ python3 main.py query --date 1969-07-29
    $ python3 main.py query --start-date 2020-01-01 --end-date 2020-01-31 --max-distance 0.025
    $ python3 main.py query --start-date 2050-01-01 --min-distance 0.2 --min-velocity 50
    $ python3 main.py query --date 2020-03-14 --max-velocity 25 --min-diameter 0.5 --hazardous
    $ python3 main.py query --start-date 2000-01-01 --max-diameter 0.1 --not-hazardous
    $ python3 main.py query --hazardous --max-distance 0.05 --min-velocity 30

The set of results can be limited in size and/or saved to an output file in CSV
or JSON format:

    $ python3 main.py query --limit 5 --outfile results.csv
    $ python3 main.py query --limit 15 --outfile results.json

The `interactive` subcommand loads the NEO database and spawns an interactive
command shell that can repeatedly execute `inspect` and `query` commands without
having to wait to reload the database each time. However, it doesn't hot-reload.

If needed, the script can load data from data files other than the default with
`--neofile` or `--cadfile`.
"""


import argparse
import cmd
import datetime
import pathlib
import shlex
import sys
import time



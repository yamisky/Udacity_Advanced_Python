

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
# 第二是 import 到其他的 python 脚本中被调用（模块重用）执行。
# 在 if __name__ == 'main': 下的代码只有在第一种情况下（即文件作为脚本直接执行）才会被执行，
# 而被 import 到其他脚本中是不会被执行的。
if __name__ == '__main__':
    main()
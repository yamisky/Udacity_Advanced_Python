

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

The set of results can be limited in size and/or saved to an output file in CSV
or JSON format:

    $ python3 main.py query --limit 5 --outfile results.csv
    $ python3 main.py query --limit 15 --outfile results.json

（3）
“interactive”：加载NEO数据库并生成一个交互式命令shell，
它可以重复执行“inspect”和“query”命令，而无需每次都等待重新加载数据库。

If needed, the script can load data from data files other than the default with
`--neofile` or `--cadfile`.

如果需要，可以从本地加载其他CSV或json数据，而不是使用“--neofile”或“--cadfile”的默认值。
"""


import argparse
import cmd
import datetime
import pathlib
import shlex
import sys
import time



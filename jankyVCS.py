import argparse
import tomllib
from datetime import datetime
import pathspec
import hashlib
from math import ceil
import os
import re
import sys
import zstandard as zstd

try:
    import grp, pwd
except ModuleNotFoundError:
    pass

argparser = argparse.ArgumentParser(description="The jankiest version control system. Embrace the jank!")

argsubparsers = argparser.add_subpaersers(
    title="Commands", 
    dest="command", 
    required=True
);

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
    case "init" : cmd_init(args)
    case "add" : cmd_add(args)
    case "checkout" : cmd_checkout(args)
    case "commit" : cmd_commit(args)
    case _ : print("Unknown command. Type --help for list of valid commands")
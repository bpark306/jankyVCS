from repository import GitRepository
import argparse
import configparser
import pathspec
from datetime import datetime
import hashlib
from math import ceil
import re
import sys
import zstandard as zstd

try:
    import grp, pwd
except ModuleNotFoundError:
    pass

argparser = argparse.ArgumentParser(description="The jankiest version control system. Embrace the jank!")

argsubparsers = argparser.add_subparsers(
    title="Commands", 
    dest="command", 
    required=True
);

def cmd_init(args):
    GitRepository.repo_create(args.path)

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "init" : cmd_init(args)
        case "add" : cmd_add(args)
        case "checkout" : cmd_checkout(args)
        case "commit" : cmd_commit(args)
        case _ : print("Unknown command. Type --help for list of valid commands")

argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")

argsp.add_argument("path",
                    metavar="directory",
                    nargs="?",
                    default=".",
                    help="Where to create the repository.")


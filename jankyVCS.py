from repository import GitRepository
from object import GitBlob #, GitCommit, GitTree, GitTag
import argparse
import configparser
import pathspec
from datetime import datetime
from math import ceil
import re
import sys

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

def cmd_cat_file(args):
    repo = GitRepository.repo_find()
    cat_file(repo, args.object, fmt=args.type.encode())

def cat_file(repo, obj, fmt=None):
    obj = GitRepository.read_object(repo, GitRepository.find_object(repo, obj, fmt=fmt))
    sys.stdout.buffer.write(obj.serialize())

def cmd_hash_object(args):
    if args.write:
        repo = GitRepository.repo_find()
    else:
        repo = None
    
    with open(args.path, "rb") as fd:
        sha = hash_object(fd, args.type.encode(), repo)
        print(sha)

def hash_object(fd, fmt, repo=None):
    data = fd.read()

    match fmt:
        case b'commit'  : obj=GitCommit(data)
        case b'tree'    : obj=GitTree(data)
        case b'tag'     : obj=GitTag(data)
        case b'blob'   : obj=GitBlob(data)
        case _: raise Exception(f"Unknown type {fmt}!")

    return GitRepository.write_object(obj, repo)

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "init"         : cmd_init(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "log"          : cmd_log(args)
        case _ : print("Unknown command. Type --help for list of valid commands")

argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")

argsp.add_argument("path",
                    metavar="directory",
                    nargs="?",
                    default=".",
                    help="Where to create the repository.")

argsp = argsubparsers.add_parser("cat-file", help="Provide content of repository objects")

argsp.add_argument("type",
                    metavar="type",
                    choices=["blob", "commit", "tag", "tree"],
                    help="Specify the type")

argsp.add_argument("object",
                    metavar="object",
                    help="The object to display")

argsp = argsubparsers.add_parser("hash-object",
                                help="Compute object ID and optionally creates a blob from a file")
                
argsp.add_argument("-t",
                    metavar="type",
                    dest="type",
                    choices=["blob", "commit", "tag", "tree"],
                    default="blob",
                    help="Specify the type")

argsp.add_argument("-w",
                    dest="write",
                    action="store_true",
                    help="Actually write the object into the database")

argsp.add_argument("path",
                    help="Read object from <file>")


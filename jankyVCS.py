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
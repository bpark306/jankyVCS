import os
import configparser

class GitRepository (object) :

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exeception(f"Not a Git repository {path}")

        self.conf = configparser.ConfigParser()

        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")
        
        if not force:
            vers = int(self.conf.get("core", "repositoryformationversion"))
            if vers !=0:
                raise Exception(f"Unsupported repositoryformationversion: {vers}")
    
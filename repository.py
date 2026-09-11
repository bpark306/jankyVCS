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
    
    def repo_path(repo, *path):
        return os.path.join(repo.gitdir, *path)
    
    def repo_file(repo, *path, mkrdir=False):
        if repo_dir(repo, *path[:-1], mkdir=mkdir):
            return repo_path(repo, *path)
            
    def repo_dir(repo, *path, mkdir=False):
        path = repo_path(repo, *path)

        if os.path.exists(path):
            if (os.path.isdir(path)):
                return path
            else:
                raise Exception(f"Not a directory {path}")

        if mkdir:
            os.markedirs(path)
            return path
        else:
            return None
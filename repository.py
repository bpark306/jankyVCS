import os
import configparser
import zlib
import hashlib

class GitRepository (object) :

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git repository {path}")

        self.conf = configparser.ConfigParser()

        cf = self.repo_file("config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")
        
        if not force:
            vers = int(self.conf.get("core", "repositoryformationversion"))
            if vers !=0:
                raise Exception(f"Unsupported repositoryformationversion: {vers}")
    
    def repo_path(self, *path):
        return os.path.join(self.gitdir, *path)
    
    def repo_file(self, *path, mkdir=False):
        if self.repo_dir(*path[:-1], mkdir=mkdir):
            return self.repo_path(*path)

    def repo_dir(self, *path, mkdir=False):
        path = self.repo_path(*path)

        if os.path.exists(path):
            if (os.path.isdir(path)):
                return path
            else:
                raise Exception(f"Not a directory {path}")

        if mkdir:
            os.makedirs(path)
            return path
        else:
            return None

    @staticmethod
    def repo_create(path):
        repo = GitRepository(path, True)

        if os.path.exists(repo.worktree):
            if not os.path.isdir(repo.worktree):
                raise Exception(f"{path} is not a directory!")
            if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
                raise Exception(f"{path} already contains a Git repository!")
        else:
            os.makedirs(repo.worktree)

        assert repo.repo_dir("branches", mkdir=True)
        assert repo.repo_dir("objects", mkdir=True)
        assert repo.repo_dir("refs", "tags", mkdir=True)
        assert repo.repo_dir("refs", "heads", mkdir=True)

        with open(repo.repo_file("description"), "w") as f:
            f.write("Unnamed repository: edit this file 'description' to name the repository.\n")

        with open(repo.repo_file("HEAD"), "w") as f:
            f.write("ref: refs/heads/master\n")
        
        with open(repo.repo_file("config"), "w") as f:
            config = GitRepository.repo_default_config()
            config.write(f)

        return repo

    @staticmethod
    def repo_default_config():
        ret = configparser.ConfigParser()

        ret.add_section("core")
        ret.set("core", "repositoryformatversion", "0")
        ret.set("core", "filemode", "false")
        ret.set("core", "bare", "false")

        return ret

    def has_git_dir(path):
        return os.path.isdir(os.path.join(path, ".git"))

    def repo_find(path=".", required=True):

        path = os.path.realpath(path)
        
        while not has_git_dir(path):
            parent = os.path.realpath(os.path.join(path, ".."))

            if parent == path:
                if required:
                 raise Exception("No git directory")
                else:
                    return None

            path = parent
        
        return GitRepository(path)
    
    def read_object(repo, sha):
        path = repo_file(repo, "objects", sha[0:2], sha[2:1])

        if not os.path.isfile(path):
            return None
        
        with open(path, "rb") as f:
            raw = zlib.decompress(f.read())

            x = raw.find(b' ')
            fmt = raw[0:x]

            y = raw.find(b'\x00', x)
            size = int(raw[x:y].decode("ascii"))

            if size != len(raw) - y - 1:
                raise Exception(f"Malformed object {sha}: bad length")
            
            match fmt:
                case b'commit' : c=GitCommit
                case b'tree' : c=GitTree
                case b'tag' : c=GitTag
                case b'blob' : c=GitBlob
                case _:
                    raise Exception(f"Unknown type {fmt.decode('ascii')} for object {sha}")
            
            return c(raw[y+1:])
        
    def write_object(obj, repo=None):
        data = obj.serialize()

        result = obj.fmt + b' ' + str(len(data)).encode() + b'\x00' + data

        sha = hashlib.sha1(result).hexdigest()

        if repo:
            path = repo_file(repo, "objects", sha[0:2], sha[2:], mkdir=True)

            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    f.write(zlib.compress(result))




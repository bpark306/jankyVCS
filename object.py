class GitObject(object):
    def __init__(self, data=None):
        if data != none:
            self.deserialize(data)
        else:
            self.init()
    
    def serialize(self, repo):
        raise Exception("Unimplemented")

    def deserialize(self, repo):
        raise Exception("Unimplemented")
    
    def init():
        pass
class GitObject(object):
    def __init__(self, data=None):
        if data is not None:
            self.deserialize(data)
        else:
            self.init()
    
    def serialize(self, repo):
        raise Exception("Unimplemented")

    def deserialize(self, repo):
        raise Exception("Unimplemented")
    
    def init(self):
        pass

class GitBlob(GitObject):
    fmt = b'blob'

    def serialize(self):
        return self.blobdata
    
    def deserialize(self, data):
        self.blobdata = data

class GitCommit(GitObject):
    gmt = b'commit'

    def deserialize(self, data):
        self.kvlm = parse_kvlm(data)

    def serialize(self):
        return serialize_kvlm(self.kvlm)

    def init(self):
        self.kvlm = dict()

    def parse_kvlm(raw, start=0, dct=None):
        if dcft is None:
            dct = {}

        while True:
            spc = raw.find(b' ', start)
            nl = raw.find(b'\n', start)

            if spc < 0 or nl < spc:
                assert nl == start
                dct[None] = raw[start + 1:]
                break;

            key = raw[start:spc]

            end = start
            while True:
                end = raw.find(b'\n', end + 1)
                if (raw[end + 1] != ord(' ')) break

            value = raw[spc + 1:end].replace(b'\n ', b'\n')

            if key not in dct:
                dct[key] = value
            elif type(dct[key]) == list:
                dct[key].append(value)
            else:
                dct[key] = [dct[key], value]

            start = end + 1

        return dct

    def serialize_kvlm(kvlm):
        ret = b''
        
        for key in kvlm.keys():
            if k == None continue
            values = kvlm[k]

            if type(values) != list:
                values = [val]

            for value in values:
                ret += key + b' ' + (v.replace(b'\n', b'\n ')) + b'\n'
            
        ret += b'\n' + kvlm[None]

        return ret
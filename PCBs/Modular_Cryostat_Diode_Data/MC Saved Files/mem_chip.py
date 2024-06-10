import ujson

class Memory:
    def __init__(self):
        # implememtn memory as a bytearray... with slice access
        self.maxsize = 1<<8
        self.mem = bytearray(self.maxsize)
        for i in range(10):
            self.mem[i]=i
    def __getsliceattributes__(self, key):
        # micropython doesn't let you access slice attributes
        #  This code extracts the attributes from the string representation of the slice
        key_string = str(key)
        key_string = key_string.split('slice')[-1].replace('(','[').replace(')',']')
        key_string = key_string.replace('None','null')
        #print('key_string', key_string)
        start, stop, step = ujson.loads(key_string)
        #print('parse slice', start, stop, step)
        start, stop, step = start or 0, stop or self.maxsize, step or 1
        if step>1:
            raise NotImplementedError('only slices with step=1 (aka None) are supported')
        return start, stop, step
    def __getitem__(self,key):
        #print(type(key), key)
        if isinstance(key, int):
            return self.mem[key]
        if isinstance(key, slice):
            start, stop, step = self.__getsliceattributes__(key)
            #print('slice attributes',start, stop, step)
            return self.mem[key]
    
    def __setitem__(self, key, value):
        #print('setitem', key, value)
        start, stop, step = self.__getsliceattributes__(key)
        #print('slice attributes',start, stop, step)
        self.mem[start:stop] = value

#---------------
# Test if slicing is working
f = Memory()
stuff = f[:]
stuff = f[:10]
print(f[:10])
#
# bytearray(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t')
#
f[:5]=b'12345'
print(f[:10])
#
#  bytearray(b'12345\x05\x06\x07\x08\t')
#

#stuff = f[::2]
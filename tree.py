from collections import deque


class Node(object):
    def __init__(self):
        self.bits = ''
        self.data = ''
        self.c0 = None
        self.c1 = None
        self.root = None
        self.count=0

        self.branch_bits = ''
        self.parents = deque([])
        self.path = deque([])
        self.prev_bits = ''
        self.prev_root = None


    def longest_common_substring(self,s1, s2):
        m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
        longest, x_longest = 0, 0
        for x in xrange(1, 1 + len(s1)):
            for y in xrange(1, 1 + len(s2)):
                if s1[x - 1] == s2[y - 1]:
                    m[x][y] = m[x - 1][y - 1] + 1
                    if m[x][y] > longest:
                        longest = m[x][y]
                        x_longest = x
                else:
                    m[x][y] = 0
        return s1[x_longest - longest: x_longest]

    def has_Key(self,key):
        return ''

    def insert_Item(self,key,datastr):
        # Single node case, where only one key has already been inserted,root points to leaf node
        if (self.count == 1):
            self.prev_root = self.root      #save prev root
            self.prev_bits = self.root.bits #save prev node's bits or key
            i = Node()           # create new inner node
            common = self.longest_common_substring(self.prev_bits,key) #function call to determine common bits
            i.bits = common
            self.root = i                                  # set new self.root as inner node
            n = Node()                     # create new leaf node
            n.bits = key
            n.data= datastr
            if(self.prev_bits[len(common)] == '0'):
                self.root.c0 = self.prev_root
                self.root.c1 = n
            else:
                self.root.c1 = self.prev_root
                self.root.c0 = n

            self.root.c0.bits = self.root.c0.bits[len(common) + 1:]#remove common bits + branch bit from old or new node
            self.root.c1.bits = self.root.c1.bits[len(common) + 1:]#remove common bits + branch bit from old or new node

        # inner node with empty bits
        elif(self.root.bits == ''):  #and (self.root.c0 != None or self.root.c1 != None) ):
            #First find the appropriate place to insert the new key
            msb = key[0]
            self.branch_bits += msb
            self.parents.append(self.root)
            self.path.append(msb)
            if (msb == '1'):
                #while (self.root.c1 != None)
                        
                self.c1.insert_Item(key[1:], datastr) #eventually takes you to leaf
            elif (msb == '0'):
                self.c0.insert_Item(key[1:], datastr) #eventually takes you to leaf
            else:
                i = Node()  # create new inner node
                n = Node()  # create new leaf node
                n.bits = key
                n.data = datastr
                current = self.parents[-1]
                if (current.c1.bits[-1] == '0'):
                    i.c0 = self.root.c1
                    i.c1 = n
                else:
                    i.c1 = self.root.c0
                    i.c0 = n

                i.c0.bits = self.root.c0.bits[len(common) + 1:]  # remove common bits + branch bit from old or new node
                i.c1.bits = self.root.c1.bits[len(common) + 1:]  # remove common bits + branch bit from old or new node
                i.bits = common

                # update the parent of i
                if len(self.parents) != 0:
                    parent = self.parents.pop()
                    path_prev_bit = self.path.pop()
                    if (path_prev_bit[-1] == '0'):
                        parent.c0 = i  # check whether c0 or c1
                    else:
                        parent.c1 = i  # check whether c0 or c1
                else:
                    self.root = i

        # inner node with non-empty bits
        elif (self.bits != ''): #and (self.root.c0 != None or self.root.c1 != None)):  # inner node with bits
            self.prev_bits = self.branch_bits + self.bits
            common = self.longest_common_substring(self.prev_bits, key[0:len(self.prev_bits)])

            if (common == '' or  ( len(common) < len(self.bits) ) ): #insert new inner node above this inner node (Github C=1111 insertion)
                i = Node()  # create new inner node
                n = Node()  # create new leaf node
                n.bits = key
                n.data = datastr
                if len(self.path) != 0:
                    path_prev_bit = self.path.pop()
                    if path_prev_bit == '0':
                        i.c0 = self.root
                        i.c1 = n
                    else:
                        i.c1 = self.root
                        i.c0 = n

                if self.bits[0] == '0':
                    i.c0 = self.root
                    i.c1 = n
                else:
                    i.c1 = self.root
                    i.c0 = n

                i.bits = common ##double check this value
                self.root.bits = self.root.bits[len(common)+1:]

                #prev_bits = prev_bits[len(common) + 1:]  # remove common bits + branch bit from old node
                #self.root.bits = self.root.bits[1:] #decrease bit due to branching
                n.bits = key[len(common) + 1:]  # remove common bits + branch bit from new node

                # update the parent of i
                if len(self.parents) != 0:
                    parent = self.parents.pop()
                    path_prev_bit = self.path.pop()
                    if(path_prev_bit == '0'):
                        parent.c0 = i  # check whether c0 or c1
                    else:
                        parent.c1 = i  # check whether c0 or c1
                else:
                    self.root = i

            elif (len(common) == len(self.bits)):
                msb = key[len(common)]
                self.branch_bits = self.prev_bits + msb
                self.parents.append(self.root)
                self.path.append(self.branch_bits)
                if (msb == '1'):
                    self.root.c1.insert_Item(key[len(common)+1:], datastr)  # eventually takes you to leaf
                elif (msb == '0'):
                    self.root.c0.insert_Item(key[len(common)+1:], datastr)  # eventually takes you to leaf
                else:
                    i = Node()  # create new inner node
                    n = Node()  # create new leaf node
                    n.bits = key
                    n.data = datastr
                    current = self.parents[-1]
                    if (current.c1.bits[-1] == '0'):
                        i.c0 = self.root.c1
                        i.c1 = n
                    else:
                        i.c1 = self.root.c0
                        i.c0 = n

                    i.c0.bits = self.root.c0.bits[len(common) + 1:]  # remove common bits + branch bit from old or new node
                    i.c1.bits = self.root.c1.bits[len(common) + 1:]  # remove common bits + branch bit from old or new node
                    i.bits = common

                    # update the parent of i
                    if len(self.parents) != 0:
                        parent = self.parents.pop()
                        path_prev_bit = self.path.pop()
                        if (path_prev_bit[-1] == '0'):
                            parent.c0 = i  # check whether c0 or c1
                        else:
                            parent.c1 = i  # check whether c0 or c1
                    else:
                        self.root = i

        # clean up
        self.branch_bits = ''
        self.parents = deque([])
        self.path = deque([])
        #self.prev_bits = ''
        #self.prev_root = None


    def insert(self,key,datastr):
        if (self.root == None):
            n = Node()
            self.root = n
            self.root.bits = key
            self.root.data = datastr
            self.count += 1
        else:
            #if self.has_Key(key) == '': #Key does not already exist
            self.insert_Item(key,datastr)
            self.count +=1
            #else:
            #    print "Key already present"




if __name__ == '__main__':
    t = Node()
    t.insert('0000','A')
    t.insert('0001','B')
    t.insert('0010','C')
    t.insert('0011','D')
    t.insert('0100','E')
    t.insert('0101','F')
    t.insert('0110','G')


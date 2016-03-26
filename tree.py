from collections import deque


class Node(object):
    def __init__(self,bits,data):
        self.bits = bits
        self.data = data


class Inner(object):
    def __init__(self):
        self.bits = ''
        self.c0  = None
        self.c1 = None


class Tree(object):
    def __init__(self):
        self.root = None

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
        if (len(self.root.bits) == 4):
            self.prev_root = self.root      #save prev root
            self.prev_bits = self.root.bits #save prev node's bits or key
            i = Inner()           # create new inner node
            common = self.longest_common_substring(self.prev_bits,key) #function call to determine common bits
            i.bits = common
            self.root = i                                  # set new root as inner node
            n = Node(key,datastr)                     # create new leaf node
            if(self.prev_bits[len(common)] == '0'):
                self.root.c0 = self.prev_root
                self.root.c1 = n
            else:
                self.root.c1 = self.prev_root
                self.root.c0 = n

            self.root.c0.bits = self.root.c0.bits[len(common) + 1:]#remove common bits + branch bit from old or new node
            self.root.c1.bits = self.root.c1.bits[len(common) + 1:]#remove common bits + branch bit from old or new node

        # inner node with empty bits
        elif(self.root.bits == '' and (self.root.c0 != None or self.root.c1 != None) ):
            #First find the appropriate place to insert the new key
            msb = key[0]
            self.branch_bits += msb
            self.parents.append(self.root)
            self.path.append(msb)
            if (msb):
                self.root.c0.insert_Item(key[1:], datastr) #eventually takes you to leaf
            else:
                self.root.c1.insert_Item(key[1:], datastr) #eventually takes you to leaf

        # inner node with non-empty bits
        elif (self.root.bits != '' and (self.root.c0 != None or self.root.c1 != None)):  # inner node with bits
            self.prev_bits = self.branch_bits + self.root.bits
            common = self.longest_common_substring(self.prev_bits, key[0:len(self.prev_bits)])

            if (common == '' or  ( len(common) < len(self.root.bits) ) ): #insert new inner node above this inner node (Github C=1111 insertion)
                i = Inner()  # create new inner node
                n = Node(key, datastr)  # create new leaf node

                if len(self.path) != 0:
                    path_prev_bit = self.path.pop()
                    if path_prev_bit == '0':
                        i.c0 = self.root
                        i.c1 = n
                    else:
                        i.c1 = self.root
                        i.c0 = n

                if self.root.bits[0] == '0':
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

            elif (len(common) == len(self.root.bits)):
                msb = key[len(common)]
                self.branch_bits = self.prev_bits + msb
                self.parents.append(self.root)
                self.path.append(self.branch_bits)
                if (msb):
                    if(isinstance(self.root.c1,Inner)):
                        self.root.c1.insert_Item(key[len(common)+1:], datastr)  # eventually takes you to leaf
                    else:
                        i = Inner()  # create new inner node
                        n = Node(key, datastr)  # create new leaf node
                        current = self.parents[-1]
                        if (current.c1.bits == '0'):
                            i.c0 = self.root.c1
                            i.c1 = n
                        else:
                            i.c1 = self.root.c0
                            i.c0 = n

                        i.c0.bits = self.root.c0.bits[len(common) + 1:]  # remove common bits + branch bit from old or new node
                        i.c1.bits = self.root.c1.bits[len(common) + 1:]  # remove common bits + branch bit from old or new node


                        # update the parent of i
                        if len(self.parents) != 0:
                            parent = self.parents.pop()
                            path_prev_bit = self.path.pop()
                            if (path_prev_bit == '0'):
                                parent.c0 = i  # check whether c0 or c1
                            else:
                                parent.c1 = i  # check whether c0 or c1
                        else:
                            self.root = i
                else:
                    if (isinstance(self.root.c0, Inner)):
                        self.root.c0.insert_Item(key[len(common)+1:], datastr)  # eventually takes you to leaf
                    else:
                        i = Inner()  # create new inner node
                        n = Node(key, datastr)  # create new leaf node
                        current = self.parents[-1]
                        if (current.c1.bits == '0'):
                            i.c0 = self.root.c1
                            i.c1 = n
                        else:
                            i.c1 = self.root.c0
                            i.c0 = n

                        i.c0.bits = self.root.c0.bits[
                                    len(common) + 1:]  # remove common bits + branch bit from old or new node
                        i.c1.bits = self.root.c1.bits[
                                    len(common) + 1:]  # remove common bits + branch bit from old or new node

                        # update the parent of i
                        if len(self.parents) != 0:
                            parent = self.parents.pop()
                            path_prev_bit = self.path.pop()
                            if (path_prev_bit == '0'):
                                parent.c0 = i  # check whether c0 or c1
                            else:
                                parent.c1 = i  # check whether c0 or c1
                        else:
                            self.root = i


        #elif ( isinstance(self.root,Node) and len(self.root.bits) < 4  ):  # leaf node reached
        #    # create inner node in place of leaf node
        #    self.prev_bits = self.branch_bits + self.root.bits  # this retrieves leaf node's key
        #    i = Inner()  # create new inner node
        #    common = self.longest_common_substring(self.prev_bits, key)
            #i.bits = common
        #    n = Node(key, datastr)  # create new leaf node
        #    if (self.prev_bits[len(common) + 1] == '0'):
        #        i.c0 = self.root
        #        i.c1 = n
        #    else:
        #        i.c1 = self.root
        #        i.c0 = n
        #    self.prev_bits = self.prev_bits[len(common) + 1:]  # remove common bits + branch bit from old node
        #    n.bits = key[len(common) + 1:]  # remove common bits + branch bit from new node
        #    # update the parent of i
        #    parent = self.parents.pop()
        #    parent.c0 = i  # check whether c0 or c1
        #    i.bits = common[1:]  # remove MSB bits from the inner node as it got moved to the branch
        #    # check if you need to borrow bit
        #    parent.bits = i.bits[0]
        #    i.bits = i.bits[1:]  # check if an expression is needed instead of ''


        # clean up
        self.branch_bits = ''
        self.parents = deque([])
        self.path = deque([])
        self.prev_bits = ''
        self.prev_root = None

    ############################
    def insert(self,key,datastr):
        if (self.root == None):
            n = Node(key,datastr)
            self.root = n
        else:
            #if self.has_Key(key) == '': #Key does not already exist
            self.insert_Item(key,datastr)
            #else:
            #    print "Key already present"




if __name__ == '__main__':
    t = Tree()
    t.insert('0000','A')
    t.insert('0001','B')
    t.insert('0010','C')
    t.insert('0011','D')
    t.insert('0100','E')



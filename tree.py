from collections import deque
from hashlib import md5


ans =[] #for hashing

class Node(object):
    def __init__(self,bits,data):
        self.bits = bits
        self.data = data
        self.c1=None
        self.c0=None


class Inner(object):
    def __init__(self):
        self.bits = ''
        self.c0  = None
        self.c1 = None


class Tree(object):
    def __init__(self):
        self.root = None

        self.branch_bits = ''
        self.key_bits = ''
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
                    if (x==1 and y==1):
                        return ''
        return s1[x_longest - longest: x_longest]

    def has_Key(self,key):
        if(self.root.bits == key):
            print "->"+self.root.data
        else:
            while(isinstance(self.root,Node) == False):
                if self.root.bits == '':
                    if(key[0] == '0'):
                        self.root = self.root.c0
                    else:
                        self.root = self.root.c1
                    key=key[1:]
                else:
                    key=key[len(self.root.bits):]
                    if (key[0] == '0'):
                        self.root = self.root.c0
                    else:
                        self.root = self.root.c1
            if(self.root.data != ''):
                print"->"+self.root.data
            else:
                print "not found"




    def insert_Item(self,key,datastr):
        # Single node case, where only one key has already been inserted,root points to leaf node
        if (len(self.root.bits) == 4):
            self.prev_root = self.root      #save prev root
            self.prev_bits = self.root.bits #save prev node's bits or key
            i = Inner()                     # create new inner node
            common = self.longest_common_substring(self.prev_bits,key) #function call to determine common bits
            i.bits = common
            self.root = i                             # set new root as inner node
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
            self.key_bits +=msb
            self.parents.append(self.root)
            self.path.append(msb)
            if (msb == '1'):
                if (isinstance(self.root.c1, Inner)):
                    current = self.root.c1
                    # self.parents.append(current)
                    j = 0
                    if (current.bits != '' and current.bits != key[len(self.branch_bits):len(current.bits)+1]):
                        # insert before current
                        i = Inner()  # create new inner node
                        n = Node(key, datastr)  # create new leaf node
                        current2 = self.parents[-1]
                        if (current2.c1.bits[0] == '0'):
                            i.c0 = current2.c1
                            i.c0.bits = i.c0.bits[1:]  # decrease inner node bits by 1 for branching
                            if (len(i.c0.bits) == 1 and i.c0.bits != '1'):
                                i.bits = i.c0.bits[0]
                                i.c0.bits = i.c0.bits[len(self.branch_bits) + len(i.bits):]
                                self.branch_bits += i.bits
                            i.c1 = n
                            self.branch_bits += '1'
                        else:
                            i.c1 = current2.c1
                            i.c1.bits = i.c1.bits[1:] # decrease inner node bits by 1
                            if (len(i.c1.bits) == 1 and i.c1.bits != '1'):
                                i.bits = i.c1.bits[0]
                                i.c1.bits = i.c1.bits[len(self.branch_bits) + len(i.bits):]
                                self.branch_bits += i.bits
                            self.branch_bits += '0'
                            i.c0 = n

                        n.bits = n.bits[len(self.branch_bits):]  # traverse bits + branch bit

                        # update the parent of i
                        if len(self.parents) != 0:
                            parent = self.parents.pop()
                            path_prev_bit = self.path.pop()
                            if (path_prev_bit[-1] == '0'):
                                parent.c0 = i
                            else:
                                parent.c1 = i
                        else:
                            self.root = i
                    else:
                        self.parents.append(current)
                        self.branch_bits += current.bits
                        self.key_bits += current.bits
                        while (isinstance(current, Node) == False and self.branch_bits[-1] == key[len(self.branch_bits)-1]):
                            if key[len(self.branch_bits) + j] == '0':
                                current = current.c0
                                self.branch_bits += '0'
                            else:
                                current = current.c1
                                self.branch_bits += '1'
                            self.path.append(key[len(self.key_bits) + j])
                            self.key_bits += key[len(self.key_bits) + j]
                            self.branch_bits += current.bits
                            self.parents.append(current)
                            j = j + 1

                        # leaf node reached
                        i = Inner()             # create new inner node
                        n = Node(key, datastr)  # create new leaf node
                        current2 = self.parents[-1]
                        if (current2.bits[0] == '0'):
                            i.c0 = current2
                            i.c0.bits = i.c0.bits[1:]   #for branching
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits,key[len(self.key_bits):len(self.key_bits)+len(i.c0.bits)])  # i.c0.bits[0]
                                i.c0.bits = i.c0.bits[len(self.branch_bits) + len(i.bits):]
                                self.key_bits += i.bits
                            self.key_bits += '1'
                            i.c1 = n
                        else:
                            i.c0 = current2
                            i.c0.bits = i.c0.bits[1:] #for branching
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(self.key_bits):len(self.key_bits)+len(i.c0.bits)])  # i.c1.bits
                                i.c0.bits = i.c0.bits[len(self.branch_bits) + len(i.bits):]
                                self.key_bits += i.bits
                            self.key_bits += '0'
                            i.c1 = n

                        n.bits = n.bits[len(self.key_bits):]  # traverse bits + branch bit

                        # update the parent of i
                        if len(self.parents) != 0:
                            self.parents.pop()  # discard the last value
                            parent = self.parents.pop()
                            path_prev_bit = self.path.pop()
                            if (path_prev_bit[-1] == '0'):
                                parent.c0 = i  # check whether c0 or c1
                            else:
                                parent.c1 = i  # check whether c0 or c1
                        else:
                            self.root = i

                else:            # leaf node reached
                    i = Inner()  # create new inner node
                    n = Node(key, datastr)  # create new leaf node
                    current2 = self.parents[-1]
                    if (current2.c1.bits[0] == '0'):
                        i.c0 = current2.c1
                        i.c1 = n
                        i.c0.bits = i.c0.bits[1:]   #remove for branching
                        if (len(i.c0.bits) != 0):
                            i.bits = self.longest_common_substring(i.c0.bits,key[len(self.branch_bits):len(self.branch_bits)+len(i.c0.bits)])#i.c0.bits[0]
                            i.c0.bits = i.c0.bits[len(self.branch_bits)+len(i.bits):]
                            self.branch_bits += i.bits
                        self.branch_bits += '1'
                    else:
                        i.c0 = current2.c0
                        i.c0.bits = i.c0.bits[1:]
                        if (len(i.c0.bits) != 0):
                            i.bits = self.longest_common_substring(i.c0.bits,key[len(self.branch_bits):len(self.branch_bits)+len(i.c0.bits)])#i.c1.bits
                            i.c0.bits = i.c0.bits[len(self.branch_bits)+len(i.bits):]
                            self.branch_bits += i.bits
                        self.branch_bits += '0'
                        i.c1 = n

                    n.bits = key[len(self.branch_bits):]

                    # update the parent of i
                    if len(self.parents) != 0:
                        parent = self.parents.pop()
                        path_prev_bit = self.path.pop()
                        if (path_prev_bit[-1] == '0'):
                            parent.c0 = i
                        else:
                            parent.c1 = i
                    else:
                        self.root = i

            elif (msb == '0'):
                if (isinstance(self.root.c0, Inner)):
                    current = self.root.c0
                    j = 0
                    if (current.bits != '' and current.bits != key[len(self.branch_bits):len(current.bits)+1]):
                        # insert before current
                        i = Inner()  # create new inner node
                        n = Node(key, datastr)  # create new leaf node
                        current2 = self.parents[-1]

                        if (current2.c1.bits[0] == '0'):
                            i.c0 = current2.c1
                            i.c0.bits = i.c0.bits[1:]
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(self.key_bits):len(self.key_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                                i.c0.bits = i.c0.bits[len(self.branch_bits) + len(i.bits):]
                                self.branch_bits += i.bits
                            self.branch_bits += '1'
                            i.c1 = n
                        else:
                            # i.c1 = current2.c0  # self.root.c0  # decrease inner node bits by 1
                            # i.c1.bits = ''
                            # i.c0 = n
                            i.c0 = current2.c0
                            i.c0.bits = i.c0.bits[1:]
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(self.key_bits):len(self.key_bits) + len(i.c0.bits)])  # i.c1.bits
                                i.c0.bits = i.c0.bits[len(self.branch_bits) + len(i.bits):]
                                self.branch_bits += i.bits
                            self.branch_bits += '0'
                            i.c1 = n

                        n.bits = n.bits[len(self.branch_bits):]  # traverse bits + branch bit

                        # update the parent of i
                        if len(self.parents) != 0:
                            parent = self.parents.pop()
                            path_prev_bit = self.path.pop()
                            if (path_prev_bit[-1] == '0'):
                                parent.c0 = i
                            else:
                                parent.c1 = i
                        else:
                            self.root = i
                    else:
                        self.parents.append(current)
                        self.branch_bits += current.bits #if any
                        self.key_bits += current.bits
                        while (isinstance(current, Node) == False and self.branch_bits[-1] == key[len(self.branch_bits)-1]) :
                            if key[len(self.branch_bits) + j] == '0':
                                current = current.c0
                                self.branch_bits += '0'
                            else:
                                current = current.c1
                                self.branch_bits += '1'
                            self.path.append(key[len(self.key_bits) + j])
                            self.branch_bits += current.bits
                            self.key_bits+= key[len(self.key_bits) + j]
                            self.parents.append(current)
                            j = j + 1

                                                # leaf node reached
                        i = Inner()             # create new inner node
                        n = Node(key, datastr)  # create new leaf node
                        current2 = self.parents[-1]
                        if (current2.bits[0] == '0'):
                            i.c0 = current2
                            i.c0.bits = i.c0.bits[1:]
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(self.key_bits):len(self.key_bits)+len(i.c0.bits)])  # i.c0.bits[0]
                                i.c0.bits = i.c0.bits[len(self.branch_bits) + len(i.bits):]
                                self.key_bits += i.bits
                            self.key_bits += '1'
                            i.c1 = n
                        else:
                            i.c0 = current2
                            i.c0.bits = i.c0.bits[1:]
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(self.key_bits):len(self.key_bits)+len(i.c0.bits)])  # i.c1.bits
                                i.c0.bits = i.c0.bits[len(self.branch_bits) + len(i.bits):]
                                self.key_bits += i.bits
                            self.key_bits += '0'
                            i.c1 = n

                        n.bits = n.bits[len(self.key_bits):]  # traverse bits + branch bit

                        # update the parent of i
                        if len(self.parents) != 0:
                            self.parents.pop()  # discard the last value
                            parent = self.parents.pop()
                            path_prev_bit = self.path.pop()
                            if (path_prev_bit[-1] == '0'):
                                parent.c0 = i
                            else:
                                parent.c1 = i
                        else:
                            self.root = i

                else:  # leaf node reached
                    i = Inner()  # create new inner node
                    n = Node(key, datastr)  # create new leaf node
                    current2 = self.parents[-1]
                    if (current2.c1.bits[0] == '0'):  # 0 vs -1
                        i.c0 = current2.c1
                        i.c0.bits = i.c0.bits[1:]
                        if (len(i.c0.bits) != 0):
                            i.bits = self.longest_common_substring(i.c0.bits, key[len(self.branch_bits):len(self.branch_bits)+len(i.c0.bits)])  # i.c0.bits[0]
                            i.c0.bits = i.c0.bits[len(self.branch_bits) + len(i.bits):]
                            self.branch_bits += i.bits
                        self.branch_bits += '1'
                        i.c1 = n
                    else:
                        i.c0 = current2.c0
                        i.c0.bits = i.c0.bits[1:]
                        if (len(i.c0.bits) != 0):
                            i.bits = self.longest_common_substring(i.c0.bits, key[len(self.branch_bits):len(self.branch_bits)+len(i.c0.bits)])  # i.c1.bits
                            i.c0.bits = i.c0.bits[len(self.branch_bits) + len(i.bits):]
                            self.branch_bits += i.bits
                        self.branch_bits += '0'
                        i.c1 = n

                    n.bits = key[len(self.branch_bits):]

                    # update the parent of i
                    if len(self.parents) != 0:
                        parent = self.parents.pop()
                        path_prev_bit = self.path.pop()
                        if (path_prev_bit[-1] == '0'):
                            parent.c0 = i
                        else:
                            parent.c1 = i
                    else:
                        self.root = i

        # inner node with non-empty bits
        elif (self.root.bits != '' and (self.root.c0 != None or self.root.c1 != None)):  # inner node with bits
            self.prev_bits = self.branch_bits + self.root.bits
            common = self.longest_common_substring(self.prev_bits, key[0:len(self.prev_bits)])

            if (common == '' or  ( len(common) < len(self.root.bits) ) ): #insert new inner node above this inner node
                i = Inner()  # create new inner node
                n = Node(key, datastr)  # create new leaf node

                if len(self.path) != 0:
                    path_prev_bit = self.path.pop()
                    if path_prev_bit[-1] == '0':
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

                i.bits = common
                self.root.bits = self.root.bits[len(common)+1:]
                n.bits = key[len(common) + 1:]  # remove common bits + branch bit from new node

                # update the parent of i
                if len(self.parents) != 0:
                    parent = self.parents.pop()
                    path_prev_bit = self.path.pop()
                    if(path_prev_bit[-1] == '0'):
                        parent.c0 = i
                    else:
                        parent.c1 = i
                else:
                    self.root = i
            #!if (common == '' or  ( len(common) < len(self.root.bits) ) )
            elif (len(common) == len(self.root.bits)): #traverse to find the insert spot
                msb = key[len(common)]
                self.branch_bits = self.prev_bits + msb
                self.parents.append(self.root)
                self.path.append(self.branch_bits)
                if (msb =='1'):
                    if(isinstance(self.root.c1,Inner)):
                        current = self.root.c1
                        j=0
                        if (current.bits != '' and current.bits != key[len(common)+1]):
                            #insert before current
                            i = Inner()  # create new inner node
                            n = Node(key, datastr)  # create new leaf node
                            current2 = self.parents[-1]
                            if (current2.c1.bits[0] == '0' ): #[0] vs [-1]
                                i.c0 = current2.c1#self.root.c1
                                i.c0.bits = i.c0.bits[1:]   #decrease inner node bits by 1
                                i.c1 = n
                                self.branch_bits += '1'
                            else:
                                i.c1 = current2.c1#self.root.c0 #decrease inner node bits by 1
                                i.c1.bits = i.c1.bits[1:]
                                self.branch_bits += '0'
                                i.c0 = n


                            i.bits = ''
                            n.bits = n.bits[len(self.branch_bits):] #traverse bits + branch bit

                            # update the parent of i
                            if len(self.parents) != 0:
                                parent = self.parents.pop()
                                path_prev_bit = self.path.pop()
                                if (path_prev_bit[-1] == '0'):
                                    parent.c0 = i
                                else:
                                    parent.c1 = i
                            else:
                                self.root = i
                        else:
                            self.parents.append(current)
                            while( isinstance(current,Node) == False ):
                                if key[len(self.branch_bits)+j] == '0':
                                    current = current.c0
                                else:
                                    current = current.c1
                                self.path.append(key[len(self.branch_bits)+j])
                                self.branch_bits += key[len(self.branch_bits)+j]
                                self.parents.append(current)
                                j = j + 1
                            #Now insert

                            #leaf node reached
                            i = Inner()  # create new inner node
                            n = Node(key, datastr)  # create new leaf node
                            current2 = self.parents[-1]
                            if (current2.bits[0] == '0'):  #[-1] vs [0]
                                i.c0 = current2
                                i.c0.bits = i.c0.bits[1:]
                                self.branch_bits += '1'
                                i.c1 = n
                            else:
                                i.c1 = current2
                                i.c1.bits = i.c1.bits[1:]
                                self.branch_bits += '0'
                                i.c0 = n

                            i.bits = ''  # double check
                            n.bits = n.bits[len(self.branch_bits):]  # traverse bits + branch bit

                            # update the parent of i
                            if len(self.parents) != 0:
                                self.parents.pop()  # discard the last value
                                parent = self.parents.pop()
                                path_prev_bit = self.path.pop()
                                if (path_prev_bit[-1] == '0'):
                                    parent.c0 = i
                                else:
                                    parent.c1 = i
                            else:
                                self.root = i

                    else:   #leaf node reached
                        i = Inner()  # create new inner node
                        n = Node(key, datastr)  # create new leaf node
                        current2 = self.parents[-1]
                        if (len(current2.c1.bits) != 0): #[0]  vs [-1] if (len(current2.c1.bits) != 0):
                            if(current2.c1.bits[0] == '0'):
                                i.c0 = current2.c1
                                i.c0.bits = i.c0.bits[1:]
                                if(len(i.c0.bits) != 0):
                                    i.bits = i.c0.bits[0]
                                    i.c0.bits = i.c0.bits[1:]
                                    self.branch_bits += i.bits
                            self.branch_bits += '1'
                            i.c1 = n
                        else:
                            i.c1 = current2.c0
                            i.c1.bits = i.c1.bits[1:]
                            if (len(i.c1.bits) != 0):
                                i.bits = i.c1.bits
                                i.c1.bits = i.c1.bits[1:]
                                self.branch_bits += i.bits
                            self.branch_bits += '0'
                            i.c0 = n

                        n.bits = key[len(self.branch_bits):]

                        # update the parent of i
                        if len(self.parents) != 0:
                            parent = self.parents.pop()
                            path_prev_bit = self.path.pop()
                            if (path_prev_bit[-1] == '0'):
                                parent.c0 = i
                            else:
                                parent.c1 = i
                        else:
                            self.root = i


                elif (msb == '0'):
                    if (isinstance(self.root.c0, Inner)):
                        current = self.root.c0
                        j = 0
                        if (current.bits != '' and current.bits != key[len(common) + 1]):
                            # insert before current
                            i = Inner()  # create new inner node
                            n = Node(key, datastr)  # create new leaf node
                            current2 = self.parents[-1]
                            if (current2.c0.bits[-1] == '0'):
                                i.c0 = current2.c0#self.root.c0
                                i.c0.bits = ''  # decrease inner node bits by 1
                                i.c1 = n
                            else:
                                i.c1 = current2.c0# decrease inner node bits by 1
                                i.c1.bits = ''
                                i.c0 = n
                            i.bits = ''  # double check
                            n.bits = n.bits[len(self.branch_bits):]  # traverse bits + branch bit

                            # update the parent of i
                            if len(self.parents) != 0:
                                parent = self.parents.pop()
                                path_prev_bit = self.path.pop()
                                if (path_prev_bit[-1] == '0'):
                                    parent.c0 = i
                                else:
                                    parent.c1 = i
                            else:
                                self.root = i
                        else:
                            self.parents.append(current)
                            while (isinstance(current, Node) == False):
                                if key[len(self.branch_bits) + j] == '0':
                                    current = current.c0
                                else:
                                    current = current.c1
                                self.path.append(key[len(self.branch_bits) + j])
                                self.branch_bits += key[len(self.branch_bits) + j]
                                self.parents.append(current)
                                j = j + 1
                            # Now insert

                            # leaf node reached
                            i = Inner()  # create new inner node
                            n = Node(key, datastr)  # create new leaf node
                            current2 = self.parents[-1]
                            if (current2.c1.bits[0] == '0'): #[0] vs [-1]
                                i.c0 = current2.c1
                                i.c0.bits = ''
                                i.c1 = n
                            else:
                                i.c1 = current2
                                i.c1.bits = ''
                                i.c0 = n

                            i.bits = ''  # double check
                            n.bits = n.bits[len(self.branch_bits):]  # traverse bits + branch bit

                            # update the parent of i
                            if len(self.parents) != 0:
                                self.parents.pop()  # discard the last value
                                parent = self.parents.pop()
                                path_prev_bit = self.path.pop()
                                if (path_prev_bit[-1] == '0'):
                                    parent.c0 = i
                                else:
                                    parent.c1 = i
                            else:
                                self.root = i

                    else:  # leaf node reached
                        i = Inner()  # create new inner node
                        n = Node(key, datastr)  # create new leaf node
                        current2 = self.parents[-1]
                        if (len(current2.c1.bits) != 0):
                            if(current2.c1.bits[0] == '0'):  #0 vs -1
                                i.c0 = current2.c1
                                i.c0.bits = i.c0.bits[1:]
                                if (len(i.c0.bits) != 0):
                                    i.bits = i.c0.bits[0]
                                    i.c0.bits = i.c0.bits[1:]
                                    self.branch_bits += i.bits
                            self.branch_bits += '1'
                            i.c1 = n
                        else:
                            i.c1 = current2.c0
                            i.c1.bits = i.c1.bits[1:]
                            if ( len(i.c1.bits) != 0):
                                i.bits = i.c1.bits[0]
                                i.c1.bits = i.c1.bits[1:]
                                self.branch_bits += i.bits
                            self.branch_bits += '0'
                            i.c0 = n

                        n.bits = key[len(self.branch_bits):]

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
        self.prev_bits = ''
        self.prev_root = None
        self.key_bits = ''


    def insert(self,key,datastr):
        if (self.root == None):
            n = Node(key,datastr)
            self.root = n
        else:
            #if self.has_Key(key) == '': #Key does not already exist
            self.insert_Item(key,datastr)
            #else:
            #    print "Key already present"

    def peek(self,stack):
        if len(stack) > 0:
            return stack[-1]
        return None

    def hash(self):
        # Create two stacks
        s1 = []
        s2 = []

        # Push root to first stack
        s1.append(self.root)

        # Run while first stack is not empty
        while (len(s1) > 0):

            # Pop an item from s1 and append it to s2
            node = s1.pop()
            s2.append(node)

            # Push left and right children of removed item to s1
            if node.c0 is not None:
                s1.append(node.c0)
            if node.c1 is not None:
                s1.append(node.c1)

                # Print all elements of second stack
        while (len(s2) > 0):
            node = s2.pop()
            print md5(node.bits + ':'+ node.data).hexdigest()



if __name__ == '__main__':
    t = Tree()
    t.insert('1111', 'A')
    t.insert('1110', 'B')
#    t.hash() #hashing is in progress

    # t.insert('0000','A')
    # t.insert('0001','B')
    # t.insert('0010','C')
    # t.insert('0011','D')
    # t.insert('0100','E')
    # t.insert('0101','F')
    # t.insert('0110','G')
    # t.insert('0111','H')
    # t.insert('1000','I')
    # t.insert('1001','J')
    # t.insert('1010','K')
    # t.insert('1011','L')
    # t.insert('1100','M')
    # t.insert('1101','N')
    # t.insert('1110','O')
    # t.insert('1111','P')
    # t.has_Key('0110')

    # t.insert('0101','A')
    # t.insert('0110','B')
    # t.insert('1111','C')
    # t.has_Key('0110')

    # t.insert('1111', 'A')
    # t.insert('1110', 'B')
    # t.insert('0000', 'C')
    # t.insert('0001', 'D')
    # t.insert('1000', 'E')


    # t.insert('0000', 'A')
    # t.insert('1111', 'B')
    # t.insert('0001', 'C')
    # t.insert('0010', 'D')
    # t.insert('0011', 'E')
    # t.insert('0100', 'F')



    # t.insert('1101', 'C')
    # t.insert('1100', 'D')



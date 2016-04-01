from collections import deque
from hashlib import md5


branch_bits = ''
key_bits = ''
parents = deque([])
path = deque([])
prev_bits = ''
prev_root = None
cur_root = None
key_dup = ''
i=None
n=None
found =0

class Tree(object):
    def __init__(self,rootNode):
        self.tree_root = rootNode



    def insert(self, key, datastr):

        global cur_root
        global branch_bits
        global key_bits
        global parents
        global path
        global prev_bits
        global prev_root
        global key_dup
        global found

        if type(key) == str and type(datastr) == str and len(key) == 4 and len(datastr) == 1:
            if (self.tree_root == None):
                n = Node()
                n.bits = key
                n.data = datastr
                self.tree_root = n
            else:
                key_dup = key
                self.tree_root.insert_Item(key, datastr)
                self.tree_root= cur_root
                # cleanup
                branch_bits = ''
                key_bits = ''
                parents = deque([])
                path = deque([])
                prev_bits = ''
                prev_root = None
                key_dup = ''
                found = 0
        else:
            print "Invalid Input"

class Node(object):
    def __init__(self):
        self.bits = ''
        self.data = ''
        self.c1=None
        self.c0=None
        self.root = None

    def longest_common_substring(self, s1, s2):
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
                    if (x == 1 and y == 1):
                        return ''
        return s1[x_longest - longest: x_longest]




    def insert_Item(self, key, datastr): #self points to root

        global cur_root
        global branch_bits
        global key_bits
        global parents
        global path
        global prev_bits
        global prev_root
        global i
        global n
        global key_dup

        # Single node case, where only one key has already been inserted,root points to leaf node
        if (len(self.bits) == 4):
            prev_root = self  # save prev root
            prev_bits = self.bits  # save prev node's bits or key
            i = Node()  # create new inner node
            common = self.longest_common_substring(prev_bits, key)  # function call to determine common bits
            i.bits = common
            self = i  # set new root as inner node
            cur_root = i
            n = Node()  # create new leaf node
            n.bits = key
            n.data  = datastr
            if (prev_bits[len(common)] == '0'):
                self.c0 = prev_root
                self.c1 = n
            else:
                self.c1 = prev_root
                self.c0 = n

            self.c0.bits = self.c0.bits[len(common) + 1:]  # remove common bits + branch bit from old or new node
            self.c1.bits = self.c1.bits[len(common) + 1:]  # remove common bits + branch bit from old or new node

        # inner node with empty bits
        elif (self.bits == '' and (self.c0 != None or self.c1 != None)):
            # First find the appropriate place to insert the new key
            msb = key[0]
            branch_bits += msb
            key_bits += msb
            parents.append(self)
            path.append(msb)
            if (msb == '1'):
                self.c1.insert_Item(key[1:], datastr)
            else:
                self.c0.insert_Item(key[1:], datastr)


        # inner node with non-empty bits
        elif self.bits != '' and (self.c0 != None or self.c1 != None):  # inner node with bits
            prev_bits = branch_bits + self.bits
            common = self.longest_common_substring(prev_bits[len(branch_bits):], key_dup[len(branch_bits):len(prev_bits)])
            msb = key[0]
            branch_bits += msb
            key_bits += msb
            parents.append(self)
            path.append(msb)
            if (common == '' or (len(common) < len(self.bits))):  # insert new inner node above this inner node
                i = Node()  # create new inner node
                n = Node()  # create new leaf node
                n.bits = key_dup
                n.data = datastr

                #for the case when the new inner node is going to become the root (i.e., there is no node above this node)
                current2 = parents[-1]
                if(current2 == parents[0]): #or parents[-1] == parents[0]
                    if self.bits[0] == '0':
                        i.c0 = self
                        i.c1 = n
                    else:
                        i.c1 = self
                        i.c0 = n

                    i.bits = common
                    self.bits = self.bits[len(common) + 1:]
                    n.bits = key[len(common) + 1:]  # remove common bits + branch bit from new node
                    #set new root
                    self = i
                    cur_root = self
                else:
                    if (current2.bits[0] == '0'):
                        i.c0 = current2
                        i.c0.bits = i.c0.bits[1:]
                        if (len(i.c0.bits) != 0):
                            i.bits = self.longest_common_substring(i.c0.bits, key_dup[len(key_bits) -1]) #:len(key_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                            i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                            key_bits += i.bits
                        else:
                            #key_bits += '0'
                            pass
                        i.c1 = n
                    else:
                        i.c1 = current2
                        i.c1.bits = i.c1.bits[1:]
                        if (len(i.c1.bits) != 0):
                            i.bits = self.longest_common_substring(i.c1.bits, key_dup[len(key_bits)-1]) #:len(key_bits) + len(i.c1.bits)])  # i.c1.bits
                            i.c1.bits = i.c1.bits[len(branch_bits) + len(i.bits):]
                            key_bits += i.bits
                        else:
                            #key_bits += '1'
                            pass

                        i.c0 = n

                    n.bits = n.bits[len(key_bits):]  # traverse bits + branch bit

                    #update the parent of i
                    if len(parents) != 0:
                        cur_root = parents[0]
                        parent = parents.pop()
                        path_prev_bit = path.pop()
                        if parent == current2:
                            parent = parents.pop()
                            path_prev_bit= path.pop()

                        if (path_prev_bit[-1] == '0'):
                            parent.c0 = i
                        else:
                            parent.c1 = i
                    else:
                        self = i
                        cur_root = self

            elif (len(common) == len(self.bits)):
                msb = key[len(common)]
                branch_bits = prev_bits + msb
                key_bits += msb
                parents.append(self)
                path.append(branch_bits)
                if(msb == '1'):
                    self.c1.insert_Item(key[len(branch_bits):],datastr)
                else:
                    self.c0.insert_Item(key[len(branch_bits):],datastr)


        else: #leaf node reached
            i = Node()  # create new inner node
            n = Node()
            n.bits = key_dup
            n.data = datastr  # create new leaf node
            self.arrange()
            # update the parent of i
            if len(parents) != 0:
                cur_root = parents[0]
                parent = parents.pop()
                path_prev_bit = path.pop()
                if (path_prev_bit[-1] == '0'):
                    parent.c0 = i
                else:
                    parent.c1 = i

            else:
                self = i
                cur_root = self




    def arrange(self):
        global cur_root
        global branch_bits
        global key_bits
        global parents
        global path
        global prev_bits
        global prev_root
        global i
        global n
        global key_dup

        #print "in arrange"
        current2 = parents[-1]
        last_bit = branch_bits[-1]

        if (last_bit == '1'):
            if len(current2.c1.bits) != 0:
                if (current2.c1.bits[0] == '0'):
                    i.c0 = current2.c1
                    i.c0.bits = i.c0.bits[1:]
                    if (len(i.c0.bits) != 0):
                        i.bits = self.longest_common_substring(i.c0.bits, key_dup[len(branch_bits):len(branch_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                        i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                        branch_bits += i.bits

                    branch_bits += '1'
                    i.c1 = n
                else:
                    i.c1 = current2.c1
                    i.c1.bits = i.c1.bits[1:]
                    if (len(i.c1.bits) != 0):
                        i.bits = self.longest_common_substring(i.c1.bits, key_dup[len(branch_bits):len(branch_bits) + len(i.c1.bits)])  # i.c0.bits[0]
                        i.c1.bits = i.c1.bits[len(branch_bits) + len(i.bits):]
                        branch_bits += i.bits

                    branch_bits += '0'
                    i.c0 = n
            elif len(current2.bits) != 0:
                if current2.bits[0] == '0':
                    i.c0 = current2
                    i.c0.bits = i.c0.bits[1:]
                    if (len(i.c0.bits) != 0):
                        i.bits = self.longest_common_substring(i.c0.bits, key_dup[len(branch_bits):len(branch_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                        i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                        branch_bits += i.bits

                    branch_bits += '1'
                    i.c1 = n

                else:
                    i.c1 = current2
                    i.c1.bits = i.c1.bits[1:]
                    if (len(i.c1.bits) != 0):
                        i.bits = self.longest_common_substring(i.c1.bits, key_dup[len(branch_bits):len(branch_bits) + len(i.c1.bits)])  # i.c0.bits[0]
                        i.c1.bits = i.c1.bits[len(branch_bits) + len(i.bits):]
                        branch_bits += i.bits

                    branch_bits += '1'
                    i.c0 = n

        else:
            if len(current2.c0.bits) != 0:
                if (current2.c0.bits[0] == '0'):
                    i.c0 = current2.c0
                    i.c0.bits = i.c0.bits[1:]
                    if (len(i.c0.bits) != 0):
                        i.bits = self.longest_common_substring(i.c0.bits, key_dup[len(branch_bits):len(branch_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                        i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                        branch_bits += i.bits

                    branch_bits += '1'
                    i.c1 = n
                else:
                    i.c1 = current2.c0
                    i.c1.bits = i.c1.bits[1:]
                    if (len(i.c1.bits) != 0):
                        i.bits = self.longest_common_substring(i.c1.bits, key_dup[len(branch_bits):len(branch_bits) + len(i.c1.bits)])  # i.c0.bits[0]
                        i.c1.bits = i.c1.bits[len(branch_bits) + len(i.bits):]
                        branch_bits += i.bits

                    branch_bits += '0'
                    i.c0 = n

            elif len(current2.bits) != 0:
                if current2.bits[0] == '0':
                    i.c0 = current2
                    i.c0.bits = i.c0.bits[1:]
                    if (len(i.c0.bits) != 0):
                        i.bits = self.longest_common_substring(i.c0.bits, key_dup[len(branch_bits):len(branch_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                        i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                        branch_bits += i.bits

                    branch_bits += '1'
                    i.c1 = n

                else:
                    i.c1 = current2
                    i.c1.bits = i.c1.bits[1:]
                    if (len(i.c1.bits) != 0):
                        i.bits = self.longest_common_substring(i.c1.bits, key_dup[len(branch_bits):len(branch_bits) + len(i.c1.bits)])  # i.c0.bits[0]
                        i.c1.bits = i.c1.bits[len(branch_bits) + len(i.bits):]
                        branch_bits += i.bits

                    branch_bits += '1'
                    i.c0 = n

        n.bits = key_dup[len(branch_bits):]

    def find(self, key):
        global found

        if self.c0 == None and self.c1 == None:
            if self.bits == key:
                print "->" + self.data
                found = 1
                return self.data

        else:
            if key[0] == '0':
                self.c0.find(key[len(self.bits)+1:])
            else:
                self.c1.find(key[len(self.bits)+1:])

        if found == 0:
            #print "Not found"
            return ''

    def hash(self):
        if self.c0 == None and self.c1 == None:
            return md5(self.bits+':'+self.data).hexdigest()
        else:
            c0_hash = self.c0.hash()
            c1_hash = self.c1.hash()
            return md5(self.bits + ':'+ c0_hash + ':'  + c1_hash).hexdigest()







if __name__ == '__main__':
    n = Node()
    n.bits = ''
    n.data = ''
    t = Tree(n.root)


    #case 1
    t.insert('0101', 'A')
    x = t.tree_root.hash()
    print x
    t.insert('0110', 'B')
    x = t.tree_root.hash()
    print x
    t.insert('1111','C')
    x = t.tree_root.hash()
    print x
    t.tree_root.find('0110')
    t.insert('1111','D')

    #case2
    t.insert('0000','A')
    t.insert('0001','B')
    t.insert('0010','C')
    t.insert('0011','D')
    t.insert('0100','E')
    t.insert('0101','F')
    t.insert('0110','G')
    t.insert('0111','H')
    t.insert('1000','I')
    t.insert('1001','J')
    t.insert('1010','K')
    t.insert('1011','L')
    t.insert('1100','M')
    t.insert('1101','N')
    t.insert('1110','O')
    t.insert('1111','P')
    t.tree_root.find('0110')
    x = t.tree_root.hash()
    print x
    t.tree_root.find('0000')
    t.tree_root.find('0001')
    t.tree_root.find('0010')
    t.tree_root.find('0011')
    t.tree_root.find('0100')
    t.tree_root.find('0111')
    t.tree_root.find('1000')
    t.tree_root.find('1001')
    t.tree_root.find('1010')
    t.tree_root.find('1010')


    #case 3
    # t.insert('1111', 'P')
    # t.insert('1110', 'O')
    # t.insert('1101', 'N')
    # t.insert('1100', 'M')
    # t.insert('1011', 'L')
    # t.insert('1010', 'K')
    # t.insert('1001', 'J')
    # t.insert('1000', 'I')
    # t.insert('0111', 'H')
    # t.insert('0110', 'G')
    # t.insert('0101', 'F')
    # t.insert('0100', 'E')
    # t.insert('0011', 'D')
    # t.insert('0010', 'C')
    # t.insert('0001', 'B')
    # t.insert('0000', 'A')
    # t.tree_root.find('0110')
    # x = t.tree_root.hash()
    # print x



    # t.insert('0101','A')
    # t.insert('0110','B')
    # t.insert('1111','C')
    # t.tree_root.find('0110')

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



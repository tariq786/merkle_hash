from collections import deque

branch_bits = ''
parents = deque([])
path  = deque([])
val = ''

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

    def insert_Item(self,root,key,datastr):
        # Single node case, where only one key has already been inserted,root points to leaf node
        if (root.data != '' and len(root.bits) == 4):
            prev_root = root      #save prev root
            prev_bits = root.bits #save prev node's bits or key
            i = Inner()           # create new inner node
            common = self.longest_common_substring(prev_bits,key) #function call to determine common bits
            i.bits = common
            root = i                                  # set new root as inner node
            n = Node(key,datastr)                     # create new leaf node
            if(prev_bits[len(common)] == '0'):
                root.c0 = prev_root
                root.c1 = n
            else:
                root.c1 = prev_root
                root.c0 = n
            prev_bits = prev_bits[len(common)+1:]  # remove common bits + branch bit from old node
            n.key = key[len(common)+1:]            # remove common bits + branch bit from new node
        # inner node with empty bits
        elif(root.bits == '' and (root.c0 != None or root.c1 != None) ):
            #First find the appropriate place to insert the new key
            msb = key[0]
            branch_bits += msb
            parents.append(root)
            path.append(msb)
            if (msb):
                self.insert_Item(root.c1, key[1:], datastr) #eventually takes you to leaf
            else:
                self.insert_Item(root.c0, key[1:], datastr) #eventually takes you to leaf

        # inner node with non-empty bits
        elif (root.bits != '' and (root.c0 != None or root.c1 != None)):  # inner node with bits
            prev_bits = branch_bits + root.bits
            common = self.longest_common_substring(prev_bits, key[0:len(prev_bits)])
            if common == '': #inser new inner node above this inner node (Github C=1111 insertion)
                i = Inner()  # create new inner node
                n = Node(key, datastr)  # create new leaf node
                path_prev_bit = path.pop()
                if path_prev_bit == '0':
                    i.c0 = root
                    i.c1 = n
                else:
                    i.c1 = root
                    i.c0 = n
                #prev_bits = prev_bits[len(common) + 1:]  # remove common bits + branch bit from old node
                root.bits = root.bit[1:] #decrease bit due to branching
                n.key = key[len(common) + 1:]  # remove common bits + branch bit from new node
                # update the parent of i
                if len(parents) != 0:
                    parent = parents.pop()
                    if(path_prev_bit == 0):
                        parent.c0 = i  # check whether c0 or c1
                    else:
                        parent.c1 = i  # check whether c0 or c1
                else:
                    root = i
                i.bits = ''  # common[1:]  # remove MSB bits from the inner node as it got moved to the branch
                branch_bits = ''

        elif (root.data != '' and len(root.bits) < 4):  # leaf node reached
            # create inner node in place of leaf node
            prev_bits = branch_bits + root.bits  # this retrieves leaf node's key
            i = Inner()  # create new inner node
            common = self.longest_common_substring(prev_bits, key)
            #i.bits = common
            n = Node(key, datastr)  # create new leaf node
            if (prev_bits[len(common) + 1] == '0'):
                i.c0 = root
                i.c1 = n
            else:
                i.c1 = root
                i.c0 = n
            prev_bits = prev_bits[len(common) + 1:]  # remove common bits + branch bit from old node
            n.key = key[len(common) + 1:]  # remove common bits + branch bit from new node
            # update the parent of i
            parent = parents.pop()
            parent.c0 = i  # check whether c0 or c1
            i.bits = common[1:]  # remove MSB bits from the inner node as it got moved to the branch
            # check if you need to borrow bit
            parent.bits = i.bits[0]
            i.bits = i.bits[1:]  # check if an expression is needed instead of ''
            branch_bits = ''



    ############################
    def insert(self,key,datastr):
        if (self.root == None):
            n = Node(key,datastr)
            self.root = n
        else:
            #if self.has_Key(key) == '': #Key does not already exist
            self.insert_Item(self.root,key,datastr)
            #else:
            #    print "Key already present"




if __name__ == '__main__':
    t = Tree()
    t.insert('0000','A')
    t.insert('0001','B')



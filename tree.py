from collections import deque
from hashlib import md5


ans =[] #for hashing

branch_bits = ''
key_bits = ''
parents = deque([])
path = deque([])
prev_bits = ''
prev_root = None
cur_root = None

class Tree(object):
    def __init__(self,rootNode):
        self.tree_root = rootNode



    def insert(self, key, datastr):
        if (self.tree_root == None):
            n = Node()
            n.bits = key
            n.data = datastr
            self.tree_root = n
        else:
            # if self.has_Key(key) == '': #Key does not already exist
            self.tree_root.insert_Item(key, datastr)
            self.tree_root= cur_root

            # else:
            #     print "Key already present"

class Node(object):
    def __init__(self):
        self.bits = ''
        self.data = ''
        self.c1=None
        self.c0=None
        self.root = None


    def insert_Item(self, key, datastr):
        # Single node case, where only one key has already been inserted,root points to leaf node
        global cur_root
        global branch_bits
        global key_bits
        global parents
        global path
        global prev_bits
        global prev_root

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
                if self.c1.data == '':
                    current = self.c1
                    # parents.append(current)
                    j = 0
                    if (current.bits != '' and current.bits != key[len(branch_bits):len(current.bits) + 1]):
                        # insert before current
                        i = Node()  # create new inner node
                        n = Node()
                        n.bits = key
                        n.data = datastr  # create new leaf node
                        current2 = parents[-1]
                        if (current2.c1.bits[0] == '0'):
                            i.c0 = current2.c1
                            i.c0.bits = i.c0.bits[1:]  # decrease inner node bits by 1 for branching
                            if (len(i.c0.bits) == 1 and i.c0.bits != '1'):
                                i.bits = i.c0.bits[0]
                                i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                                branch_bits += i.bits
                            i.c1 = n
                            branch_bits += '1'
                        else:
                            i.c1 = current2.c1
                            i.c1.bits = i.c1.bits[1:]  # decrease inner node bits by 1
                            if (len(i.c1.bits) == 1 and i.c1.bits != '1'):
                                i.bits = i.c1.bits[0]
                                i.c1.bits = i.c1.bits[len(branch_bits) + len(i.bits):]
                                branch_bits += i.bits
                            branch_bits += '0'
                            i.c0 = n

                        n.bits = n.bits[len(branch_bits):]  # traverse bits + branch bit

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
                    else:
                        parents.append(current)
                        branch_bits += current.bits
                        key_bits += current.bits
                        while ( current.data == '' and branch_bits[-1] == key[len(branch_bits) - 1]):
                            if key[len(branch_bits) + j] == '0':
                                current = current.c0
                                branch_bits += '0'
                            else:
                                current = current.c1
                                branch_bits += '1'
                            path.append(key[len(key_bits) + j])
                            key_bits += key[len(key_bits) + j]
                            branch_bits += current.bits
                            parents.append(current)
                            j = j + 1

                        # leaf node reached
                        i = Node()  # create new inner node
                        n = Node()
                        n.bits = key
                        n.data = datastr  # create new leaf node
                        current2 = parents[-1]
                        if (current2.bits[0] == '0'):
                            i.c0 = current2
                            i.c0.bits = i.c0.bits[1:]  # for branching
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(key_bits):len(key_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                                i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                                key_bits += i.bits
                            key_bits += '1'
                            i.c1 = n
                        else:
                            i.c0 = current2
                            i.c0.bits = i.c0.bits[1:]  # for branching
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(key_bits):len(key_bits) + len(i.c0.bits)])  # i.c1.bits
                                i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                                key_bits += i.bits
                            key_bits += '0'
                            i.c1 = n

                        n.bits = n.bits[len(key_bits):]  # traverse bits + branch bit

                        # update the parent of i
                        if len(parents) != 0:
                            cur_root = parents[0]
                            parents.pop()  # discard the last value
                            parent = parents.pop()
                            path_prev_bit = path.pop()
                            if (path_prev_bit[-1] == '0'):
                                parent.c0 = i  # check whether c0 or c1
                            else:
                                parent.c1 = i  # check whether c0 or c1


                        else:
                            self = i
                            cur_root = self

                else:  # leaf node reached
                    i = Node()  # create new inner node
                    n = Node()
                    n.bits = key
                    n.data = datastr  # create new leaf node
                    current2 = parents[-1]
                    if (current2.c1.bits[0] == '0'):
                        i.c0 = current2.c1
                        i.c1 = n
                        i.c0.bits = i.c0.bits[1:]  # remove for branching
                        if (len(i.c0.bits) != 0):
                            i.bits = self.longest_common_substring(i.c0.bits, key[len(branch_bits):len(branch_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                            i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                            branch_bits += i.bits
                        branch_bits += '1'
                    else:
                        i.c0 = current2.c0
                        i.c0.bits = i.c0.bits[1:]
                        if (len(i.c0.bits) != 0):
                            i.bits = self.longest_common_substring(i.c0.bits, key[len(branch_bits):len(branch_bits) + len(i.c0.bits)])  # i.c1.bits
                            i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                            branch_bits += i.bits
                        branch_bits += '0'
                        i.c1 = n

                    n.bits = key[len(branch_bits):]

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

            elif (msb == '0'):
                if self.c0.data == '':
                    current = self.c0
                    j = 0
                    if (current.bits != '' and current.bits != key[len(branch_bits):len(current.bits) + 1]):
                        # insert before current
                        i = Node()  # create new inner node
                        n = Node()
                        n.bits = key
                        n.data = datastr  # create new leaf node
                        current2 = parents[-1]

                        if (current2.c1.bits[0] == '0'):
                            i.c0 = current2.c1
                            i.c0.bits = i.c0.bits[1:]
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(key_bits):len(key_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                                i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                                branch_bits += i.bits
                            branch_bits += '1'
                            i.c1 = n
                        else:
                            # i.c1 = current2.c0  # self.c0  # decrease inner node bits by 1
                            # i.c1.bits = ''
                            # i.c0 = n
                            i.c0 = current2.c0
                            i.c0.bits = i.c0.bits[1:]
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(key_bits):len(key_bits) + len(i.c0.bits)])  # i.c1.bits
                                i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                                branch_bits += i.bits
                            branch_bits += '0'
                            i.c1 = n

                        n.bits = n.bits[len(branch_bits):]  # traverse bits + branch bit

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
                    else:
                        parents.append(current)
                        branch_bits += current.bits  # if any
                        key_bits += current.bits
                        while (current.data == '' and branch_bits[-1] == key[len(branch_bits) - 1]):
                            if key[len(branch_bits) + j] == '0':
                                current = current.c0
                                branch_bits += '0'
                            else:
                                current = current.c1
                                branch_bits += '1'
                            path.append(key[len(key_bits) + j])
                            branch_bits += current.bits
                            key_bits += key[len(key_bits) + j]
                            parents.append(current)
                            j = j + 1

                            # leaf node reached
                        i = Node()  # create new inner node
                        n = Node()
                        n.bits = key
                        n.data = datastr  # create new leaf node
                        current2 = parents[-1]
                        if (current2.bits[0] == '0'):
                            i.c0 = current2
                            i.c0.bits = i.c0.bits[1:]
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(key_bits):len(key_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                                i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                                key_bits += i.bits
                            key_bits += '1'
                            i.c1 = n
                        else:
                            i.c0 = current2
                            i.c0.bits = i.c0.bits[1:]
                            if (len(i.c0.bits) != 0):
                                i.bits = self.longest_common_substring(i.c0.bits, key[len(key_bits):len(key_bits) + len(i.c0.bits)])  # i.c1.bits
                                i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                                key_bits += i.bits
                            key_bits += '0'
                            i.c1 = n

                        n.bits = n.bits[len(key_bits):]  # traverse bits + branch bit

                        # update the parent of i
                        if len(parents) != 0:
                            cur_root = parents[0]
                            parents.pop()  # discard the last value
                            parent = parents.pop()
                            path_prev_bit = path.pop()
                            if (path_prev_bit[-1] == '0'):
                                parent.c0 = i
                            else:
                                parent.c1 = i

                        else:
                            self = i
                            cur_root = self

                else:  # leaf node reached
                    i = Node()  # create new inner node
                    n = Node()
                    n.bits = key
                    n.data = datastr  # create new leaf node
                    current2 = parents[-1]
                    if (current2.c1.bits[0] == '0'):  # 0 vs -1
                        i.c0 = current2.c1
                        i.c0.bits = i.c0.bits[1:]
                        if (len(i.c0.bits) != 0):
                            i.bits = self.longest_common_substring(i.c0.bits, key[len(branch_bits):len(
                                branch_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                            i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                            branch_bits += i.bits
                        branch_bits += '1'
                        i.c1 = n
                    else:
                        i.c0 = current2.c0
                        i.c0.bits = i.c0.bits[1:]
                        if (len(i.c0.bits) != 0):
                            i.bits = self.longest_common_substring(i.c0.bits, key[len(branch_bits):len(
                                branch_bits) + len(i.c0.bits)])  # i.c1.bits
                            i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                            branch_bits += i.bits
                        branch_bits += '0'
                        i.c1 = n

                    n.bits = key[len(branch_bits):]

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

        # inner node with non-empty bits
        elif (self.bits != '' and (self.c0 != None or self.c1 != None)):  # inner node with bits
            prev_bits = branch_bits + self.bits
            common = self.longest_common_substring(prev_bits, key[0:len(prev_bits)])

            if (common == '' or (len(common) < len(self.bits))):  # insert new inner node above this inner node
                i = Node()  # create new inner node
                n = Node()
                n.bits = key
                n.data = datastr  # create new leaf node

                if len(path) != 0:
                    path_prev_bit = path.pop()
                    if path_prev_bit[-1] == '0':
                        i.c0 = self
                        i.c1 = n
                    else:
                        i.c1 = self
                        i.c0 = n

                if self.bits[0] == '0':
                    i.c0 = self
                    i.c1 = n
                else:
                    i.c1 = self
                    i.c0 = n

                i.bits = common
                self.bits = self.bits[len(common) + 1:]
                n.bits = key[len(common) + 1:]  # remove common bits + branch bit from new node

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

            # !if (common == '' or  ( len(common) < len(self.bits) ) )
            elif (len(common) == len(self.bits)):  # traverse to find the insert spot
                msb = key[len(common)]
                branch_bits = prev_bits + msb
                parents.append(self)
                path.append(branch_bits)
                if (msb == '1'):
                    if self.c1.data == '':
                        current = self.c1
                        j = 0
                        if (current.bits != '' and current.bits != key[len(common) + 1]):
                            # insert before current
                            i = Node()  # create new inner node
                            n = Node()
                            n.bits = key
                            n.data = datastr  # create new leaf node
                            current2 = parents[-1]
                            if (current2.c1.bits[0] == '0'):  # [0] vs [-1]
                                i.c0 = current2.c1  # self.c1
                                i.c0.bits = i.c0.bits[1:]  # decrease inner node bits by 1
                                i.c1 = n
                                branch_bits += '1'
                            else:
                                i.c1 = current2.c1  # self.c0 #decrease inner node bits by 1
                                i.c1.bits = i.c1.bits[1:]
                                branch_bits += '0'
                                i.c0 = n

                            i.bits = ''
                            n.bits = n.bits[len(branch_bits):]  # traverse bits + branch bit

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
                        else:
                            parents.append(current)
                            while current.data == '':
                                if key[len(branch_bits) + j] == '0':
                                    current = current.c0
                                else:
                                    current = current.c1
                                path.append(key[len(branch_bits) + j])
                                branch_bits += key[len(branch_bits) + j]
                                parents.append(current)
                                j = j + 1
                            # Now insert

                            # leaf node reached
                            i = Node()  # create new inner node
                            n = Node()
                            n.bits = key
                            n.data = datastr  # create new leaf node
                            current2 = parents[-1]
                            # if (current2.bits[0] == '0'):  # [-1] vs [0]
                            #     i.c0 = current2
                            #     i.c0.bits = i.c0.bits[1:]
                            #     branch_bits += '1'
                            #     i.c1 = n
                            # else:
                            #     i.c1 = current2
                            #     i.c1.bits = i.c1.bits[1:]
                            #     branch_bits += '0'
                            #     i.c0 = n
                            #
                            # i.bits = common #  double check if ''

                            if (current2.bits[0] == '0'):
                                i.c0 = current2
                                i.c0.bits = i.c0.bits[1:]  # for branching
                                if (len(i.c0.bits) != 0):
                                    i.bits = self.longest_common_substring(i.c0.bits, key[len(key_bits):len(key_bits) + len(i.c0.bits)])  # i.c0.bits[0]
                                    i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                                    key_bits += i.bits
                                key_bits += '1'
                                i.c1 = n
                            else:
                                i.c0 = current2
                                i.c0.bits = i.c0.bits[1:]  # for branching
                                if (len(i.c0.bits) != 0):
                                    i.bits = self.longest_common_substring(i.c0.bits, key[len(key_bits):len(key_bits) + len(i.c0.bits)])  # i.c1.bits
                                    i.c0.bits = i.c0.bits[len(branch_bits) + len(i.bits):]
                                    key_bits += i.bits
                                key_bits += '0'
                                i.c1 = n

                            n.bits = n.bits[len(branch_bits):]  # traverse bits + branch bit

                            # update the parent of i
                            if len(parents) != 0:
                                cur_root = parents[0]
                                parents.pop()  # discard the last value
                                parent = parents.pop()
                                path_prev_bit = path.pop()
                                if (path_prev_bit[-1] == '0'):
                                    parent.c0 = i
                                else:
                                    parent.c1 = i

                            else:
                                self = i
                                cur_root = self

                    else:  # leaf node reached
                        i = Node()  # create new inner node
                        n = Node()
                        n.bits = key
                        n.data = datastr  # create new leaf node
                        current2 = parents[-1]
                        if (len(current2.c1.bits) != 0):  # [0]  vs [-1] if (len(current2.c1.bits) != 0):
                            if (current2.c1.bits[0] == '0'):
                                i.c0 = current2.c1
                                i.c0.bits = i.c0.bits[1:]
                                if (len(i.c0.bits) != 0):
                                    i.bits = i.c0.bits[0]
                                    i.c0.bits = i.c0.bits[1:]
                                    branch_bits += i.bits
                            branch_bits += '1'
                            i.c1 = n
                        else:
                            i.c1 = current2.c0
                            i.c1.bits = i.c1.bits[1:]
                            if (len(i.c1.bits) != 0):
                                i.bits = i.c1.bits
                                i.c1.bits = i.c1.bits[1:]
                                branch_bits += i.bits
                            branch_bits += '0'
                            i.c0 = n

                        n.bits = key[len(branch_bits):]

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


                elif (msb == '0'):
                    if self.c0.data == '':
                        current = self.c0
                        j = 0
                        if (current.bits != '' and current.bits != key[len(common) + 1]):
                            # insert before current
                            i = Node()  # create new inner node
                            n = Node()
                            n.bits = key
                            n.data = datastr  # create new leaf node
                            current2 = parents[-1]
                            if (current2.c0.bits[-1] == '0'):
                                i.c0 = current2.c0  # self.c0
                                i.c0.bits = ''  # decrease inner node bits by 1
                                i.c1 = n
                            else:
                                i.c1 = current2.c0  # decrease inner node bits by 1
                                i.c1.bits = ''
                                i.c0 = n
                            i.bits = ''  # double check
                            n.bits = n.bits[len(branch_bits):]  # traverse bits + branch bit

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
                        else:
                            parents.append(current)
                            while current.data == '':
                                if key[len(branch_bits) + j] == '0':
                                    current = current.c0
                                else:
                                    current = current.c1
                                path.append(key[len(branch_bits) + j])
                                branch_bits += key[len(branch_bits) + j]
                                parents.append(current)
                                j = j + 1
                            # Now insert

                            # leaf node reached
                            i = Node()  # create new inner node
                            n = Node()
                            n.bits = key
                            n.data = datastr  # create new leaf node
                            current2 = parents[-1]
                            if (current2.c1.bits[0] == '0'):  # [0] vs [-1]
                                i.c0 = current2.c1
                                i.c0.bits = ''
                                i.c1 = n
                            else:
                                i.c1 = current2
                                i.c1.bits = ''
                                i.c0 = n

                            i.bits = ''  # double check
                            n.bits = n.bits[len(branch_bits):]  # traverse bits + branch bit

                            # update the parent of i
                            if len(parents) != 0:
                                cur_root = parents[0]
                                parents.pop()  # discard the last value
                                parent = parents.pop()
                                path_prev_bit = path.pop()
                                if (path_prev_bit[-1] == '0'):
                                    parent.c0 = i
                                else:
                                    parent.c1 = i

                            else:
                                self = i
                                cur_root = self

                    else:  # leaf node reached
                        i = Node()  # create new inner node
                        n = Node()
                        n.bits = key
                        n.data = datastr  # create new leaf node
                        current2 = parents[-1]
                        if (len(current2.c1.bits) != 0):
                            if (current2.c1.bits[0] == '0'):  # 0 vs -1
                                i.c0 = current2.c1
                                i.c0.bits = i.c0.bits[1:]
                                if (len(i.c0.bits) != 0):
                                    i.bits = i.c0.bits[0]
                                    i.c0.bits = i.c0.bits[1:]
                                    branch_bits += i.bits
                            branch_bits += '1'
                            i.c1 = n
                        else:
                            i.c1 = current2.c0
                            i.c1.bits = i.c1.bits[1:]
                            if (len(i.c1.bits) != 0):
                                i.bits = i.c1.bits[0]
                                i.c1.bits = i.c1.bits[1:]
                                branch_bits += i.bits
                            branch_bits += '0'
                            i.c0 = n

                        n.bits = key[len(branch_bits):]

                        # update the parent of i
                        if len(parents) != 0:
                            cur_root = parents[0]
                            parent = parents.pop()
                            path_prev_bit = path.pop()
                            if (path_prev_bit[-1] == '0'):
                                parent.c0 = i  # check whether c0 or c1
                            else:
                                parent.c1 = i  # check whether c0 or c1

                        else:
                            self = i
                            cur_root = self



        branch_bits = ''
        key_bits = ''
        parents = deque([])
        path = deque([])
        prev_bits = ''
        prev_root = None

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

    def find(self,key):
        if(self.bits == key):
            print "->"+self.data
        else:
            while self.data == '':
                if self.bits == '':
                    if(key[0] == '0'):
                        self = self.c0
                    else:
                        self = self.c1
                    key=key[1:]
                else:
                    key=key[len(self.bits):]
                    if (key[0] == '0'):
                        self = self.c0
                    else:
                        self = self.c1
            if(self.data != ''):
                print"->"+self.data
            else:
                print "not found"



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


    ##case 1
    # t.insert('0101', 'A')
    # x = t.tree_root.hash()
    # print x
    # t.insert('0110', 'B')
    # x = t.tree_root.hash()
    # print x
    # t.insert('1111','C')
    # x = t.tree_root.hash()
    # print x

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



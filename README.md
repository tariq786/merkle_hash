# Description
Implement a binary Merkle-tree-like data structure, along with a brief write-up. This exercise requires absolutely no prior bitcoin-related knowledge or experience. Background information and more details about the task are below.

This exercise should take 2-3 hours to complete (really):

* 30 minutes to read this document and familiarize yourself with merkle-trees;
* 30-90 minutes to code up a working first cut of the result in the programming language of your choice; and
* 60 minutes to test, debug, and clean up your code, write down a few thoughts, and submit the final product.

If you find it going past three hours or so, please get in touch and let us know your progress. Also, please complete this on your own without direct help from others, but feel free to use Google, StackOverflow, and other references as needed. Use any reasonable third-party libraries you want, e.g. md5 libraries.

You may write in any language you consider appropriate, but please include clear instructions for us to run/test it locally, including setting up any dependencies on whatever platform you develop. Most of us run OS X with homebrew, nodejs/npm, and python/pip readily accessible, but are open to anything reasonable.

You should deliver your solution by committing it to the TradeBlock GitHub repository provided to you, along with the write-up. You can append your write-up to the bottom of this readme or create a separate file.

If anything in this document is unclear, feel free to make a reasonable assumption, state it in your write-up, and continue on. Also feel free to reach out at any time with questions and we will try to get them answered as soon as possible.

# Background
* Blockchain protocols such as Bitcoin and Ethereum make heavy use of Merkle-Trees, or Merkle-Patricia-Trees.
* Those trees are data structures that summarize any number of data objects (eg, transactions) by a single hash value, amongst other benefits, such as the ability to derive compact cryptographic proofs for data object inclusion (eg, transaction confirmation).
* In this exercise, the goal is to implement a similar (albeit significantly simplified) data structure, as defined below. Note that this data structure shares some concepts of traditional merkle trees but with a simplified hashing model and data structure.

# Specification
* The tree resembles a compact binary search tree that maps keys (numbers) to data items (arbitrary strings).
* A key is given as a string that represents a binary number and it has exactly 4 digits. Example: "0101" represents the key 5. Keys serve as the unique identifier for the data stored.
* There are two different types of tree nodes, inner nodes which are the branches of the tree, and leaf nodes which reference specific data objects:

        Inner Node: {
            bits: string
            c0: child node that follows with a "0"
            c1: child node that follows with a "1"
        }

        Leaf Node: {
            bits: string
            data: string
        }

    Where `bits` is a compacted segment of the node ID (see below), `c0` and `c1` are the children node of the inner node, and `data` is the string of data stored in the leaf node.

* A node's key is described by the edges on the path of the leaf node through the root node, and by all bits on that path.
* `bits` are used for tree compaction (mandatory), ie, instead of adding superfluous inner nodes, common bits are stored in `bits`. In the case of an inner node, `bits` stores the common bits of its two children. And for leaf nodes, `bits` stores the remaining bits for the key of the data item that node references. In case there are no shared bits, or no remaining bits for the key, `bits` is set to the empty string. The example below should help to understand how `bits` is used for tree compaction.
* A leaf node's hash is defined as `md5(bits + ':' + data)`.
* An inner node's hash is recursively defined as `md5(bits + ':' + c0.hash() + ':' + c1.hash())`.

# Functions to be implemented:
* `tree.insert('0101', 'dataA'); // inserts the given data string under key '0101'. Fails if key invalid or already present.`
* `tree.find('0101'); // returns the data string for key '0101', returns null if not found.`
* `tree.hash(); // computes and returns the root node's hash.`

# Example
    tree.insert('0101', 'A')
        Tree root: leaf(bits = '0101', data = 'A')

    tree.hash()
        -> b5ffc0ab4c199b1bd5de6be3c0a6f92c

    tree.insert('0110', 'B')
        Tree root: inner(bits = '01',
                         c0 = leaf(bits = '1', data = 'A'),
                         c1 = leaf(bits = '0', data = 'B'))

    tree.hash()
        -> 1118dd742ca668445754b6e8da1817ef

    tree.insert('1111', 'C')
        Tree root: inner(bits = '',
                         c0 = inner(bits = '1',
                                    c0 = leaf(bits = '1', data = 'A',
                                    c1 = leaf(bits = '0', data = 'B')),
                         c1 = leaf(bits = '111', 'C'))

    tree.find('0110')
        -> B

    tree.hash()
        -> c12b7c13dedeb057c37af6a4b183c242

 

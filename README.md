#generalized-suffix-tree

python implementation of generalized suffix tree

## compare
create generalized suffix tree for "aba" and "a"

### old way
append a unique ending character to each string(the character should not in all the strings), "aba#", "a$"
and then concatenate the strings into one string, "aba#a$"

the suffix tree is:

![aba_a](aba_a.png)

there are two data structure in the tree: Node and Edge

* Node: edge_dict(identify by the first char of the edge's lable)
* Edge: target node, label(the string it represents)

The problem of the suffix tree is that you have to find a unique character for each string,
when there are too many strings, it is impossible.

### change

so we change the suffix tree, add some information to the node, this change is inspired by https://github.com/abahgat/suffixtree

we assign a unique index to each string, and each leaf node has index_list, which contains
the indexes of the strings.

* Node: index_list, edge_dict, all_index_list(optional)
* Edge: target node, label

The new suffix tree we create

![aba_a_index](aba_a_index.png)

#### Process
Here we split the process of building suffix tree:

`append(text, index)` add text the the suffix tree.

after `append('aba', 0)`

![aba_index](aba_index.png)

after `append('a', 0)`

![aba_a_index](aba_a_index.png)

#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self, index=None):
        self.index_set = set()
        if not index is None:
            self.index_set.add(index)
        self.edge_dict = {}
        self.suffix_link = None

    def add_index(self, index):
        self.index_set.add(index)

    def get_indexs(self):
        return self.index_set

    def add_edge(self, edge):
        char = edge.get_char()
        self.edge_dict[char] = edge

    def remove_edge(self, char):
        self.edge_dict.pop(char)

    def get_edge(self, char):
        return self.edge_dict.get(char)

    def get_edges(self):
        return self.edge_dict.itervalues()

    def __str__(self):
        return "id: %d, edges: %s" % (id(self), self.edge_dict)


class Edge(object):

    def __init__(self, index, start, end, target_node):
        self.index = index
        self.start = start
        self.end = end
        self.target_node = target_node
        self.text_store = TextStore()

    @property
    def length(self):
        return self.end - self.start

    def get_char(self, i=0):
        return self.text_store.get_char(self.index, self.start + i)

    def split(self, i, new_target):
        new_edge = Edge(self.index, self.start, self.start + i, new_target)
        self.start += i
        return new_edge

    @property
    def label(self):
        return self.text_store.get_str(self.index, self.start, self.end)

    def __str__(self):
        return "-- %s --> %d, edge_id: %s" % (self.label, id(self.target_node),
                                              id(self))


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TextStore(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.text_list = []

    def append(self, text):
        self.text_list.append(text)

    def get_char(self, index, i):
        return self.text_list[index][i]

    def get_str(self, index, start, end):
        return self.text_list[index][start:end]

    def clear(self):
        self.text_list = []


class GST(object):

    def __init__(self):
        self.remainder = 0
        self.root = Node()
        self.active_node = self.root
        self.active_length = 0
        self.active_edge = None  # should be a char

        self.text_store = TextStore()
        self.text_store.clear()

    def reset_active(self):
        self.active_node = self.root
        self.active_length = 0
        self.active_edge = None
        self.remainder = 0

    def add_text(self, text, index):
        self.reset_active()
        self.text_store.append(text)
        self.text_len = len(text)
        for i in range(self.text_len):
            self.add_char(i, index)

    def add_char(self, start, index):
        ''' if start == text_len - 1 is "", we need some operation '''
        self.remainder += 1
        char = self.text_store.get_char(index, start)
        last_parent = None
        over = (start == self.text_len-1)

        while self.remainder:
            self.canonize()
            self.active_edge = self.text_store.get_char(index,
                                                        start-self.remainder+1)

            edge = self.active_node.get_edge(self.active_edge)
            if edge is None:
                # add a new edge here
                leaf_node = Node(index)
                new_edge = Edge(index, start, self.text_len, leaf_node)
                self.active_node.add_edge(new_edge)
                # add suffix link
                self.add_suffix_link(last_parent, self.active_node)
                last_parent = self.active_node
            else:
                # next char match
                if edge.get_char(self.active_length) == char:
                    # if over is True
                    self.active_length += 1
                    # add suffix link
                    self.add_suffix_link(last_parent, self.active_node)
                    last_parent = self.active_node
                    if not over:
                        break
                    else:
                        self.add_index(index)
                        break

                #split
                internal_node = self.split_edge(edge)

                # add suffix link
                self.add_suffix_link(last_parent, internal_node)
                last_parent = internal_node

                # add a new edge
                leaf_node = Node(index)
                new_edge = Edge(index, start, self.text_len, leaf_node)
                internal_node.add_edge(new_edge)

            self.remainder -= 1

            self.go_next()

    def split_edge(self, edge):
        self.active_node.remove_edge(self.active_edge)

        internal_node = Node()
        new_edge = edge.split(self.active_length, internal_node)
        internal_node.add_edge(edge)

        self.active_node.add_edge(new_edge)
        return internal_node

    def go_next(self):
        if self.active_node is self.root:
            if self.active_length:
                self.active_length -= 1
        else:
            self.active_node = self.active_node.suffix_link
            if self.active_node is None:
                self.active_node = self.root

    def add_index(self, index):
        last_parent = None
        while self.remainder:
            self.canonize()
            if self.active_length == 0:
                self.active_node.add_index(index)
            else:
                edge = self.active_node.get_edge(self.active_edge)
                assert not edge is None, "Edge should not be none"
                internal_node = self.split_edge(edge)
                internal_node.add_index(index)

                # add suffix link
                self.add_suffix_link(last_parent, internal_node)
                last_parent = internal_node

            self.remainder -= 1
            self.go_next()

    def search(self, pattern):
        cur_node = self.root
        while pattern != "":
            edge = cur_node.get_edge(pattern[0])
            if edge is None:
                return

            label = edge.label
            min_len = min(len(label), len(pattern))
            if label[:min_len] == pattern[:min_len]:
                cur_node = edge.target_node
                pattern = pattern[min_len:]
            else:
                return

        index_set = set()
        for index in self.dfs(cur_node):
            if index in index_set:
                continue
            index_set.add(index)
            yield index

    def dfs(self, node):
        if node is None:
            return
        for index in node.get_indexs():
            yield index

        for edge in node.get_edges():
            for index in self.dfs(edge.target_node):
                yield index

    def add_suffix_link(self, last_parent, current):
        if not last_parent is None:
            last_parent.suffix_link = current

    def canonize(self):
        if self.active_length <= 0:
            return
        edge = self.active_node.get_edge(self.active_edge)
        if edge.length <= self.active_length:
            self.active_length -= edge.length
            self.active_node = edge.target_node

    def print_active(self):
        print 'active: node: %d, edge: %s, len: %d' % (id(self.active_node),
                                                       self.active_edge, self.active_length)

    def traverse(self, output):
        self.dot_str = "digraph {\n label=\"%s\";\n" % output

        def dfs(node):
            self.dot_str += "%d [label=\"%s\"]" % (id(node), str(node.index_set))
            if not node.suffix_link is None:
                self.dot_str += "%d -> %d[style=dotted];\n" % (id(node), id(node.suffix_link))

            for edge in node.edge_dict.itervalues():
                self.dot_str += "%d -> %d[label=\"%s\"];\n" % (id(node),
                                                          id(edge.target_node),
                                                          edge.label)
                dfs(edge.target_node)

        #self.print_active()
        dfs(self.root)

        self.dot_str += "}"
        with open(output+".dot", 'w') as w_file:
            w_file.write(self.dot_str)

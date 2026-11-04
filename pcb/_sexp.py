"""Minimal s-expression reader/writer for KiCad files, with source spans.

parse(text) -> Node; Node has .head (str), .children (list[Node|str]), .start, .end
Strings are returned as ('q', value) tuples so that quotedness is preserved.
"""
import re


class Node:
    __slots__ = ("head", "children", "start", "end")

    def __init__(self, head, children, start, end):
        self.head = head
        self.children = children
        self.start = start
        self.end = end

    def __repr__(self):
        return "<Node %s @%d-%d n=%d>" % (self.head, self.start, self.end, len(self.children))

    def find_all(self, head):
        out = []
        for c in self.children:
            if isinstance(c, Node):
                if c.head == head:
                    out.append(c)
                out.extend(c.find_all(head))
        return out

    def find(self, head):
        for c in self.children:
            if isinstance(c, Node) and c.head == head:
                return c
        return None

    def atoms(self):
        return [c for c in self.children if not isinstance(c, Node)]

    def value(self, head, idx=0):
        n = self.find(head)
        if n is None:
            return None
        a = n.atoms()
        if idx < len(a):
            v = a[idx]
            return v[1] if isinstance(v, tuple) else v
        return None


def parse(text):
    """Return a list of top-level Nodes plus the root Node."""
    i = 0
    n = len(text)
    stack = []
    roots = []

    def read_atom(i):
        # returns (value, is_quoted, new_i)
        if text[i] == '"':
            j = i + 1
            buf = []
            while j < n:
                c = text[j]
                if c == "\\":
                    buf.append(text[j:j + 2])
                    j += 2
                    continue
                if c == '"':
                    return ('q', "".join(buf)), j + 1
                buf.append(c)
                j += 1
            raise ValueError("unterminated string at %d" % i)
        j = i
        while j < n and not text[j].isspace() and text[j] not in "()":
            j += 1
        return text[i:j], j

    while i < n:
        c = text[i]
        if c in " \t\r\n":
            i += 1
            continue
        if c == ";":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == "(":
            start = i
            i += 1
            # read head atom
            while i < n and text[i].isspace():
                i += 1
            if i < n and text[i] == ")":
                node = Node("", [], start, i + 1)
                i += 1
            else:
                head, i = read_atom(i)
                if isinstance(head, tuple):
                    head = head[1]
                node = Node(head, [], start, None)
                stack.append(node)
                continue
            if stack:
                stack[-1].children.append(node)
            else:
                roots.append(node)
            continue
        if c == ")":
            node = stack.pop()
            node.end = i + 1
            i += 1
            if stack:
                stack[-1].children.append(node)
            else:
                roots.append(node)
            continue
        atom, i = read_atom(i)
        if stack:
            stack[-1].children.append(atom)
        else:
            raise ValueError("top-level atom at %d: %r" % (i, atom))
    return roots


def walk(node, head=None):
    if isinstance(node, Node):
        if head is None or node.head == head:
            yield node
        for c in node.children:
            yield from walk(c, head)


def atom_str(a):
    return a[1] if isinstance(a, tuple) else a

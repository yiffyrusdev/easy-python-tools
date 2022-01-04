# Structures

## Quick start
Submodule structure:

**easy_pytools.structures**
- **trees**
  - BinaryTree (C++, Linux)
  - PyBinaryTree (Python)
  - PrefixTree (C++, Linux)
  - PyPrefixTree (Python)
- **primitives**
  - Queue (C++, Linux)
  - Stack (C++, Linux)
- **graphs**
  - PyGraph (Python) 
  - PyOrientedGraph (Python)

### BinaryTree
BinaryTree and PyBinaryTree are similar in behavour.
```python
from easy_pytools.structures.trees import BinaryTree

tree = BinaryTree()
```

#### Add value to tree
All values have to be comparable with each other with standad Python lt, gt, eq magic methods.
```python
tree.add(20)   # Now all added values have to be comparable with int
tree.add(15)   # Good
tree.add(7)    # Good
tree.add(17.5) # Good
tree.add("h")  # Exception
```

#### Using fulfilled tree
```python
# Useful properties with "talking" names:
tree.depth  # Depth of the tree. I try to keep it near to log2
tree.is_empty()

# Check containment
tree.contains(15)
15 in tree
```
Deletion is not currently supported

### Prefix Tree
Also known as "Bor".

PrefixTree and PyPrefixTree are similar in behavour.
```python
from easy_pytools.structures.trees import PrefixTree

tree = PrefixTree()
```

#### Enroll sequence into tree
Any iterable and ordered sequence can be enrolled into the tree:
```python
tree.add([10, 20, 30])
tree.add([10, 30, 40])
tree.add("Hello")
tree.add("Helluva")
tree.add("Hello")
```

#### Using fulfilled tree
```python
# Count how much times sequence was enrolled:
tree.count("Hello")      # Returns 2
tree.count("Helluva")    # Returns 1
tree.count([10, 20, 30]) # Returns 1
tree.count("Hell")       # Returns 0
tree.count([10])         # Returns 0

# Check if tree contains sequence:
tree.contains("Hello")   # True
tree.contains("Hell")    # False
```

Deletion and "in" operators are not supported.

### Stack, Queue
These are pseudo-structures as they do not affect the way data is organized in memory.

```python
from easy_pytools.structures.primitives import Stack, Queue

s = Stack()
q = Queue()

s.push(None)
s.push(20)
s.top         # 20, top element still remains in the stack
s.top         # 20
s.size        # 2
s.is_empty()  # Returns False
s.pop()       # Returns 20
s.pop()       # Returns None
s.pop()       # Stack is empty, returns None
s.is_empty()  # Returns True


q.add(None)
q.add(10)
q.add(20)
q.first       # None
q.last        # 20
q.size        # 3
q.is_epmty()  # Returns False
q.next()      # Returns None
q.next()      # Returns 10
q.next()      # Returns 20
q.is_empty()  # Returns True
q.size        # 0
q.next()      # Queue is empty, returns None
```

### Graph, OrientedGraph
The difference between them is that when adding an edge in a regular graph, the order of the vertices does not matter, but in an oriented graph it does. Accordingly, the check and search for the path is carried out on the basis of this.

```python
from easy_pytools.structures.graphs import PyGraph, PyOrientedGraph

g = PyGraph()
og = PyOrientedGraph()
```

Add vertex:
```python
g.add_vertex(0)
g.add_vertex(1)
og.add_vertex(0)
og.add_vertex(1)
```

Add Edge:
```python
# You can set edge between existing vertexes:
g.add_edge(0, 1)
og.add_edge(0, 1)

# Or vertexes can be added automatically:
g.add_edge(10, 20)
g.add_edge(10, 30)
g.add_edge(20, 30)
g.add_edge(30, 40)
og.add_edge(10, 20)
og.add_edge(10, 30)
og.add_edge(20, 30)
og.add_edge(30, 40)
```

Vertexes checks:
```python
1 in g       # True
1 in og      # True
30 in g      # False
30 in og     # False
```

Edges checks:
```python
# You can check if vertexes has edge:
g.are_adjacent(1, 0)    # True
g.are_adjacent(0, 1)    # True
og.are_adjecent(1, 0)   # True
og.are_adjecent(0, 1)   # False. Orientations is 1 -> 0, so they are not adjecent!

# You can see all vertexes that can be directly reached from some:
g.adjacents(10)         # {20,}
g.adjacents(20)         # {10,} 
og.adjecents(10)        # {20,}
og.adjecents(20)        # set() -- empty set

# You can travel through vertexes from start point:
list(g.travel(10))      # [10,20,30,30,40,40]
list(g.travel(30))      # [30,40,10,20,20]
list(og.travel(10))     # [10,20,30,30,40,40]
list(og.travel(30))     # [30,40]

# And you can travel through vertexes by levels:
list(g.travel_levels(20))
"""
[(20, {10, 30}),
 (10, {20, 30}),
 (30, {10, 20, 40}),
 (30, {10, 20, 40}),
 (40, {30}),
 (40, {30})]
"""
list(og.travel_levels(20))
"""
[(20, {30}),
 (30, {40}),
 (40, set())]
"""
```

Find minimal path from one to other:
```python
g.minimal_path_deikstra(10, 40)   # {'path': [10, 30, 40], 'weight': 2}
g.minimal_path_deikstra(40, 10)   # {'path': [40, 30, 10], 'weight': 2}

og.minimal_path_deikstra(10, 40)   # {'path': [10, 30, 40], 'weight': 2}
og.minimal_path_deikstra(40, 10)   # {'path': [], 'weight': inf}
```

Weights (Yep, edges can have weights)
```python
g.add_edge(10, 1, 40)  # weight of edge is 40
og.add_edge(10, 1, 40) # weight of edge is 40
```

And minimal path is calculated not by adges count, but by edges weight.
Default weight is 1. 'inf' means no edge, or infinite edge weight (similar).

```python
g.edge_weight(10, 30)   # 1
g.edge_weight(30, 10)   # 1
g.edge_weight(10, 40)   # inf

og.edge_weight(10, 30)  # 1
og.edge_weight(30, 10)  # inf
og.edge_weight(10, 40)  # inf
```
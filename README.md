# Python tools
Simple toolset with Python type hints made to deserve my needs on some Python projects.

Both Python anc C++ implementations are in plans:
- Any Python implementation is cross-platform but achieve less average performance goals
- C++ implementations are currently supported only for Linux and provided in this repository in two ways:
  - Prebuilt .so files, so in average case you can just "git clone" and use C++ classes in Python project
  - Source code

## Roadmap
- [x] Pseudo structures
  - [x] Stack **(C++)**
  - [x] Queue **(C++)**
- [ ] Basic data structures
  - [ ] Trees
    - [ ] Tree of arbitrary objects
    - [x] Binary tree with post-insertion balance **(Python, C++)**
    - [x] Prefix tree for sequential search **(Python, C++)**
    - [ ] Red-black tree
    - [ ] AVL tree
    - [ ] 1-2-3 tree
  - [ ] Graph-based
    - [x] Graph **(Python)**
    - [x] Oriented graph **(Python)**
    - [ ] Network with flows
- [x] Class and object enhancements
  - [x] DataTransferObject class decorator **(Python only)**

## Requirements
Python implementations require the following:
- Python >= 3.10 < 4.0

C++ implementations require the following to be built:
- Cmake >= 3.20
- PythonLibs >= 3.10
- Boost with Python package

## Have fun!
If you find this code useful, I will be glad if you use it in your GPL3-compatible licensed project.

**"Why GPL-3. Author, are you too proud?"**
> Nope. It's just that I'm fighting for free software, and any possibility that someone else is using my code on a project that people, myself included, will have to pay for is unacceptable. My code is neither perfect nor revolutionary.

Any help and criticism is greatly appreciated.
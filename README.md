# Python tools
Simple toolset with Python type hints made to deserve my needs on some Python projects.

Both Python anc C++ implementations are in plans:
- Any Python implementation is cross-platform but achieve less average performance goals
- C++ implementations are currently supported only for Linux and provided in this repository in two ways:
  - Prebuilt .so files, so in average case you can just "git clone" and use C++ classes in Python project
  - Source code _(try your luck and build it for Windows)_

## Roadmap
- **Pseudo structures**
  - [x] Stack _(C++)_
  - [x] Queue _(C++)_
  - [ ] Prioritized Queue
    - [ ] _Python_
    - [ ] _C++_
- **Basic data structures**
  - **Plain**
    - [ ] LinkedList
      - [ ] _Python_
      - [ ] _C++_
    - [ ] LinkedList with O(1) index access _(C++)_
  - **Trees**
    - [ ] Tree of arbitrary objects
      - [ ] _Python_
      - [ ] _C++_
    - [x] Binary tree with post-insertion balance
      - [x] _Python_
      - [x] _C++_
    - [x] Prefix tree for sequential search
      - [x] _Python_
      - [x] _C++_
    - [ ] Red-black tree
      - [ ] _Python_
      - [ ] _C++_
    - [ ] AVL tree
      - [ ] _Python_
      - [ ] _C++_
    - [ ] 1-2-3 tree
      - [ ] _Python_
      - [ ] _C++_
  - **Graphs**
    - [x] Graph _(Python)_
    - [x] Oriented graph _(Python)_
    - [ ] Network with flows _(Python)_
- **Class and object enhancements**
  - [x] DataTransferObject class decorator _(Python)_

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
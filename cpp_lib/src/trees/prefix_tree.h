//
// Created by psycho on 20.12.2021.
//

#ifndef CPP_LIB_PREFIX_TREE_H
#define CPP_LIB_PREFIX_TREE_H

#include <boost/python.hpp>
#include <unordered_map>

using namespace boost;

template<> struct std::hash<python::object>{
  size_t operator()(const python::object &obj) const noexcept;
};

struct prefix_tree_node{
  python::object value;
  uint terminations;
  std::unordered_map<python::object, prefix_tree_node*> *children;
  prefix_tree_node();
  explicit prefix_tree_node(python::object value);
};

class prefix_tree {
  prefix_tree_node *root;
public:
  prefix_tree();
  void add(python::object &sequence);
  prefix_tree_node *catch_node(python::object &sequence) const;
  [[nodiscard]] bool contains(python::object &sequence) const;
  [[nodiscard]] uint count(python::object &sequence) const;
};


#endif //CPP_LIB_PREFIX_TREE_H

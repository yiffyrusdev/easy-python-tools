//
// Created by psycho on 20.12.2021.
//

#ifndef CPP_LIB_BINARY_TREE_H
#define CPP_LIB_BINARY_TREE_H

#include <boost/python.hpp>
#include <utility>
#include <algorithm>

using namespace boost;

class binary_tree_node{
  python::object value;
  binary_tree_node* left;
  binary_tree_node* right;
  binary_tree_node* parent;
  uint depth;
public:
  explicit binary_tree_node(python::object value);
  python::object get_value();
  [[nodiscard]] bool has_left() const;
  [[nodiscard]] bool has_right() const;
  [[nodiscard]] bool has_parent() const;
  [[nodiscard]] uint get_depth() const;
  [[nodiscard]] uint left_depth() const;
  [[nodiscard]] uint right_depth() const;
  void inc_depth();
  void dec_depth();
  void set_depth(uint val);
  void set_left(binary_tree_node* other);
  void set_right(binary_tree_node* other);
  void set_parent(binary_tree_node* other);
  binary_tree_node* get_left();
  binary_tree_node* get_right();
  binary_tree_node* get_parent();
  [[nodiscard]] uint get_balance_factor() const;
};

class binary_tree {
  binary_tree_node* root;
public:
  binary_tree();
  void add(const python::object& value);
  void insert(binary_tree_node* node);
  [[nodiscard]] bool is_empty() const;
  [[nodiscard]] bool contains(const python::object& value) const;
  [[nodiscard]] uint get_depth() const;
  [[nodiscard]] binary_tree_node* catch_node(const python::object& value) const;
  void rotate_left(binary_tree_node* node);
  void rotate_right(binary_tree_node* node);
  void balance(binary_tree_node* node);
};


#endif //CPP_LIB_BINARY_TREE_H

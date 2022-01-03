//
// Created by psycho on 20.12.2021.
//

#include "binary_tree.h"

binary_tree_node::binary_tree_node(python::object value) {
  this->value = std::move(value);
  this->left = nullptr;
  this->right = nullptr;
  this->parent = nullptr;
  this->depth = 1;
}

bool binary_tree_node::has_left() const {
  return this->left != nullptr;
}

bool binary_tree_node::has_right() const {
  return this->right != nullptr;
}

bool binary_tree_node::has_parent() const {
  return this->parent != nullptr;
}

uint binary_tree_node::get_depth() const {
  return this->depth;
}

uint binary_tree_node::left_depth() const {
  if (this->has_left()) {
    return this->left->get_depth();
  } else {
    return 0;
  }
}

uint binary_tree_node::right_depth() const {
  if (this->has_right()) {
    return this->right->get_depth();
  } else {
    return 0;
  }
}

void binary_tree_node::set_left(binary_tree_node *other) {
  this->left = other;
  if (other != nullptr) {
    other->set_parent(this);
  }
}

void binary_tree_node::set_right(binary_tree_node *other) {
  this->right = other;
  if (other != nullptr) {
    other->set_parent(this);
  }
}

void binary_tree_node::set_parent(binary_tree_node *other) {
  this->parent = other;
}

binary_tree_node *binary_tree_node::get_left() {
  return this->left;
}

binary_tree_node *binary_tree_node::get_right() {
  return this->right;
}

binary_tree_node *binary_tree_node::get_parent() {
  return this->parent;
}

python::object binary_tree_node::get_value() {
  return this->value;
}

void binary_tree_node::inc_depth() {
  this->depth++;
}

void binary_tree_node::dec_depth() {
  this->depth--;
}

void binary_tree_node::set_depth(uint val) {
  this->depth = val;
}

uint binary_tree_node::get_balance_factor() const {
  if (this->left_depth() > this->right_depth()) {
    return this->left_depth() - this->right_depth();
  } else {
    return this->right_depth() - this->left_depth();
  }
}


binary_tree::binary_tree() {
  this->root = nullptr;
}

void binary_tree::add(const python::object &value) {
  auto new_node = new binary_tree_node(value);
  if (this->is_empty()) {
    this->root = new_node;
  } else {
    this->insert(new_node);
  }
}

void binary_tree::insert(binary_tree_node *existing_node) {
  auto *node = this->root;
  auto **visited_nodes = new binary_tree_node *[this->get_depth()];
  uint visited_depth = 0;
  while (true) {
    if (node->get_value() == existing_node->get_value()) {
      return;
    }
    visited_nodes[visited_depth] = node;
    visited_depth++;
    if (node->get_value() > existing_node->get_value()) {
      if (node->has_left()) {
        node = node->get_left();
      } else {
        node->set_left(existing_node);
        break;
      }
    } else {
      if (node->has_right()) {
        node = node->get_right();
      } else {
        node->set_right(existing_node);
        break;
      }
    }
  }
  for (uint i = visited_depth; i > 0; i--) {
    node = visited_nodes[i - 1];
    if ((node->get_value() > existing_node->get_value()) && (node->left_depth() + 1 > node->right_depth())) {
      node->inc_depth();
    }
    if ((node->get_value() < existing_node->get_value()) && (node->right_depth() + 1 > node->left_depth())) {
      node->inc_depth();
    }
    this->balance(node);
  }
}

bool binary_tree::is_empty() const {
  return this->root == nullptr;
}

bool binary_tree::contains(const python::object &value) const {
  return (this->catch_node(value) != nullptr);
}

uint binary_tree::get_depth() const {
  if (this->is_empty()) {
    return 0;
  } else {
    return this->root->get_depth();
  }
}

binary_tree_node *binary_tree::catch_node(const python::object& value) const {
  if (this->is_empty()) {
    return nullptr;
  } else {
    auto *node = this->root;
    while (true) {
      if (node->get_value() == value) {
        return node;
      }
      if (node->get_value() > value) {
        if (node->has_left()) {
          node = node->get_left();
        } else {
          return nullptr;
        }
      } else {
        if (node->has_right()) {
          node = node->get_right();
        } else {
          return nullptr;
        }
      }
    }
  }
}

void binary_tree::rotate_left(binary_tree_node *node) {
  auto z = node;
  auto p = z->get_parent();
  auto y = z->get_right();
  auto t3 = y->get_left();

  if (p != nullptr) {
    if (p->get_value() > y->get_value()) {
      p->set_left(y);
    } else {
      p->set_right(y);
    }
  } else {
    y->set_parent(p);
    this->root = y;
  }
  y->set_left(z);
  z->set_right(t3);

  z->set_depth(std::max(z->left_depth(), z->right_depth()) + 1);
  y->set_depth(std::max(y->left_depth(), y->right_depth()) + 1);
  if (p != nullptr) {
    p->set_depth(std::max(p->left_depth(), p->right_depth()) + 1);
  }
}

void binary_tree::rotate_right(binary_tree_node *node) {
  auto z = node;
  auto p = z->get_parent();
  auto y = z->get_left();
  auto t3 = y->get_right();

  if (p != nullptr) {
    if (p->get_value() > y->get_value()) {
      p->set_left(y);
    } else {
      p->set_right(y);
    }
  } else {
    y->set_parent(p);
    this->root = y;
  }
  y->set_right(z);
  z->set_left(t3);

  z->set_depth(std::max(z->left_depth(), z->right_depth()) + 1);
  y->set_depth(std::max(y->left_depth(), y->right_depth()) + 1);
  if (p != nullptr) {
    p->set_depth(std::max(p->left_depth(), p->right_depth()) + 1);
  }
}

void binary_tree::balance(binary_tree_node *node) {
  if (node->get_balance_factor() > 1) {
    if (node->left_depth() > node->right_depth()) {
      if (node->get_left()->left_depth() > node->get_left()->right_depth()) {
        //L-L case
        this->rotate_right(node);
      } else {
        //L-R case
        this->rotate_left(node->get_left());
        this->rotate_right(node);
      }
    } else {
      if (node->get_right()->right_depth() > node->get_right()->left_depth()) {
        //R-R case
      } else {
        //R-L case
        this->rotate_right(node->get_right());
        this->rotate_left(node);
      }
    }
  }
}

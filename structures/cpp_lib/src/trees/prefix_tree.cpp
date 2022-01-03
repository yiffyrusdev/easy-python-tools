//
// Created by psycho on 20.12.2021.
//

#include "prefix_tree.h"
#include <stdio.h>

prefix_tree_node::prefix_tree_node() {
  this->value = *new python::object();
  this->terminations = 0;
  this->children = new std::unordered_map<python::object, prefix_tree_node*>();
}

prefix_tree_node::prefix_tree_node(python::object value) : prefix_tree_node() {
  this->value = std::move(value);
}

size_t std::hash<python::object>::operator()(const python::object &obj) const noexcept {
  return PyObject_Hash(obj.ptr());
}

prefix_tree::prefix_tree() {
  this->root = new prefix_tree_node();
}

void prefix_tree::add(python::object &sequence) {
  auto iter = PyObject_GetIter(sequence.ptr());
  if (iter == nullptr){
    return;
  }

  PyObject *item;
  uint i;
  auto node = this->root;
  for (i = 0, item = PyIter_Next(iter); item; ++i, item = PyIter_Next(iter)){
    python::object obj((python::handle<>(item)));
    if (node->children->contains(obj)){
      node = node->children->at(obj);
    }else{
      auto new_node = new prefix_tree_node(obj);
      node->children->insert({obj, new_node});
      node = new_node;
    }
  }
  node->terminations++;
}

prefix_tree_node *prefix_tree::catch_node(python::object &sequence) const{
  auto iter = PyObject_GetIter(sequence.ptr());
  if (iter == nullptr){
    return nullptr;
  }

  PyObject *item;
  uint i;
  auto node = this->root;
  for (i = 0, item = PyIter_Next(iter); item; ++i, item = PyIter_Next(iter)){
    python::object obj((python::handle<>(item)));
    if (node->children->contains(obj)){
      node = node->children->at(obj);
    }else{
      return nullptr;
    }
  }
  return node;
}

bool prefix_tree::contains(python::object &sequence) const {
  return (this->count(sequence) > 0);
}

uint prefix_tree::count(python::object &sequence) const {
  auto node = this->catch_node(sequence);
  if (node == nullptr){
    return 0;
  }
  return node->terminations;
}

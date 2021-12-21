//
// Created by psycho on 19.12.2021.
//

#include "stack.h"

stack_item::stack_item(boost::python::object value) : value(std::move(value)), prev(nullptr) {}


stack::stack(){
  this->size = 0;
  this->last = nullptr;
}

boost::python::object stack::pop() {
  if (this->is_empty()){
    return {};
  }else{
   stack_item *p = this->last;
    this->last = p->prev;
    this->size--;
    return p->value;
  }
}

boost::python::object stack::top() {
  if (this->is_empty()){
    return {};
  }else {
    return this->last->value;
  }
}

void stack::push(boost::python::object value) {
  auto *p = new stack_item(std::move(value));
  p->prev = this->last;
  this->last = p;
  this->size++;
}

bool stack::is_empty() {
  return this->size == 0;
}

uint stack::get_size() const {
  return this->size;
}

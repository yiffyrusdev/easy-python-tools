//
// Created by psycho on 19.12.2021.
//

#include "queue.h"

queue_item::queue_item(python::object value) {
  this->value = std::move(value);
  this->next = nullptr;
}

queue::queue() {
  this->size = 0;
  this->first = nullptr;
  this->last = nullptr;
}

void queue::add(python::object value) {
  auto *i = new queue_item(std::move(value));
  if (this->is_empty()){
    this->first = i;
    this->last = i;
  }else{
   this->last->next = i;
    this->last = i;
  }
  this->size++;
}

python::object queue::next() {
  if (this->is_empty()){
   return {};
  }else {
    auto *i = this->first;
    this->first = i->next;
    this->size--;
    return i->value;
  }
}

bool queue::is_empty() {
  return this->size == 0;
}

uint queue::get_size() const {
  return this->size;
}

python::object queue::get_first() {
  if (this->is_empty()){
    return {};
  }else {
    return this->first->value;
  }
}

python::object queue::get_last() {
  if (this->is_empty()){
    return {};
  }else {
    return this->last->value;
  }
}

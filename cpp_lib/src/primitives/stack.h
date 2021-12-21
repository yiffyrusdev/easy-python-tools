//
// Created by psycho on 19.12.2021.
//

#ifndef CPP_LIB_STACK_H
#define CPP_LIB_STACK_H

#include <boost/python.hpp>
#include <utility>

using namespace std;
using namespace boost::python;

struct stack_item{
  boost::python::object value;
  stack_item *prev;
  explicit stack_item(boost::python::object value);
};

class stack {
  stack_item *last;
  uint size;
public:
  stack();
  void push(boost::python::object value);
  boost::python::object pop();
  boost::python::object top();
  bool is_empty();
  [[nodiscard]] uint get_size() const;
};

#endif //CPP_LIB_STACK_H
